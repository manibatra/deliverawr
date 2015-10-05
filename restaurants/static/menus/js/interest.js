//function ot submit the interest form
$('#rawrButton').on('click', function() {
    $('#interestForm').submit();
});

//checking the validity of the interest page
$(document).ready(function() {
    $("#interestForm").validate({

        rules: {
            busName: {
                required: true,
                rangelength: [2, 30]
            },

            email: {
                email: true
            },

            address: {
                required: true,
            },

            phoneNo: {
                required: true,
                digits: true,
                minlength: 10,
                maxlength: 10
            }
        },

        showErrors: function(errorMap, errorList) {
            $("#interestForm .error-span").css('visibility', 'hidden');
            $.each(errorMap, function(key, value) {
                $('.' + key + '-error').css('visibility', 'visible');
                $('.' + key + '-error').text(value);
            });
        }
    });

});