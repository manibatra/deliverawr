$(document).ready(function() {

    $("#signupForm").validate({

        rules: {
            firstName: {
                required: true,
                rangelength: [2, 30]
            },

            lastName: {
                required: true,
                rangelength: [2, 30]
            },

            email: {
                required: true,
                email: true
            },

            password: {
                required: true,
                rangelength: [6, 30]
            }
        },

        messages: {
            firstName: {
                rangelength: "Required length : Between 2 and 30"
            },

            lastName: {
                rangelength: "Required length : Between 2 and 30"
            },

            password: {
                rangelength: "Required length : Between 6 and 30"
            }
        },

        showErrors: function(errorMap, errorList) {
            $(".error-span").css('visibility', 'hidden');
            $.each(errorMap, function(key, value) {
                $('.' + key + '-error').css('visibility', 'visible');
                $('.' + key + '-error').text(value);
            });
        },

        submitHandler: function(form) {
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
    });
});

function submitForm() {
    $('#signupForm').submit();
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