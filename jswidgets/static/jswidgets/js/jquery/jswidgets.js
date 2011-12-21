$( function() {
    $.each($('.jswidget-singleselect'), function(idx, elem) {
        $( "#" + $(elem).attr('id') ).autocomplete({
			source: $(elem).attr("data-sourceurl"),
			minLength: 2,
			select: function( event, ui ) {
                var target_id = $(elem).attr("data-target-id");
                $("#"+target_id).val(ui.item.id);
			}
		});
    });
});
