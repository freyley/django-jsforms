define([], function() {


    var set_up_formsetfield = function(template_tag) {
        var data = {};
        data.template_text = $(template_tag).html();
        data.name = $(template_tag).data("name");
        data.total_forms = 0;
        data.forms = [];

        $.each($(".jswidgets-formsetfield-form-" + data.name), function(_, form) {
            var f = $(form);
            set_up_form_events(f, data);
            data.total_forms += 1;
            data.forms.push(f);
        });

        update_management_form(data);

        $("a.jswidgets-formsetfield-addform-" + data.name).click(function() {
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
        $("#id_jswidgets-" + data.name + "-TOTAL_FORMS").val(data.total_forms);
    };


    var decrement_form = function(form, num, data) {
        var old_num = num + 1,
            old_str = "jswidgets-" + data.name + "-" + old_num + "-",
            new_str = "jswidgets-" + data.name + "-" + num + "-";

        console.log(old_str, new_str);
        $.each(form.find("*"), function(_, elem) {
            var e = $(elem);
            if(e.prop("for"))
                e.prop("for", e.prop("for").replace(old_str, new_str));
            if(e.prop("id"))
                e.prop("id", e.prop("id").replace(old_str, new_str));
            if(e.prop("name"))
                e.prop("name", e.prop("name").replace(old_str, new_str));
        });
    };


    var delete_form = function(form, data) {
        console.log("delete", form, data);
        var index = $.inArray(form, data.forms);
        var id_field = form.find("#id_jswidgets-book_formats-" + index + "-id");

        if(id_field.val() == "") {
            // form was created on this page
            data.forms.splice(index, 1);
            form.remove();

            for(var i=index; i<data.forms.length; i++) {
                var f = data.forms[i];
                decrement_form(f, i, data);
            }


/*
            var total = 0;
            $.each($(".jswidgets-formsetfield-form-" + data.name), function(_, f) {
                renumber_form(f, total, data);
                total += 1;
            });
            data.total_forms = total;
            */
            update_management_form(data);

        } else {
            // form is bound
            console.log("todo");
        }
    };


    var set_up_form_events = function(form, data) {
        console.log("setting up form", form);
        var link = $('<a href="#" class="jswidgets-formsetfield-delete">delete</a>');
        form.find("label[for$='DELETE']").hide();
        form.find("*[id$='DELETE']").hide().after(link);
        link.click(function() {
            delete_form(form, data);
            return false;
        });
    };


    $(function() {
        $.each($("script.jswidgets-formsetfield-template"), function(_, fsft) {
            set_up_formsetfield(fsft);
        });
    });

});
