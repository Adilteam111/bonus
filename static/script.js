const modal = document.getElementById('faceModal');
const video = document.getElementById('video');

function openModal() {
  modal.style.display = 'block';

  // Kameranı aç
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((err) => {
      alert("Kameraya icazə verilmədi.");
    });
}

function closeModal() {
  modal.style.display = 'none';
  if (video.srcObject) {
    video.srcObject.getTracks().forEach(track => track.stop());
  }
}
