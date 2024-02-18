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

AFRAME.registerComponent('play-video-on-click', {
    init: function () {
        var videoEl = document.querySelector('#videoSource');
        var video_player = document.querySelector('#videoPlayer');
        var player_pose = document.querySelector('#pose');
        var score_text = document.querySelector('#score');
        var el = this.el;
        this.el.addEventListener('click', function () {
            if (videoEl.paused) {
                el.removeAttribute('class');
                el.setAttribute('visible', false);
                player_pose.setAttribute('visible', true);
                score_text.setAttribute('visible', true);
                setTimeout(() => {
                    videoEl.play();
                    video_player.setAttribute('visible', true);
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
        });
        videoEl.addEventListener('ended', function () {
            setTimeout(() => {
                video_player.setAttribute('visible', false);
                player_pose.setAttribute('visible', false);
                score_text.setAttribute('visible', false);
                display_results();
            }, 1000);
            // el.setAttribute('class', 'clickable');
            // el.setAttribute('visible', true);
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

function start_game() {
    setTimeout(() => {
        var button = document.querySelector('#startButton_entity');
        var pose = document.querySelector('#pose');
        button.setAttribute('visible', true);
        button.setAttribute('class', 'clickable');
        pose.setAttribute('visible', true);
    }, 500);
}

AFRAME.registerComponent('open-menu-on-click', {
    init: function () {
        this.el.addEventListener('click', () => {
            var logo = document.querySelector('#logo_entity');
            var playButton = document.querySelector('#playButton_entity');
            logo.emit('fadeOut');
            playButton.emit('fadeOut');
            playButton.removeAttribute('class');
            var soundEl = document.createElement('a-sound');
            soundEl.setAttribute('src', '#intro');
            soundEl.setAttribute('autoplay', 'true');
            soundEl.setAttribute('position', '0 0 0');
            var sceneEl = document.querySelector('a-scene');
            sceneEl.appendChild(soundEl);
            setTimeout(() => {
                chen_entity.emit('fadeIn');
                chen_entity.setAttribute('class', 'clickable');
                sun_entity.emit('fadeIn');
                sun_entity.setAttribute('class', 'clickable');
                yang_entity.emit('fadeIn');
                yang_entity.setAttribute('class', 'clickable');
                wu_entity.emit('fadeIn');
                wu_entity.setAttribute('class', 'clickable');
            }, 500);
        });
    }
});

AFRAME.registerComponent('chen-environment-on-click', {
    init: function () {
        this.el.addEventListener('click', () => {
            sun_entity.emit('fadeOut');
            yang_entity.emit('fadeOut');
            wu_entity.emit('fadeOut');
            sun_entity.removeAttribute('class');
            yang_entity.removeAttribute('class');
            wu_entity.removeAttribute('class');
            chen_entity.emit('selected');
            setTimeout(() => {
                chen_entity.emit('fadeOut');
                chen_entity.emit('deselected');
                chen_entity.removeAttribute('class');
                var environment = document.querySelector('#environment');
                environment.setAttribute('environment', 'skyColor', '#24b59f');
                environment.setAttribute('horizonColor', 'skyColor', '#eff9b7');
                start_game();
            }, 500);
        });
    }
});

AFRAME.registerComponent('sun-environment-on-click', {
    init: function () {
        this.el.addEventListener('click', () => {
            chen_entity.emit('fadeOut');
            yang_entity.emit('fadeOut');
            wu_entity.emit('fadeOut');
            chen_entity.removeAttribute('class');
            yang_entity.removeAttribute('class');
            wu_entity.removeAttribute('class');
            sun_entity.emit('selected');
            setTimeout(() => {
                sun_entity.emit('fadeOut');
                sun_entity.emit('deselected')
                sun_entity.removeAttribute('class');
                var environment = document.querySelector('#environment');
                environment.setAttribute('environment', 'skyColor', '#7E1529');
                environment.setAttribute('horizonColor', 'skyColor', '#FFFF74');
                start_game();
            }, 500);
        });
    }
});

AFRAME.registerComponent('yang-environment-on-click', {
    init: function () {
        this.el.addEventListener('click', () => {
            sun_entity.emit('fadeOut');
            chen_entity.emit('fadeOut');
            wu_entity.emit('fadeOut');
            sun_entity.removeAttribute('class');
            chen_entity.removeAttribute('class');
            wu_entity.removeAttribute('class');
            yang_entity.emit('selected');
            setTimeout(() => {
                yang_entity.emit('fadeOut');
                yang_entity.emit('deselected');
                yang_entity.removeAttribute('class');
                var environment = document.querySelector('#environment');
                environment.setAttribute('environment', 'skyColor', '#45788B');
                environment.setAttribute('horizonColor', 'skyColor', '#FFFFFF');
                start_game();
            }, 500);
        });
    }
});

AFRAME.registerComponent('wu-environment-on-click', {
    init: function () {
        this.el.addEventListener('click', () => {
            sun_entity.emit('fadeOut');
            yang_entity.emit('fadeOut');
            chen_entity.emit('fadeOut');
            sun_entity.removeAttribute('class');
            yang_entity.removeAttribute('class');
            chen_entity.removeAttribute('class');
            wu_entity.emit('selected');
            setTimeout(() => {
                wu_entity.emit('fadeOut');
                wu_entity.emit('deselected');
                wu_entity.removeAttribute('class');
                var environment = document.querySelector('#environment');
                environment.setAttribute('environment', 'skyColor', '#001F3C');
                environment.setAttribute('horizonColor', 'skyColor', '#A95D53');
                start_game();
            }, 500);
        });
    }
});

function display_results() {
    var finish_entity = document.querySelector('#finish_entity');
    var results_entity = document.querySelector('#results_entity');
    var back_entity = document.querySelector('#back_entity');
    var score_results = document.querySelector('#score_results');
    finish_entity.emit('fadeIn');
    results_entity.emit('fadeIn');
    back_entity.emit('fadeIn');
    setTimeout(() => {
        score_results.setAttribute('visible', true);
    }, 500);
    back_entity.setAttribute('class', 'clickable');
}

AFRAME.registerComponent('open-menu-from-results', {
    init: function () {
        this.el.addEventListener('click', () => {
            var finish_entity = document.querySelector('#finish_entity');
            var results_entity = document.querySelector('#results_entity');
            var back_entity = document.querySelector('#back_entity');
            var score_results = document.querySelector('#score_results');
            finish_entity.emit('fadeOut');
            results_entity.emit('fadeOut');
            back_entity.emit('fadeOut');
            score_results.setAttribute('visible', false);
            back_entity.removeAttribute('class');
            setTimeout(() => {
                chen_entity.emit('fadeIn');
                chen_entity.setAttribute('class', 'clickable');
                sun_entity.emit('fadeIn');
                sun_entity.setAttribute('class', 'clickable');
                yang_entity.emit('fadeIn');
                yang_entity.setAttribute('class', 'clickable');
                wu_entity.emit('fadeIn');
                wu_entity.setAttribute('class', 'clickable');
            }, 500);
        });
    }
});

// https://stackoverflow.com/questions/62048075/lights-in-a-frame-have-striped-artifacts-depending-on-distance-from-them
AFRAME.registerComponent('fix-shadow', { 
    dependencies: ['material'],
  
    init: function () {
      this.el.addEventListener('model-loaded', () => {
        const mesh = this.el.getObject3D('mesh');
        if (!mesh) return;
        mesh.traverse(node => {
          if (node.isMesh) {
            node.material.shadowSide = THREE.BackSide;
          }
        });
      });
    }
  });