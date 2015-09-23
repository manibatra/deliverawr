function submitForm() {

    $.ajax({
        type: "POST",
        url: $('#signupForm').attr('action'), // or whatever
        data: $('#signupForm').serialize(),
        success: function(data) {
            if (data.status == 1) {
                window.location.reload();
            } else if (data.status == 0) {
                alert(data.msg);
            }
        }
    });
}

function submitloginForm() {
    document.getElementById('loginForm').submit();
};

//function to click the signup button on pressing enter
$("#signupForm input").keyup(function(event) {
    if (event.keyCode == 13) {
        $("#signupButton").click();
    }
});