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

function submitLoginForm() {
  var email = document.getElementById('loginEmail').value;
  var password = document.getElementById('loginPassword').value;
  closeModal('loginModal');
}

function submitRegistrationForm() {
  var name = document.getElementById('name').value;
  var email = document.getElementById('registrationEmail').value;
  var password = document.getElementById('registrationPassword').value;
  var password = document.getElementById('registrationPassword2').value;
  var password = document.getElementById('signup-club-serect').value;
  closeModal('registrationModal');
}