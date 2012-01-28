define([
    "./resig_micro_templating"
], function() {


function source_override (itemlist, request, response) {
    var exclude = itemlist.item_ids(),
        term = request.term;

    log("searching", { term: term, exclude: exclude });

    $.ajax({
        url: itemlist.url,
        data: { term: term, exclude: exclude },
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
    log(itemlist.list_item_tmpl_id);

    var html = "",
        ids = "";

    $.each(itemlist.items, function(_, item) {
        html += tmpl(itemlist.list_item_tmpl_id, item);
        ids += item.id + ",";
    });

    itemlist.display_list.html(html);
    itemlist.hidden_input.val(ids.substring(0, ids.length-1));

};


function override_display_item_template(itemlist) {
    itemlist.input.data("autocomplete")._renderItem = function(ul, item) {
        return $( "<li></li>" )
            .data( "item.autocomplete", item )
            .append(
                "<a>"
                + tmpl(itemlist.dropdown_item_tmpl_id, item)
                + "</a>")
            .appendTo( ul );
    };
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


var Itemlist = function(_, input) {
    // helpers
    input = $(input);
    var id = input.data("target_id");

    var that = {
        input: input,
        url: input.data("sourceurl"),
        id: input.data("target_id"),
        hidden_input: $("#" + id),
        display_list: $("#" + id + "_itemlist"),
        list_item_tmpl_id: id + "_list_item_template",
        dropdown_item_tmpl_id: id + "_dropdown_item_template",
        items: {}
    };


    // Functions
    that.add_item_to_list = function(item) {
        log("adding", item);
        that.items[item.id] = item;
        that.render_list();
        log("items", that.items);
    };

    that.render_list = function() {
        render_list(that);
    };

    that.item_ids = function() {
        var ids = [];
        $.each(that.items, function(id, val) {
            ids.push(val.id);
        });
        return ids;
    };

    jqueryui_autocomplete(that);

    // use dropdown_item template if it exists.
    if(Boolean($("#"+that.dropdown_item_tmpl_id).length))
        override_display_item_template(that);

    that.display_list.on("click", "a.jsforms-remove", function() {
        var id = $(this).closest("li").data("jsforms_item_id");
        delete that.items[id];
        render_list(that);
        return false;
    });

    // add items from existing-data
    var existing_data = that.display_list.data("existing_data");
    if(existing_data) {
        existing_data = decodeURIComponent(existing_data); // now json
        existing_data = $.parseJSON(existing_data); // now an array

        $.each(existing_data, function(_, item) {
            that.items[item.id] = item;
        });
        that.render_list();
    }

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
    $.each($(".jsforms-multiselect"), Itemlist);
});

// helper fn for console logging
function log() {
	if (!$.fn.ajaxSubmit.debug) 
		return;
	var msg = '[jquery.form] ' + Array.prototype.join.call(arguments,'');
	if (window.console && window.console.log) {
		window.console.log(msg);
	}
	else if (window.opera && window.opera.postError) {
		window.opera.postError(msg);
	}
};

return {};

});
