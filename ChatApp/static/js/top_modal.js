// モーダルを開く
function openModal(modalId) {
  document.getElementById(modalId).style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
}
// モーダルを閉じる
function closeModal(modalId) {
  document.getElementById(modalId).style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
}