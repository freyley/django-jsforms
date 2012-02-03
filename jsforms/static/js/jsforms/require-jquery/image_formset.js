define(
["jqueryui", "./jquery.form", "./resig_micro_templating", "./json2"],
function() {

    var image_tmpl = '<img src="<%= url %>" id="<%= id %>">'


    var success_callback = function(data, a, b, form) {
        var button = $(form.data("button")),
            hidden_id = button.data("hidden_id"),
            image_id = hidden_id + "_image_tag";

        button.html(button.data("change_image_text"));

        $("#" + image_id).remove();
        button.before(tmpl(image_tmpl, {
            url: data.thumbnail_url,
            id: image_id
        }));

        $("#" + hidden_id).val(data.id);
    };


    $(function() {

        $("body").on("click", "button.jsforms-thumbnailimage", function() {
            var button = $(this);
            var upload_options = {
                url: $(this).data('upload_url'),
                success: function(text, b, c, form) {

                    // remove textarea tags
                    text = text.substring(10,text.length-11);
                    var data = JSON.parse(text);

                    var fn = button.data("success_callback");
                    if(fn)
                        fn(data, b, c, form);
                    else
                        success_callback(data, b, c, form);
                }
            }

            var id = $(this).data('hidden_id');
            var form = $(this).data("form");

            form.ajaxSubmit(upload_options);
            form.data("button", this);

            return false;
        });

    });




});

