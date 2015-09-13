//show the input address fields in the modal


var toggle = 1;
var csrftoken;

//script for creating a new address in the address modal
function submitAddress(country, target_url, csrf_token) {

    if (toggle == 1) {

        $("#inputAddress").slideDown("slow");
        $("#addAddress").children("paper-material").text("Save Address");
        toggle = 0;
    } else {
        var address = $("#address_label").val();
        var city = $("#city_label").val();
        var postcode = $("#postcode_label").val();
        console.log(postcode);
        if (address !== '' && city !== '' && postcode !== '') {
            var data = {}
            data['street_address'] = address;
            data['city'] = city;
            data['postcode'] = String(postcode);
            data['country'] = country;
            data['csrfmiddlewaretoken'] = csrf_token;
            console.log("about to post data");
            $.post(

                target_url,
                data,
                function(response) {
                    //the object was saved in the database
                    if (response.status == 1) {

                        $("#inputAddress").hide();
                        //add a panel
                        //change the properties back to the add address button
                        $("#addAddress").children('paper-material').text('Add an address');
                        $("#addressButton > paper-material").text(address);
                        toggle = 1;
                        $("#address_label").val("");
                        $("#city_label").val("");
                        $("#postcode_label").val("");
                        $("#deliveryAddressModal").modal('hide');

                    } else {
                        alert('Could not save address');
                    }

                }

            )
        }
    }

}

// make a get call to get the the addresses

function getAddresses(delivery_info, target_url, csrf_token) {
    csrftoken = csrf_token;
    $('#defaultAddress').prop('disabled', true);
    $("#panels").children().remove();

    $.get(
        target_url,
        function(data) {

            for (var i = 0; i < data.user_addresses.length; i++) {
                $("#panels").last().append("<div class='row vcenter'><div class='col-md-11'><div class='panel panel-default address'><div class='panel-body text-center'></div></div></div><div class='col-md-1'><i class='material-icons delete-address'>delete</i></div></div>");
                $("#panels").children().last().find(".panel-body").text(data.user_addresses[i].street_address);
                $("#panels").children().last().find(".panel-body").attr('id', String(data.user_addresses[i].id));
                $("#panels").children().last().find("i").attr('onclick', "deleteAddress(this)");
                if (data.user_addresses[i].default === true) {
                    $("#panels").children().last().find(".panel-default").addClass("mdl-shadow--4dp");
                }
            };


        }
    )

    $("#deliveryAddressModal").modal('show');
}

//function to save the default address
function setDefaultAddress(target_url, csrf_token) {
    var id = $("#panels .mdl-shadow--4dp > .panel-body").attr('id');
    $.post(
        target_url, {
            'address_id': id,
            'csrfmiddlewaretoken': csrf_token
        },
        function(data) {
            if (data.status === 1) {
                $("#addressButton > paper-material").text(data.street_address);
                $("#deliveryAddressModal").modal('hide');
                $('#defaultAddress').prop('disabled', true);
            } else {
                alert("Address could not be used, Try again");
            }
        }

    )

}

//function to delete the address
function deleteAddress(element) {

    var choice = confirm("Are you sure you want to delete this address ?")

    if (choice == true) {
        var id = $(element).parent().siblings().find('.panel-body').attr('id');
        $.post(
            '/user/delete_address/', {
                'address_id': id,
                'csrfmiddlewaretoken': csrftoken
            },
            function(data) {
                if (data.status === 1) {
                    $(element).parent().parent().remove();
                    $('#defaultAddress').prop('disabled', true);
                } else if (data.status === 2) { //default address deleted
                    $(element).parent().parent().remove();
                    $("#" + data.default_id).parent().addClass('mdl-shadow--4dp');
                    $("#addressButton > paper-material").text($("#" + data.default_id).text());
                    $('#defaultAddress').prop('disabled', true);
                } else if (data.status === 3) {
                    $(element).parent().parent().remove();
                    $("#addressButton > paper-material").text('Add an address');
                    $('#defaultAddress').prop('disabled', true);
                } else {
                    alert("Address could not be deleted");
                }
            }

        )
    }
}

//function to add radio button functionality to the various addresses
var selectDefault = $("#panels").on("click", "*", function() {
    $(this).closest(".address").addClass("mdl-shadow--4dp").parent().parent().siblings().find(".panel").removeClass("mdl-shadow--4dp");
    $('#defaultAddress').prop('disabled', false);
});

$(document).ready(selectDefault);

//script for adding to the cart
$('.add_to_cart').click(function() {
    var $id = $(this).attr("name");
    $.get("add/" + $id, function(data, status) {
        alert("Data: " + data + "\nStatus: " + status);
        $('#payButton').attr("value", data);
    });
});