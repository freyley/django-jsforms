define(
["jqueryui", "./jquery.form"],
function() {



var upload_options = {
    dataType: "json",
    type: "post",
    clearForm: true,
    success: function(json, x, y, form) {
        console.log("i done gots stuff from the server", this.arguments);

    }
};








    $(function() {
        var temp_form = $('<form id="jswidgets-image-uploader" style="display:none;" method="POST" enctype="multipart/form-data"><input type="file" name="timage"/></form>');
        $("body").append(temp_form);
        var uploader_form = $("#jswidgets-image-uploader");
        var file_field = uploader_form.find("input");

        $("body").on("click", "button.jswidgets-thumbnailimage", function() {
            var id = $(this).data('hidden_id');
            uploader_form.find("input").click();

            file_field.off("change");
            file_field.on("change", function() {
                console.log("a file has been selected");
                console.log("upload temp_form now using the ajaxForm");
            });

            return false;
        });

    });




});

