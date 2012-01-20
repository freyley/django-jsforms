define(
["jqueryui"],
function() {

var init_image_formset = function(ifs) {
    console.log("initing", ifs);

    // button event
    ifs.find("button").click(function() {
        var html = ifs.find("script.jswidgets-imageformset-newform").html();
        $(html).dialog();
        console.log("hi");
        return false;

    });

};




    $(function() {
        $.each($("div.jswidgets-imageformset"), function(_, ifs) {
            init_image_formset($(ifs));
        });
    });

});

