define(
["jqueryui", "./jquery.form", "./resig_micro_templating", "./json2"],
function() {

    var form_tmpl = '<form id="<%= id %>" action="<%= action %>" style="display:none;" method="POST" enctype="multipart/form-data"><input type="file" name="timage"/></form>';

    var upload_options = {
        success: function(text) {
            // remove textarea tags
            text = text.substring(10,text.length-11)
            var data = JSON.parse(text);
            console.log(data);
        }
    };


    $(function() {

        $("body").on("click", "button.jswidgets-thumbnailimage", function() {
            var id = $(this).data('hidden_id'),
                form_id = id + "_form",
                form_text = tmpl(form_tmpl, {
                    id: form_id,
                    action: $(this).data('upload_url')
                });

            $("#" + form_id).remove();
            $("body").append(form_text);

            form = $("#" + form_id);
            var file_field = form.find("input");

            form.find("input").click();

            form.ajaxForm(upload_options);

            file_field.on("change", function() {
                form.submit();
            });

            return false;
        });

    });




});

