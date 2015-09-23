function submitForm() {
    document.getElementById('signupForm').submit();
};

function submitloginForm() {
    document.getElementById('loginForm').submit();
};

//function to click the signup button on pressing enter
$("#signupForm input").keyup(function(event) {
    if (event.keyCode == 13) {
        $("#signupButton").click();
    }
});