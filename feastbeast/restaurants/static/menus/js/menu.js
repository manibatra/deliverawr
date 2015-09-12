//show the input address fields in the modal


var toggle = 1;

//script for creating a new address in the address modal
function submitAddress(country, target_url, csrf_token) {

    if (toggle == 1) {

        $("#inputAddress").slideDown("slow");
        $("#addAddress").children("paper-material").text("Save Address");
        toggle = 0;
    } else {
        var address = $("#address_label").val();
        var city = $("#city_label").val();
        var postcode = $("postcode_label").val();
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
                        $("#panels").last().append("<div class='panel panel-default'><div class='panel-body text-center'></div></div>");
                        $("#panels").children().last().children().text(address);

                        $("#inputAddress").hide();
                        //add a panel
                        //change the properties back to the add address button
                        $("#addAddress").children('paper-material').text('Add an address');
                        toggle = 1;

                    } else {
                        alert('Could not save address');
                    }

                }

            )
        }
    }

}

// make a get call to get the the addresses

function getAddresses(delivery_info, target_url) {
    if (delivery_info === 'true') {
        $.get(
            target_url,
            function(data) {

                for (var i = 0; i < data.user_addresses.length; i++) {
                    $("#panels").last().append("<div class='panel panel-default'><div class='panel-body text-center'></div></div>");
                    $("#panels").children().last().children().text(data.user_addresses[i].street_address);
                    $("#panels").children().last().children().attr('id', String(data.user_addresses[i].id));
                };


            }
        )
    };

    $("#deliveryAddressModal").modal('show');
}

//script for adding to the cart
$('.add_to_cart').click(function() {
    var $id = $(this).attr("name");
    $.get("add/" + $id, function(data, status) {
        alert("Data: " + data + "\nStatus: " + status);
        $('#payButton').attr("value", data);
    });
});