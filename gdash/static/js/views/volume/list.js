"use strict";

define([
    "collections/Volumes",
    "views/volume/menu"
], function (Collection, MenuView) {
    return Backbone.View.extend({
        el: "#menu",
        events: {
            "click .pure-menu-link": 'menuClicked'
        },
        initialize: function (router) {
            this.router = router;
            this.collection = new Collection();
            this.collection.on("add", this.addVolumeMenus, this);
        },
        render: function () {
            // Need to be async since need to highlight the corresponding menu
            this.collection.fetch({async: false});
        },
        addVolumeMenu: function (volume) {
            var menuView = new MenuView(volume);
            this.$el
                .find(".pure-menu .pure-menu-list")
                .append(menuView.render());
        },
        addVolumeMenus: function () {
            this.$el.find(".pure-menu .pure-menu-list").html('');
            this.collection.each(this.addVolumeMenu, this);
        },
        menuClicked: function (e) {
            e.preventDefault();
            var href = $(e.currentTarget).attr('href');
            this.router.navigate(href, true); // <- this part will pass the path to your router
        }
    });
});
