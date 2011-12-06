$( function() {
    $.each($('.ajax_widget_singleselect'), function(idx, elem) {
        console.log(elem);
        $( "#" + $(elem).attr('id') ).autocomplete({
			source: $(elem).attr("data-sourceurl"),
			minLength: 2,
			select: function( event, ui ) {
				log( ui.item ?
					"Selected: " + ui.item.value + " aka " + ui.item.id :
					"Nothing selected, input was " + this.value );
			}
		});
        console.log("id: " + $(elem).attr('id'));
    });
});