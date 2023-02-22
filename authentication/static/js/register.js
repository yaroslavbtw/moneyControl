const usernameField = document.querySelector("#usernameField");
const helpBlockUsername = document.querySelector("#usernameHelpBlock");
const emailField = document.querySelector("#emailField");
const helpBlockEmail = document.querySelector("#emailHelpBlock");
const toggleShowPassword = document.querySelector("#showPasswordToggle");
const passwordField = document.querySelector("#passwordField");
const helpBlockPassword = document.querySelector("#passwordHelpBlock");
const signUpButton = document.querySelector("#signUpButton");
const formReg = document.querySelector(".form_register");
let usernameHelpBlockText = 'Your username must be 5-20 characters long, only contain letters and numbers.';
let emailHelpBlockText = 'Your mail should look like a template: name@example.com.';



toggleShowPassword.addEventListener("click", (e)=>{
    if(toggleShowPassword.checked)
        passwordField.setAttribute("type", "text");
    else passwordField.setAttribute("type", "password");
})
usernameField.addEventListener("focus", (e)=> {
    helpBlockUsername.children[0].textContent = usernameHelpBlockText;
})
usernameField.addEventListener("focusout", (e)=> {
    helpBlockUsername.children[0].textContent = '';
})
emailField.addEventListener("focus", (e)=> {
    helpBlockEmail.children[0].textContent = emailHelpBlockText;
})
emailField.addEventListener("focusout", (e)=> {
    helpBlockEmail.children[0].textContent = '';
})
passwordField.addEventListener("focus", (e)=> {
    helpBlockPassword.children[0].textContent = 'Your password must be 8-20 characters long.';
})
passwordField.addEventListener("focusout", (e)=> {
    helpBlockPassword.children[0].textContent = '';
})

usernameField.addEventListener("input", (e) => {
    let usernameVal = e.target.value;
    if(usernameVal.length > 0)
    {
        fetch("/authentication/validate-username/", {
          body: JSON.stringify({ username: usernameVal }),
          method: "POST",
        })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if(data.username_error) {
            usernameField.classList.remove("is-valid");
            usernameField.classList.add("is-invalid");
            usernameHelpBlockText = `${data.username_error}`
            helpBlockUsername.children[0].textContent = usernameHelpBlockText;
        } else {
            usernameField.classList.remove("is-invalid");
            usernameField.classList.add("is-valid");
            usernameHelpBlockText = 'This nickname is available.';
            helpBlockUsername.children[0].textContent = usernameHelpBlockText;
        }
      });
    }else{
        usernameField.classList.remove("is-valid");
        usernameField.classList.add("is-invalid");
        usernameHelpBlockText = 'Your username must be 5-20 characters long, only contain letters and numbers.';
        helpBlockUsername.children[0].textContent = usernameHelpBlockText;
    }
})

emailField.addEventListener("input", (e) => {
    let emailVal = e.target.value;
    console.log(emailVal);
    if(emailVal.length > 0)
    {
        fetch("/authentication/validate-email/", {
          body: JSON.stringify({ email: emailVal}),
          method: "POST",
        })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if(data.email_error) {
            emailField.classList.remove("is-valid");
            emailField.classList.add("is-invalid");
            emailHelpBlockText = `${data.email_error}`
            helpBlockEmail.children[0].textContent = emailHelpBlockText;
        } else {
            emailField.classList.remove("is-invalid");
            emailField.classList.add("is-valid");
            emailHelpBlockText = 'This email is available.';
            helpBlockEmail.children[0].textContent = emailHelpBlockText;
        }
      });
    }else {
        emailField.classList.remove("is-valid");
        emailField.classList.add("is-invalid");
        emailHelpBlockText = 'Your mail should look like a template: name@example.com.';
        helpBlockEmail.children[0].textContent = emailHelpBlockText;
    }
})

passwordField.addEventListener("input", (e) => {
    let passwordVal = e.target.value;
    console.log(passwordVal);
    if(passwordVal.length < 8) {
        passwordField.classList.remove("is-valid");
        passwordField.classList.add("is-invalid");
        helpBlockPassword.children[0].textContent = 'Your password must be 8-20 characters long.';
    } else {
        passwordField.classList.remove("is-invalid");
        passwordField.classList.add("is-valid");
        helpBlockPassword.children[0].textContent = 'This password is compliant.';
    }
})

signUpButton.addEventListener("click", (e)=>{
    e.preventDefault();
    if(usernameField.value.length < 5){
        usernameField.classList.add("is-invalid");
        helpBlockUsername.children[0].textContent = usernameHelpBlockText;
    }
    if(emailField.value.length === 0) {
        emailField.classList.add("is-invalid");
        helpBlockEmail.children[0].textContent = emailHelpBlockText;
    }
    if(passwordField.value.length < 8) {
        passwordField.classList.add("is-invalid");
        helpBlockPassword.children[0].textContent = 'Your password must be 8-20 characters long.';
    }
    if(usernameField.classList.contains("is-valid") && emailField.classList.contains("is-valid")
        && passwordField.classList.contains("is-valid"))
        formReg.submit();
})
