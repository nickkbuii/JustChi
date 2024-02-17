const POSE_CONNECTIONS = [
    [15, 21], [16, 20], [18, 20], [3, 7], [14, 16], [23, 25], [28, 30], [11, 23], [27, 31], [6, 8],
    [15, 17], [24, 26], [16, 22], [4, 5], [5, 6], [29, 31], [12, 24], [23, 24], [0, 1], [9, 10],
    [1, 2], [0, 4], [11, 13], [30, 32], [28, 32], [15, 19], [16, 18], [25, 27], [26, 28], [12, 14],
    [17, 19], [2, 3], [11, 12], [27, 29], [13, 15]
];

document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    socket.on('connect', function() {
        console.log('WebSocket connected!');
    });

    // Listen for pose data from the server
    socket.on('update_model', function(data) {
        const scene = document.querySelector('a-scene');
        
        // Clear existing entities (spheres and lines) to redraw them
        const existingEntities = scene.querySelectorAll('a-sphere, a-entity[line]');
        existingEntities.forEach(entity => entity.remove());

        // Create and append a new sphere for each landmark with visibility > 0.5
        data.pose.forEach(landmark => {
            if (landmark.visibility > 0.5) {
                const sphere = document.createElement('a-sphere');
                sphere.setAttribute('color', '#4CC3D9');
                sphere.setAttribute('radius', '0.02');
                
                const x = landmark.x;
                const y = landmark.y;
                const z = 0;

                sphere.setAttribute('position', `${x} ${y} ${z}`);
                scene.appendChild(sphere);
            }
        });

        // Draw lines for each connected pair in POSE_CONNECTIONS
        POSE_CONNECTIONS.forEach(pair => {
            const landmark1 = data.pose[pair[0]];
            const landmark2 = data.pose[pair[1]];

            if (landmark1.visibility > 0.5 && landmark2.visibility > 0.5) {
                const line = document.createElement('a-entity');
                const start = `${landmark1.x} ${landmark1.y} 0`;
                const end = `${landmark2.x} ${landmark2.y} 0`;
                line.setAttribute('line', `start: ${start}; end: ${end}; color: #C3C3C3`);
                scene.appendChild(line);
            }
        });
    });
});