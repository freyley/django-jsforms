define([
    "requireplugins/text!templates/autocomplete_with_list_default.tmpl",
    "jqueryui"
], function(DefaultTmpl) {

console.log("it's getting loaded successfully!");


function source_override (itemlist, request, response) {
    var exclude = itemlist.item_ids(),
        term = request.term;

    console.log("exclude", exclude);
    console.log("itemlist.item_ids()", itemlist.item_ids());

    $.ajax({
        url: itemlist.url,
        data: { q: term, exclude: exclude },
        dataType: "json",
        success: response
    });
};


function delete_item(itemlist, delete_link) {
    var id = $(delete_link).closest("li").data("item_id");
    delete itemlist.items[id];
    render_list(itemlist);
};


function render_list(itemlist) {
    console.log("rendering list");
    console.log(itemlist.list_item_tmpl_id);

    itemlist.display_list.html(tmpl(
            itemlist.list_item_tmpl_id,
            {itemlist: itemlist}
    ));
};


function jqueryui_autocomplete(itemlist) {
    itemlist.select = function(event, ui) {
        itemlist.add_item_to_list(ui.item);
        itemlist.input.val("");
        return false;
    };

    var settings = {
        minLength:1,
        source: function(request, response) {
            source_override(itemlist, request, response);
        },
        select: itemlist.select
    };

    itemlist.input.autocomplete(settings);
};


function Itemlist(_, input) {
    console.group("new_autocomplete");

    // helpers
    input = $(input);
    var id = input.data("target-id");

    var that = {
        input: input,
        url: input.data("sourceurl"),
        id: input.data("target-id"),
        hidden_input: $("#" + id),
        display_list: $("#" + id + "_itemlist"),
        list_item_tmpl_id: id + "_list_item_template",
        dropdown_item_tmpl_id: id + "_dropdown_item_template",
        items: {}
    };


    // Functions
    that.add_item_to_list = function(item) {
        that.items[item.id] = item;
        that.render_list();
    };

    that.add_items_to_list = function(items) {
        $.each(items, function(_, item) {
            that.items[item.id] = item;
        });
        that.render_list();
    };

    that.render_list = function() {
        render_list(that);
    };

    that.item_ids = function() {
        var ids = [];
        $.each(that.items, function(id, _) {
            ids.push(id);
        });
        return ids;
    };

    jqueryui_autocomplete(that);

    console.groupEnd();
};



/*
        // optional settings
        if(settings.template)
            that.template = settings.template;
        else
            that.template = DefaultTmpl;

        that.display_list.on("click", "a.delete-link", function() {
            ;;; // (that, this), aka (itemlist, delete_link)
            delete_item(that, this);
            return false;
        });


        return that;
*/


$(function() {
    $.each($(".jswidget-multiselect"), Itemlist);
});


return {};

});
