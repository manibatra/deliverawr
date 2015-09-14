//show the input address fields in the modal


var toggle = 1;
var configured = 0;
var add_handler;
// using jQuery to get the csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


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

//function to retreive the cards of the customer, TODO : remove the class address from  the panel, add  a waiting symbol
$("#paymentMethodsButton").on('click', function() {
    $('#defaultCard').prop('disabled', true);
    $("#cardPanels").children().remove();

    $.get(
        "/payments/get-cards/",
        function(data) {

            if (data.status === 1) {
                for (var i = 0; i < data.user_payment_methods.length; i++) {
                    $("#cardPanels").last().append("<div class='row vcenter'><div class='col-md-11'><div class='panel panel-default address'><div class='panel-body text-center'></div></div></div><div class='col-md-1'><i class='material-icons delete-address'>delete</i></div></div>");
                    $("#cardPanels").children().last().find(".panel-body").text(data.user_payment_methods[i].brand + " : " + data.user_payment_methods[i].last);
                    $("#cardPanels").children().last().find(".panel-body").attr('id', data.user_payment_methods[i].card_id);
                    $("#cardPanels").children().last().find("i").attr('onclick', "deleteCard(this)");
                    if (data.user_payment_methods[i].card_id === data.default) {
                        $("#cardPanels").children().last().find(".panel-default").addClass("mdl-shadow--4dp");
                    }
                };
            }

            $("#paymentInfoModal").modal('show');
        }
    )

});

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
var selectDefault = $("#panels, #cardPanels").on("click", "*", function() {
    $(this).closest(".address").addClass("mdl-shadow--4dp").parent().parent().siblings().find(".panel").removeClass("mdl-shadow--4dp");
    $('#defaultAddress').prop('disabled', false);
    $('#defaultCard').prop('disabled', false);
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

/////////Stripe related requests

function addCard(stripe_id, mail, image_url) {
    var add_handler = StripeCheckout.configure({
        key: 'pk_test_ZyFNgoOGTLmMjJKaFZ1MwuqD',
        image: image_url,
        locale: 'auto',
        //shippingAddress: true,
        panelLabel: 'Add card',
        token: function(token, args) {
            // Use the token to create the charge with a server-side script.
            // You can access the token ID with `token.id`
            var data = {}
            data['csrfmiddlewaretoken'] = csrftoken;
            data['stripeToken'] = token.id;
            data['stripe_id'] = stripe_id;
            $.post(
                '/payments/add-card/',
                data,
                function(data) {
                    if (data.status == 1) {
                        $("#cardPanels").last().append("<div class='row vcenter'><div class='col-md-11'><div class='panel panel-default address'><div class='panel-body text-center'></div></div></div><div class='col-md-1'><i class='material-icons delete-address'>delete</i></div></div>");
                        $("#cardPanels").children().last().find(".panel-body").text(data.brand + " : " + data.last);
                        $("#cardPanels").children().last().find(".panel-body").attr('id', data.card_id);
                        $("#cardPanels").children().last().find("i").attr('onclick', "deleteCard(this)");
                        setDefaultCard(stripe_id, data.brand, data.last, data.card_id);
                    }
                }
            );
        }
    });



    add_handler.open({
        email: mail,
        name: 'Feast Beast',
        description: 'Add the card',
    });

    //Close Checkout on page navigation
    $(window).on('popstate', function() {
        add_handler.close();
    });
}

//function to set the default card
function setDefaultCard(stripe_id, brand, last, card_id) {
    $.post(
        '/payments/make-default/', {
            'stripe_id': stripe_id,
            'card_id': card_id,
            'csrfmiddlewaretoken': csrftoken
        },
        function(data) {
            if (data.status == 1) {
                $("#ppaymentMethodsButton > paper-material").text(brand + " : " + last);
                $("#paymentMethodsButton").attr('id', card_id);
                $("#paymentInfoModal").modal('hide');
            }
        }

    );

}