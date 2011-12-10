define( [], function() {
    // we're assuming jquery and jqueryUI exist - they could be loaded.

    function create_singleselect(elem) {
        $(elem).autocomplete({
            source: $(elem).attr("data-sourceurl"),
            minLength: 2,
            select: function( event, ui ) {
                var target_id = $(elem).attr("data-target-id");
                $("#"+target_id).val(ui.item.id);
            }
        });
    };


    $(function() {
        console.log("setting up the stuff");

        $.each($('.ajax_widget_singleselect'), function(_, elem) {
            create_singleselect(elem);
        });

    });




    return {
        create_singleselect: create_singleselect
    };

});
