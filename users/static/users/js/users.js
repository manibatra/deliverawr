$('#rawrButton').on('click', function() {
    $('#driverinterestForm').submit();
});

//checking the validity of the interest page
$(document).ready(function() {
    $("#driverinterestForm").validate({

        rules: {
            Name: {
                required: true,
                rangelength: [2, 30]
            },

            email: {
                email: true
            },

            city: {
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
            $("#driverinterestForm .error-span").css('visibility', 'hidden');
            $.each(errorMap, function(key, value) {
                $('.' + key + '-error').css('visibility', 'visible');
                $('.' + key + '-error').text(value);
            });
        }
    });

});