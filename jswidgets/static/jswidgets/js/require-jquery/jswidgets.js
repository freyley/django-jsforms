define( [], function() {
    // we're assuming jquery and jqueryUI exist - they could be loaded.

    function create_singleselect(elem) {
        $(elem).autocomplete({
            source: $(elem).data("sourceurl"),
            minLength: 2,
            select: function( event, ui ) {
                var target_id = $(elem).data("target-id");
                $("#"+target_id).val(ui.item.id);
            }
        });

    };
    function create_divopener(elem) {
        var id = $(elem).data("opens");
        $("#"+id).hide();
        $(elem).click(function() {
            $("#"+id).show();
            return false;
        });
    };


    $(function() {
        console.log("setting up the stuff");

        $.each($('.jswidget-singleselect'), function(_, elem) {
            create_singleselect(elem);
        });
        $.each($('.jswidgets-opener'), function(_, elem) {
            create_divopener(elem);
        });

    });




    return {
        create_singleselect: create_singleselect
    };

});
