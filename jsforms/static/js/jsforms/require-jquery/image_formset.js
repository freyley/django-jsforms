define(
["jqueryui", "./jquery.form", "./resig_micro_templating", "./json2"],
function() {

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
            upload_options['url'] = $(this).data('upload_url');

            var id = $(this).data('hidden_id');
            var form = $(this).data("form");

            form.ajaxSubmit(upload_options);
            form.data("button", this);

            return false;
        });

    });




});

