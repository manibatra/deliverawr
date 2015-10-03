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
                minlength: 6
            },

            phoneNo: {
                required: true,
                digits: true,
                minlength: 10,
                maxlength: 10
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
                minlength: "Required length : Atleast 6"
            },

            phoneNo: {
                minlength: "Required length : At least 10",
                maxlength: "Required length : At most 10"
            }
        },

        showErrors: function(errorMap, errorList) {
            $("#signupForm .error-span").css('visibility', 'hidden');
            $.each(errorMap, function(key, value) {
                $('.' + key + '-error').css('visibility', 'visible');
                $('.' + key + '-error').text(value);
            });
        },

        submitHandler: function(form) {
            $('.fadeMe').show();
            $.ajax({
                type: "POST",
                url: $('#signupForm').attr('action'), // or whatever
                data: $('#signupForm').serialize(),
                success: function(data) {
                    if (data.status == 1) {
                        $('.fadeMe').hide();
                        window.location.replace('/user/verification-start/')
                    } else if (data.status == 0) {
                        $('.fadeMe').hide();
                        alert(data.msg);
                    }
                }
            });
        }
    });

    $("#loginForm").validate({

        rules: {
            emailLogIn: {
                required: true,
                email: true
            },

            passwordLogIn: {
                required: true,
            }
        },

        showErrors: function(errorMap, errorList) {
            $("#loginForm .error-span").css('visibility', 'hidden');
            $.each(errorMap, function(key, value) {
                $('.' + key + '-error').css('visibility', 'visible');
                $('.' + key + '-error').text(value);
            });
        },

        submitHandler: function(form) {
            $('.fadeMe').show();
            $.ajax({
                type: "POST",
                url: $('#loginForm').attr('action'), // or whatever
                data: $('#loginForm').serialize(),
                success: function(data) {
                    $('.fadeMe').hide();
                    if (data.status == 1) {
                        window.location.reload();
                    } else if (data.status == 0) {
                        $('.fadeMe').hide();
                        alert(data.msg);
                    }
                }
            });
        }
    });

    $("#resetForm").validate({

        rules: {
            email: {
                required: true,
                email: true
            },

        },

        showErrors: function(errorMap, errorList) {
            $("#resetForm .error-span").css('visibility', 'hidden');
            $.each(errorMap, function(key, value) {
                $('.' + key + '-error').css('visibility', 'visible');
                $('.' + key + '-error').text(value);
            });
        }

    });

    $("#changeForm").validate({

        rules: {
            new_password1: {
                required: true,
                minlength: 6
            },

            new_password2: {
                required: true,
                minlength: 6,
            }

        },

        showErrors: function(errorMap, errorList) {
            $("#changeForm .error-span").css('visibility', 'hidden');
            $.each(errorMap, function(key, value) {
                $('.' + key + '-error').css('visibility', 'visible');
                $('.' + key + '-error').text(value);
            });
        }

    });
});

function submitchangeForm() {
    $('#changeForm').submit();
}

function submitresetForm() {
    $('#resetForm').submit();
}

function submitForm() {
    $('#signupForm').submit();
}

function submitloginForm() {
    $('#loginForm').submit();
};

//function to click the signup button on pressing enter
$("#signupForm input").keyup(function(event) {
    if (event.keyCode == 13) {
        $("#signupButton").click();
    }
});

//function to click the signup button on pressing enter
$("#loginForm input").keyup(function(event) {
    if (event.keyCode == 13) {
        $("#loginButton").click();
    }
});