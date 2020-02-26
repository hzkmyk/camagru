(function() {
  
  let width = 320;
  let height = 0;    

  let streaming = false;

  let video = null;
  let canvas = null;
  let photo = null;
  let snap = null;
  let imagefield = null;
  let preview = null;
  let image = null;
  let ratio = 1.0;

  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    snap = document.getElementById('snap');
    imagefield = document.getElementById('id_image_field');
    preview = document.getElementById('preview').getContext('2d');

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    snap.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
    }, false);
    
  }

  const filterselected = function(e) {
    preview.clearRect(0, 0, width, height);
  
    const imageElem = new Image();
    imageElem.src = '/static/filters/' + e.target.defaultValue + '.png';
    image = imageElem;
    preview.drawImage(imageElem, 0, 0, width * 0.8, height * 0.63);
  }

  function takepicture() {
    let context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, width, height);
    context.drawImage(image, 0, 0, width, height);
  
    let data = canvas.toDataURL('image/png');
    imagefield.value = data;
  }

  document.getElementById('water').addEventListener('click', filterselected);
  document.getElementById('frame').addEventListener('click', filterselected);
  document.getElementById('wing').addEventListener('click', filterselected);
  
  window.addEventListener('load', startup, false);
})();
