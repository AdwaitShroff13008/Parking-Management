# Futuristic Parking Management System

A modern, minimal, and fully-responsive Parking Management System web application built with Python (Flask) and a Three.js 3D animated background.

## Features
- **3D Animated Background**: Lightweight, smooth Three.js floating geometric shapes.
- **Glassmorphic UI**: Premium design with soft shadows, neon accents, and transparent panels.
- **Real-Time Dashboard**: View total, available, and occupied slots at a glance.
- **Vehicle Entry/Exit**: Securely register vehicle entries and process exits with automatic fee calculation (₹20/hr).
- **Live Parking Status**: Visual grid displaying the current state of all 20 parking slots.
- **Prisma Studio Integration**: Easily view the underlying SQLite database using Prisma Studio.

## Architecture
- **Backend**: Python with Flask
- **Database**: SQLite (visualized via Prisma)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Properties), Vanilla JS, Three.js (via CDN)

## Prerequisites
- **Python 3.x**
- **Node.js & npm** (only required for running `npx prisma studio` to view the database)

## Quick Start Guide

### 1. Set up the Python Backend
First, ensure you have Flask installed:
```bash
pip install flask
```

Next, run the Flask application. This will automatically create the SQLite database (`database.db`) with the required `vehicles` table if it doesn't already exist.
```bash
python app.py
```
> **Note:** The server will run on [http://localhost:5000](http://localhost:5000). Keep this terminal open.

### 2. View the Database using Prisma Studio (Optional)
To interactively view the database entries, open a **new terminal** in the `parking-management-system` folder and run:
```bash
npm install
npx prisma db push
npx prisma studio
```
> **Note:** Prisma Studio will open automatically in your browser, typically at [http://localhost:5555](http://localhost:5555).

## Directory Structure
```
parking-management-system/
│
├── app.py                 # Main Flask application and backend routes
├── database.db            # SQLite database (auto-generated)
├── README.md              # Project documentation
│
├── prisma/                
│   └── schema.prisma      # Prisma schema for viewing the database
│
├── templates/             # HTML templates for rendering
│   ├── base.html          # Base layout with Three.js canvas
│   ├── index.html         # Dashboard
│   ├── parking.html       # Visual slot status
│   ├── entry.html         # Vehicle entry form
│   └── exit.html          # Vehicle exit form
│
└── static/                # Static assets
    ├── css/
    │   └── style.css      # Custom styling and glassmorphism
    ├── js/
    │   ├── main.js        # Frontend animations and logic
    │   └── three-bg.js    # Three.js 3D background animation
```
