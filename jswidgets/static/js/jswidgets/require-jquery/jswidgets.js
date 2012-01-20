define([
        "./multi_model_select", 
        "./formset_field", 
        "./image_formset", 
        ], function(MMS, FSF, IF) {
    // we're assuming jquery and jqueryUI exist - they SHOULD be loaded.


    // TODO - put this in single_select.js
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


    // TODO - put this in div_opener.js
    function create_divopener(elem) {
        var id = $(elem).data("opens");
        $("#"+id).hide();
        $(elem).click(function() {
            $("#"+id).show();
            return false;
        });
    };


    $(function() {
        $.each($('.jswidgets-singleselect'), function(_, elem) {
            create_singleselect(elem);
        });
        $.each($('.jswidgets-opener'), function(_, elem) {
            create_divopener(elem);
        });
    });

    // TODO - does this help anything?
    return {
        create_singleselect: create_singleselect
    };

});
