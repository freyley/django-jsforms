define([], function() {


    var set_up_formsetfield = function(template_tag) {
        var data = {};
        data.template_text = $(template_tag).html();
        data.name = $(template_tag).data("name");
        data.total_forms = 0;
        data.forms = [];

        $.each($(".jsforms-formsetfield-form-" + data.name), function(_, form) {
            var f = $(form);
            set_up_form_events(f, data);
            data.total_forms += 1;
            data.forms.push(f);
        });

        update_management_form(data);

        $("a.jsforms-formsetfield-addform-" + data.name).click(function() {
            var form = $(data.template_text.replace(/__prefix__/g, data.total_forms));
            data.forms.push(form);
            set_up_form_events(form, data);
            $(this).before(form);

            data.total_forms += 1;
            update_management_form(data);

            return false;
        });
    };


    var update_management_form = function(data) {
        $("#id_jsforms-" + data.name + "-TOTAL_FORMS").val(data.total_forms);
    };


    var decrement_form = function(form, num, data) {
        var old_num = num + 1,
            old_str = "jsforms-" + data.name + "-" + old_num + "-",
            new_str = "jsforms-" + data.name + "-" + num + "-";

        $.each(form.find("*"), function(_, elem) {
            var e = $(elem);
            $.each(["for", "id", "name"], function(_, attr) {
                if(e.prop(attr))
                    e.prop(attr, e.prop(attr).replace(old_str, new_str));
            });

            $.each(e.data(), function(key, val) {
                if(typeof val === "string")
                    e.data(key, val.replace(old_str, new_str));
            });
        });
    };


    var delete_form = function(form, data) {
        console.log("delete", form, data);
        var index = $.inArray(form, data.forms);
        var id_field = form.find("#id_jsforms-" + data.name + "-" + index + "-id");

        if(id_field.val() == "") {
            // form was created on this page
            data.forms.splice(index, 1);
            form.remove();

            for(var i=index; i<data.forms.length; i++) {
                var f = data.forms[i];
                decrement_form(f, i, data);
            }

            data.total_forms = data.forms.length;
            update_management_form(data);
        } else {
            // form is bound
            form.find("#id_jsforms-" + data.name + "-" + index + "-DELETE").prop("checked", true);
            form.hide();
        }
    };


    var set_up_form_events = function(form, data) {
        console.log("setting up form", form);
        var link = $('<a href="#" class="jsforms-formsetfield-delete">delete</a>');
        form.find("label[for$='DELETE']").hide();
        form.find("*[id$='DELETE']").hide().after(link);
        link.click(function() {
            delete_form(form, data);
            return false;
        });
    };


    $(function() {
        $.each($("script.jsforms-formsetfield-template"), function(_, fsft) {
            set_up_formsetfield(fsft);
        });
    });

});
