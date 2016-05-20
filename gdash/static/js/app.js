"use strict";

define([
    "views/layout",
    "views/volume/detail"
], function (LayoutView, DetailView) {
    var AppRouter = Backbone.Router.extend({
        routes: {
            "volume/:volumeName": 'getDetail'
        },
        getDetail: function (volumeName) {
            var volumeDetailView = new DetailView(volumeName);
            volumeDetailView.render();
        }
    });

    var appRouter = new AppRouter();
    var layoutView = new LayoutView(appRouter);
    layoutView.render();

    var initialize = function () {
        Backbone.history.start({
            pushState: true,
            root: "/"
        });
    };
    return {
        initialize: initialize
    };
});
