AFRAME.registerComponent('hide-on-play',{
    schema:{type:'selector'},
    init:function(){
        this.onPlaying=this.onPlaying.bind(this);
        this.onPause=this.onPause.bind(this);
        this.el.object3D.visible=!this.data.playing;
    },
    play:function(){
        if(this.data){
            this.data.addEventListener('playing',this.onPlaying);
            this.data.addEventListener('pause',this.onPause);
        }
    },
    pause:function(){
        if(this.data){
            this.data.removeEventListener('playing',this.onPlaying);
            this.data.removeEventListener('pause',this.onPause);
        }
    },
    onPlaying:function(evt){
        this.el.object3D.visible=false;
    },
    onPause:function(evt){
        this.el.object3D.visible=true;
    }
});

AFRAME.registerComponent('play-on-click', {
    init: function () {
        this.onClick = this.onClick.bind(this);
    },
    play: function () {
        window.addEventListener('click', this.onClick);
    },
    pause: function () {
        window.removeEventListener('click', this.onClick);
    },
    onClick: function (evt) {
        var videoEl = this.el.getAttribute('material').src;
        if (!videoEl) { return; }
        this.el.object3D.visible = true;
        videoEl.play();
    }
});

AFRAME.registerComponent("overlay", {
        dependencies: ['material'],
        init: function () {
        this.el.sceneEl.renderer.sortObjects = true;
        this.el.object3D.renderOrder = 100;
        this.el.components.material.material.depthTest = false;
        }
});