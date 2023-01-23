const usernameField = document.querySelector("#usernameField");
const feedbackAreaUsername = document.querySelector(".usernameFeedbackArea")
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector("#submitRegistration");
const toggleShowPassword = document.querySelector("#toggleShowPassword");
const passwordField = document.querySelector("#passwordField");
// let myModal = document.getElementById('myModal');
// let myInput = document.getElementById('myInput');
//
// myModal.addEventListener('shown.bs.modal', function () {
//   myInput.focus()
// })

toggleShowPassword.addEventListener("click", (e)=>{
    if(toggleShowPassword.textContent === "SHOW") {
        toggleShowPassword.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }
    else {
        toggleShowPassword.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
})

usernameField.addEventListener("input", (e) =>
{
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
        console.log(data);
        if(data.username_error) {
            usernameField.classList.remove("is-valid");
            usernameField.classList.add("is-invalid");
            feedbackAreaUsername.innerHTML = `<p>${data.username_error}</p>`;
            feedbackAreaUsername.style.display = 'contents';
            submitBtn.disabled = true;
        }
        else {
            usernameField.classList.remove("is-invalid");
            usernameField.classList.add("is-valid");
            feedbackAreaUsername.style.display = 'none';
            submitBtn.removeAttribute("disabled");
        }
      });
    }


})














// const usernameField = document.querySelector("#usernameField");
// const feedBackArea = document.querySelector(".invalid_feedback");
// const emailField = document.querySelector("#emailField");
// const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
// const passwordField = document.querySelector("#passwordField");
// const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
// const showPasswordToggle = document.querySelector(".showPasswordToggle");
// const submitBtn = document.querySelector(".submit-btn");
// const handleToggleInput = (e) => {
//   if (showPasswordToggle.textContent === "SHOW") {
//     showPasswordToggle.textContent = "HIDE";
//     passwordField.setAttribute("type", "text");
//   } else {
//     showPasswordToggle.textContent = "SHOW";
//     passwordField.setAttribute("type", "password");
//   }
// };
//
// showPasswordToggle.addEventListener("click", handleToggleInput);
//
// emailField.addEventListener("keyup", (e) => {
//   const emailVal = e.target.value;
//
//   emailField.classList.remove("is-invalid");
//   emailFeedBackArea.style.display = "none";
//
//   if (emailVal.length > 0) {
//     fetch("/authentication/validate-email", {
//       body: JSON.stringify({ email: emailVal }),
//       method: "POST",
//     })
//       .then((res) => res.json())
//       .then((data) => {
//         console.log("data", data);
//         if (data.email_error) {
//           submitBtn.disabled = true;
//           emailField.classList.add("is-invalid");
//           emailFeedBackArea.style.display = "block";
//           emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
//         } else {
//           submitBtn.removeAttribute("disabled");
//         }
//       });
//   }
// });
//
// usernameField.addEventListener("keyup", (e) => {
//   const usernameVal = e.target.value;
//
//   usernameSuccessOutput.style.display = "block";
//
//   usernameSuccessOutput.textContent = `Checking  ${usernameVal}`;
//
//   usernameField.classList.remove("is-invalid");
//   feedBackArea.style.display = "none";
//
//   if (usernameVal.length > 0) {
//     fetch("/authentication/validate-username", {
//       body: JSON.stringify({ username: usernameVal }),
//       method: "POST",
//     })
//       .then((res) => res.json())
//       .then((data) => {
//         usernameSuccessOutput.style.display = "none";
//         if (data.username_error) {
//           usernameField.classList.add("is-invalid");
//           feedBackArea.style.display = "block";
//           feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
//           submitBtn.disabled = true;
//         } else {
//           submitBtn.removeAttribute("disabled");
//         }
//       });
//   }
// });