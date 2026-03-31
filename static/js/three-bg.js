// Three.js Animated Background setup
document.addEventListener('DOMContentLoaded', () => {
    // Scene setup
    const scene = new THREE.Scene();
    
    // Camera setup
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 30;
    
    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.getElementById('three-canvas-container').appendChild(renderer.domElement);
    
    // Create particles/cubes
    const objects = [];
    const geometry = new THREE.IcosahedronGeometry(1, 0); // Cool geometric shape
    
    // Colors based on our CSS theme
    const colors = [0x00f0ff, 0x8a2be2, 0x0044ff];
    
    // Create 70 floating objects
    for (let i = 0; i < 70; i++) {
        // Create wireframe material for a futuristic outline look
        const material = new THREE.MeshBasicMaterial({ 
            color: colors[Math.floor(Math.random() * colors.length)],
            wireframe: true,
            transparent: true,
            opacity: Math.random() * 0.4 + 0.1
        });
        
        const mesh = new THREE.Mesh(geometry, material);
        
        // Random positioning across a wide area
        mesh.position.x = (Math.random() - 0.5) * 100;
        mesh.position.y = (Math.random() - 0.5) * 100;
        mesh.position.z = (Math.random() - 0.5) * 50 - 15;
        
        // Random scaling
        const scale = Math.random() * 2 + 0.5;
        mesh.scale.set(scale, scale, scale);
        
        // Store random rotation speeds
        mesh.rotationSpeedX = (Math.random() - 0.5) * 0.02;
        mesh.rotationSpeedY = (Math.random() - 0.5) * 0.02;
        
        // Store random drift velocities
        mesh.driftX = (Math.random() - 0.5) * 0.05;
        mesh.driftY = (Math.random() - 0.5) * 0.05;
        
        scene.add(mesh);
        objects.push(mesh);
    }
    
    // Add some subtle fog to fade out objects in the distance
    scene.fog = new THREE.FogExp2(0x050505, 0.015);
    
    // Animation Loop
    function animate() {
        requestAnimationFrame(animate);
        
        // Move camera slowly for a panning effect
        const time = Date.now() * 0.0001;
        camera.position.x = Math.sin(time) * 5;
        camera.position.y = Math.cos(time) * 5;
        camera.lookAt(scene.position);
        
        // Animate each object
        objects.forEach(obj => {
            // Rotate
            obj.rotation.x += obj.rotationSpeedX;
            obj.rotation.y += obj.rotationSpeedY;
            
            // Drift slowly
            obj.position.x += obj.driftX;
            obj.position.y += obj.driftY;
            
            // Loop positions if they drift too far
            if (obj.position.x > 50) obj.position.x = -50;
            if (obj.position.x < -50) obj.position.x = 50;
            if (obj.position.y > 50) obj.position.y = -50;
            if (obj.position.y < -50) obj.position.y = 50;
        });
        
        renderer.render(scene, camera);
    }
    
    // Handle Window Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    animate();
});
