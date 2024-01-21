import { checkpassword } from "./password_check.js"
var password = document.getElementById("newPassword1")
var strengthbar = document.getElementById("passwordSrengthStatusBar")

password.addEventListener("keyup", function () {
  const value = checkpassword(password.value)
  strengthbar.value = value
  if (value > 85) {
    strengthbar.style.accentColor = "#2B9720"
  } else if (value > 60) {
    strengthbar.style.accentColor = "#EAC435"
  } else {
    strengthbar.style.accentColor = "#C81D25"
  }
})