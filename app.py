from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import datetime
import os

app = Flask(__name__)
DATABASE = 'database.db'

# Calculate fee (e.g. ₹20 per hour)
FEE_PER_HOUR = 20

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_number TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                vehicle_type TEXT NOT NULL,
                parking_class TEXT NOT NULL DEFAULT 'Standard',
                slot_number INTEGER NOT NULL,
                entry_time DATETIME NOT NULL,
                exit_time DATETIME,
                payment_method TEXT,
                fee REAL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    # Total slots (e.g. fixed at 60 for 3 floors)
    TOTAL_SLOTS = 60
    
    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status='parked'")
    occupied = cursor.fetchone()[0]
    available = TOTAL_SLOTS - occupied
    
    # Calculate customers
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    month_date = datetime.datetime.now().strftime("%Y-%m")
    year_date = datetime.datetime.now().strftime("%Y")
    
    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE entry_time LIKE ?", (today_date + '%',))
    customers_today = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE entry_time LIKE ?", (month_date + '%',))
    customers_month = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE entry_time LIKE ?", (year_date + '%',))
    customers_year = cursor.fetchone()[0]
    
    # Earnings calculations
    cursor.execute("SELECT SUM(fee) FROM vehicles WHERE exit_time LIKE ?", (today_date + '%',))
    earnings_today_result = cursor.fetchone()[0]
    earnings_today = earnings_today_result if earnings_today_result else 0
    
    cursor.execute("SELECT SUM(fee) FROM vehicles WHERE exit_time LIKE ?", (month_date + '%',))
    earnings_month_result = cursor.fetchone()[0]
    earnings_month = earnings_month_result if earnings_month_result else 0
    
    # Calculate live accrued fee for currently parked vehicles
    cursor.execute("SELECT entry_time, parking_class FROM vehicles WHERE status='parked'")
    parked_current = cursor.fetchall()
    live_accrued = 0
    now = datetime.datetime.now()
    for p in parked_current:
        entry_t = datetime.datetime.strptime(p['entry_time'], "%Y-%m-%d %H:%M:%S")
        duration = now - entry_t
        total_seconds = duration.total_seconds()
        hr = 20
        if p['parking_class'] == 'Premium': hr = 50
        elif p['parking_class'] == 'VIP': hr = 100
        live_accrued += (total_seconds / 3600) * hr
        
    earnings_today += live_accrued
    earnings_month += live_accrued
    
    earnings_today = round(earnings_today)
    earnings_month = round(earnings_month)

    # Simple graph data (Last 7 days)
    graph_labels = []
    graph_data = []
    earnings_graph_data = []
    
    for i in range(6, -1, -1):
        day_obj = datetime.datetime.now() - datetime.timedelta(days=i)
        day_str = day_obj.strftime("%Y-%m-%d")
        display_day = day_obj.strftime("%b %d") # e.g. Mar 17
        
        cursor.execute("SELECT COUNT(*) FROM vehicles WHERE entry_time LIKE ?", (day_str + '%',))
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(fee) FROM vehicles WHERE exit_time LIKE ?", (day_str + '%',))
        e_day = cursor.fetchone()[0]
        e_day = e_day if e_day else 0
        
        if day_str == today_date:
            e_day += live_accrued
            
        graph_labels.append(display_day)
        graph_data.append(count)
        earnings_graph_data.append(round(e_day))
    
    cursor.execute("SELECT slot_number, vehicle_number, owner_name, vehicle_type, parking_class FROM vehicles WHERE status='parked'")
    parked_vehicles = cursor.fetchall()
    conn.close()
    
    occupied_slots = {}
    for row in parked_vehicles:
        slot = row['slot_number']
        occupied_slots[slot] = {
            'vehicle_number': row['vehicle_number'],
            'owner_name': row['owner_name'],
            'vehicle_type': row['vehicle_type'],
            'parking_class': row['parking_class']
        }
    
    slots = []
    for i in range(1, TOTAL_SLOTS + 1):
        if i in occupied_slots:
            slots.append({'number': i, 'status': 'Occupied', 'vehicle': occupied_slots[i]})
        else:
            slots.append({'number': i, 'status': 'Available', 'vehicle': None})
            
    return render_template('index.html', 
                           total=TOTAL_SLOTS, 
                           occupied=occupied, 
                           available=available, 
                           slots=slots,
                           customers_today=customers_today,
                           customers_month=customers_month,
                           customers_year=customers_year,
                           earnings_today=earnings_today,
                           earnings_month=earnings_month,
                           graph_labels=graph_labels,
                           graph_data=graph_data,
                           earnings_graph_data=earnings_graph_data)

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number')
        owner_name = request.form.get('owner_name')
        vehicle_type = request.form.get('vehicle_type')
        parking_class = request.form.get('parking_class')
        slot_number = request.form.get('slot_number')
        
        entry_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = 'parked'
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if slot is already occupied
        cursor.execute("SELECT id FROM vehicles WHERE slot_number=? AND status='parked'", (slot_number,))
        if cursor.fetchone() is not None:
            conn.close()
            return render_template('entry.html', error=f"Slot {slot_number} is already occupied.")
            
        # Check if vehicle is already parked
        cursor.execute("SELECT id FROM vehicles WHERE vehicle_number=? AND status='parked'", (vehicle_number,))
        if cursor.fetchone() is not None:
            conn.close()
            return render_template('entry.html', error=f"Vehicle {vehicle_number} is already parked.")

        cursor.execute('''
            INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type, parking_class, slot_number, entry_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (vehicle_number, owner_name, vehicle_type, parking_class, slot_number, entry_time, status))
        
        conn.commit()
        conn.close()
        
        return render_template('entry.html', success=f"Vehicle {vehicle_number} successfully parked at slot {slot_number}.")
        
    return render_template('entry.html', prefill_slot=request.args.get('slot', ''))

@app.route('/exit', methods=['GET', 'POST'])
def exit_vehicle():
    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number')
        confirm_exit = request.form.get('confirm_exit')
        payment_method = request.form.get('payment_method', 'Cash')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Find the parked vehicle
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number=? AND status='parked'", (vehicle_number,))
        record = cursor.fetchone()
        
        if record is None:
            conn.close()
            return render_template('exit.html', error=f"No parked vehicle found with number {vehicle_number}.")
            
        entry_time_str = record['entry_time']
        entry_time = datetime.datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
        exit_time = datetime.datetime.now()
        
        # Calculate duration
        duration = exit_time - entry_time
        total_seconds = duration.total_seconds()
        
        remaining_seconds = total_seconds % 3600
        
        # Determine fee
        parking_class = record['parking_class']
        hourly_rate = 20
        if parking_class == 'Premium':
            hourly_rate = 50
        elif parking_class == 'VIP':
            hourly_rate = 100
            
        # Proportional fee calculation rounded to the nearest integer
        fee = round((total_seconds / 3600) * hourly_rate)
        
        display_hours = int(total_seconds // 3600)
        display_minutes = int(remaining_seconds // 60)
        duration_str = str(display_hours) + "h " + str(display_minutes) + "m"
        
        # If user is just checking the fee (Stage 1)
        if not confirm_exit:
            conn.close()
            return render_template('exit.html',
                                   checkout_pending=True,
                                   vehicle_number=vehicle_number,
                                   parking_class=parking_class,
                                   duration=duration_str,
                                   fee=fee)
        
        # If user is confirming exit (Stage 2)
        exit_time_str = exit_time.strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            UPDATE vehicles
            SET exit_time=?, payment_method=?, fee=?, status='exited'
            WHERE id=?
        ''', (exit_time_str, payment_method, fee, record['id']))
        
        conn.commit()
        conn.close()
        
        return render_template('exit.html', 
                               success=True, 
                               vehicle_number=vehicle_number,
                               entry_time=entry_time_str,
                               exit_time=exit_time_str,
                               duration=duration_str,
                               payment_method=payment_method,
                               fee=fee)
                               
    return render_template('exit.html', prefill_vehicle=request.args.get('vehicle', ''))



