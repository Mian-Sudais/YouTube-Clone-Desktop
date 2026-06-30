const $ = (sel) => document.querySelector(sel);

const form = $("#loginForm");
const togglePw = $("#togglePw");
const pw = $("#password");
const submitBtn = $("#submitBtn");

$("#year").textContent = new Date().getFullYear();

togglePw.addEventListener("click", () => {
  const showing = pw.type === "text";
  pw.type = showing ? "password" : "text";
  togglePw.textContent = showing ? "Show" : "Hide";
});

form.addEventListener("submit", (e) => {
  // Only block submit if invalid
  if (!form.checkValidity()){
    e.preventDefault();
    e.stopPropagation();
    form.classList.add("was-validated");
    return;
  }

  // Valid -> allow normal POST to Flask (NO preventDefault)
  submitBtn.disabled = true;
  submitBtn.textContent = "Signing in...";
});