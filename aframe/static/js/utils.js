const POSE_CONNECTIONS = [
    [15, 21], [16, 20], [18, 20], [3, 7], [14, 16], [23, 25], [28, 30], [11, 23], [27, 31], [6, 8],
    [15, 17], [24, 26], [16, 22], [4, 5], [5, 6], [29, 31], [12, 24], [23, 24], [0, 1], [9, 10],
    [1, 2], [0, 4], [11, 13], [30, 32], [28, 32], [15, 19], [16, 18], [25, 27], [26, 28], [12, 14],
    [17, 19], [2, 3], [11, 12], [27, 29], [13, 15]
];

function landmarkDistance(landmark1, landmark2){
    return Math.sqrt((landmark2.x-landmark1.x)*(landmark2.x-landmark1.x) + (landmark2.y-landmark1.y)*(landmark2.y-landmark1.y))
}

function drawSphere(scene, x, y, z, color, radius){
    const sphere = document.createElement('a-sphere');
    sphere.setAttribute('color', color);
    sphere.setAttribute('radius', radius);
    sphere.setAttribute('position', `${x} ${y} ${z}`);
    scene.appendChild(sphere);
}

AFRAME.registerComponent("overlay", {
    dependencies: ['material'],
    init: function () {
    this.el.sceneEl.renderer.sortObjects = true;
    this.el.object3D.renderOrder = 100;
    this.el.components.material.material.depthTest = false;
    }
});

AFRAME.registerComponent("thick-line", {
    schema: {
        start: {type: 'vec3'},
        end: {type: 'vec3'},
        thickness: {type: 'number', default: 0.05},
        color: {type: 'color', default: '#000000'}
    },
    init: function() {
        const {start, end, thickness, color} = this.data;
        const curve = new THREE.LineCurve3(new THREE.Vector3(start.x, start.y, start.z), new THREE.Vector3(end.x, end.y, end.z));
        const geometry = new THREE.TubeGeometry(curve, 20, thickness, 8, false);
        const material = new THREE.MeshBasicMaterial({color: color});
        const mesh = new THREE.Mesh(geometry, material);
        this.el.object3D.add(mesh);
    }
});

AFRAME.registerComponent('change-color-on-click', {
    init: function () {
        this.el.addEventListener('click', (evt) => {
        const randomColor = '#' + Math.floor(Math.random()*16777215).toString(16);
        this.el.setAttribute('material', 'color', randomColor);
        });
    }
});

AFRAME.registerComponent('play-video-on-click', {
    init: function () {
        var videoEl = document.querySelector('#calibrationVideo');
        var video_player = document.querySelector('#videoPlayer');
        var player_pose = document.querySelector('#pose');
        var el = this.el;
        this.el.addEventListener('click', function () {
            if (videoEl.paused) {
                el.setAttribute('visible', false);
                player_pose.setAttribute('visible', true);
                setTimeout(() => {
                    video_player.setAttribute('visible', true);
                    videoEl.play();
                    fetch('/video-started', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: 'Video has started' }),
                    })
                    .then(response => response.json())
                    .then(data => console.log(data))
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                }, 4000);
            } 
            // else {
            //     videoEl.pause();
            //     el.setAttribute('visible', true);
            // }
        });
        videoEl.addEventListener('ended', function () {
            video_player.setAttribute('visible', false);
            player_pose.setAttribute('visible', false);
            el.setAttribute('visible', true);
        });
    }
});

AFRAME.registerComponent('hover-color-change', {
    schema: {
        hoverColor: {type: 'color', default: '#FF0000'},
        originalColor: {type: 'color', default: '#00FF00'}
    },
    init: function() {
        var el = this.el;
        var data = this.data;
        var laser_count = 0;
        el.setAttribute('material', 'color', data.originalColor);
        el.addEventListener('raycaster-intersected', function () {
            el.setAttribute('material', 'color', data.hoverColor);
            laser_count += 1;
        });
        el.addEventListener('raycaster-intersected-cleared', function () {
            laser_count -= 1;
            if (laser_count == 0) el.setAttribute('material', 'color', data.originalColor);
        });
    }
});

AFRAME.registerComponent('hover-image-change', {
    schema: {
        hoverImage: {type: 'string', default: ''},
        originalImage: {type: 'string', default: ''}
    },
    init: function() {
        var el = this.el;
        var data = this.data;
        var laser_count = 0;
        el.setAttribute('material', 'src', data.originalImage);
        el.addEventListener('raycaster-intersected', function () {
            el.setAttribute('material', 'src', data.hoverImage);
            laser_count += 1;
        });
        el.addEventListener('raycaster-intersected-cleared', function () {
            laser_count -= 1;
            if (laser_count == 0) el.setAttribute('material', 'src', data.originalImage);
        });
    }
});

AFRAME.registerComponent('start-countdown', {
    init: function () {
        this.el.addEventListener('click', () => {
            let counter = 3;
            const countdownElement = document.querySelector('#countdownText');
            countdownElement.setAttribute('text', 'value', counter);
            
            const interval = setInterval(() => {
                counter--;
                if (counter > 0) {
                    countdownElement.setAttribute('text', 'value', counter);
                } else if (counter == 0) {
                    countdownElement.setAttribute('text', 'value', "Go!");
                } else {
                    clearInterval(interval);
                    countdownElement.setAttribute('text', 'value', '');
                }
            }, 1000);
        });
    }
});