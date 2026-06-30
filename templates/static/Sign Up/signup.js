const $ = (sel) => document.querySelector(sel);

const form = $("#signupForm");
const togglePw = $("#togglePw");
const pw = $("#password");
const cpw = $("#confirmPassword");
const submitBtn = $("#submitBtn");

$("#year").textContent = new Date().getFullYear();

// Show / hide password
togglePw.addEventListener("click", () => {
  const showing = pw.type === "text";
  pw.type = showing ? "password" : "text";
  cpw.type = showing ? "password" : "text";
  togglePw.textContent = showing ? "Show" : "Hide";
});

// Basic password rule: 8+ chars, at least 1 letter + 1 number
function strongPassword(value){
  const hasLetter = /[A-Za-z]/.test(value);
  const hasNumber = /[0-9]/.test(value);
  return value.length >= 8 && hasLetter && hasNumber;
}

// Confirm password validity updates live
function validateConfirm(){
  const ok = cpw.value.length > 0 && cpw.value === pw.value;
  cpw.setCustomValidity(ok ? "" : "Passwords do not match");
}

pw.addEventListener("input", () => {
  pw.setCustomValidity(strongPassword(pw.value) ? "" : "Weak password");
  validateConfirm();
});
cpw.addEventListener("input", validateConfirm);

form.addEventListener("submit", (e) => {
  // Apply our password rule
  pw.setCustomValidity(strongPassword(pw.value) ? "" : "Weak password");
  validateConfirm();

  // If invalid: stop submit and show validation UI (Bootstrap style)
  if (!form.checkValidity()){
    e.preventDefault();
    e.stopPropagation();
    form.classList.add("was-validated");
    return;
  }

  // If valid: allow normal POST to Flask (DO NOT preventDefault)
  // Optional UX: show loading state
  submitBtn.disabled = true;
  submitBtn.textContent = "Creating...";
});