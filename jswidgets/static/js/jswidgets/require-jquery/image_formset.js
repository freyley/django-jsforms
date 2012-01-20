define(
["jqueryui", "./jquery.form"],
function() {





var upload_options = {
    dataType: "json",
    type: "post",
    clearForm: true,
    beforeSubmit: function(formData, form){
        var caption_valid = false;
        var image_valid = false;
        $.each(formData, function(k,v) {
            if(v.name=="image" && v.value!="")
                image_valid = true;
            if(v.name=="caption" && v.value!="")
                caption_valid = true;
        });

        if(!image_valid || !caption_valid) {
            var message = "";
            if(!image_valid)
                message += "Select an image to upload.\n";
            if(!caption_valid)
                message += "Please give your image a caption.\n";
            alert(message);
            return false;
        }

        var entry_id = form.closest(".image-editor").attr("class").split(" ")[1];
        form.find('input#id_entry_id').val(entry_id);
        form.find('a.cancel-image-form').click();
    },
    success: function(json, x, y, form) {
        console.log("i done gots stuff from the server", this.arguments);

    }
};









    var init_image_formset = function(ifs) {
        console.log("initing", ifs);

        // button event
        ifs.find("button").click(function() {
            var html = ifs.find("script.jswidgets-imageformset-newform").html();
            var form = $(html).dialog();

            form.on("submit", function() {
                // TODO - don't post fields other than the image file
            
                form.ajaxForm(upload_options);
                $.post(form.prop("action"), form.serialize());
                console.log("gotcha");
                return false;
            });

            return false;
        });

    };





    $(function() {
        $.each($("div.jswidgets-imageformset"), function(_, ifs) {
            init_image_formset($(ifs));
        });
    });




});

