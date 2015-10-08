$(document).ready(function() {
    if ($(".restaurant-listings .demo-card-square").length) {

    } else {
        $(".restaurant-listings").append('\
					<div class="row text-center pretty-text center-block">\
						<span class="sorry-text">\
							Sorry. All restaurants are closed for delivery at the moment. Pre-ordering coming soon!!\
						</span>\
					</div>');
    }
})