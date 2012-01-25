define(
["jqueryui", "./jquery.form", "./resig_micro_templating", "./json2"],
function() {

    var form_tmpl = '<form id="<%= id %>" action="<%= action %>" style="display:none;" method="POST" enctype="multipart/form-data"><input value="<%= csrf %>" name="csrfmiddlewaretoken"><input type="file" name="timage"/></form>';
    var image_tmpl = '<img src="<%= url %>" id="<%= id %>">'

    var upload_options = {
        success: function(text, a, b, form) {
            // remove textarea tags
            text = text.substring(10,text.length-11)
            var data = JSON.parse(text),
                button = $(form.data("button")),
                hidden_id = button.data("hidden_id"),
                image_id = hidden_id + "_image_tag";

            button.html(button.data("change_image_text"));

            $("#" + image_id).remove();
            button.before(tmpl(image_tmpl, {
                url: data.thumbnail_url,
                id: image_id
            }));

            $("#" + hidden_id).val(data.id);
        }
    };


    $(function() {

        $("body").on("click", "button.jsforms-thumbnailimage", function() {
            var id = $(this).data('hidden_id'),
                form_id = id + "_form",
                form_text = tmpl(form_tmpl, {
                    id: form_id,
                    action: $(this).data('upload_url'),
                    csrf: $("input[name='csrfmiddlewaretoken']").val()
                });

            $("#" + form_id).remove();
            $("body").append(form_text);

            form = $("#" + form_id);
            var file_field = form.find("input");

            form.find("input").click();

            form.ajaxForm(upload_options);
            form.data("button", this);

            file_field.on("change", function() {
                form.submit();
            });

            return false;
        });

    });




});

