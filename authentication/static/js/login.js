const toggleShowPassword = document.querySelector("#showPasswordToggle");
const passwordField = document.querySelector("#passwordField");

toggleShowPassword.addEventListener("click", (e)=>{
    if(toggleShowPassword.checked)
        passwordField.setAttribute("type", "text");
    else passwordField.setAttribute("type", "password");
})