@app.route('/api/vehicle/<path:vehicle_number>')
def api_vehicle(vehicle_number):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles WHERE vehicle_number=? ORDER BY entry_time DESC", (vehicle_number,))
    records = cursor.fetchall()
    
    if not records:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
        
    total_visits = len(records)
    total_spent = sum([r['fee'] for r in records if r['fee'] is not None])
    
    latest = records[0]
    
    conn.close()
    
    return jsonify({
        'vehicle_number': vehicle_number,
        'owner_name': latest['owner_name'],
        'latest_entry': latest['entry_time'],
        'latest_exit': latest['exit_time'] if latest['exit_time'] else 'Currently Parked',
        'total_visits': total_visits,
        'total_spent': total_spent
    })

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    date_query = request.args.get('date', '').strip()
    
    conn = get_db()
    cursor = conn.cursor()
    
    if query and date_query:
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number LIKE ? AND entry_time LIKE ? ORDER BY entry_time DESC", (f'%{query}%', f'{date_query}%'))
    elif query:
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number LIKE ? ORDER BY entry_time DESC", (f'%{query}%',))
    elif date_query:
        cursor.execute("SELECT * FROM vehicles WHERE entry_time LIKE ? ORDER BY entry_time DESC", (f'{date_query}%',))
    else:
        cursor.execute("SELECT * FROM vehicles ORDER BY entry_time DESC LIMIT 100")
        
    records = cursor.fetchall()
    conn.close()
    
    return render_template('search.html', records=records, query=query, date_query=date_query)

@app.route('/activity')
def activity_log():
    conn = get_db()
    cursor = conn.cursor()
    query = '''
        SELECT vehicle_number, slot_number, entry_time AS time, 'entered' AS action 
        FROM vehicles 
        UNION ALL 
        SELECT vehicle_number, slot_number, exit_time AS time, 'exited' AS action 
        FROM vehicles 
        WHERE exit_time IS NOT NULL 
        ORDER BY time DESC 
        LIMIT 200
    '''
    cursor.execute(query)
    activities = cursor.fetchall()
    conn.close()
    return render_template('activity.html', activities=activities)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
