"use strict";

define(function () {
    return Backbone.Model.extend({
        urlRoot: "/api/volume/",
        getNumberOfUpBrick: function () {
            var numberOfUp = 0;
            var nodes = this.get("nodes");
            for (var idx = 0; idx < nodes.length; ++idx) {
                var node = nodes[idx];
                if (node.status) {
                    numberOfUp++;
                }
            }
            return numberOfUp;
        },
        getNumberOfDownBrick: function () {
            var numberOfDown = 0;
            var nodes = this.get("nodes");
            for (var idx = 0; idx < nodes.length; ++idx) {
                var node = nodes[idx];
                if (!node.status) {
                    numberOfDown++;
                }
            }
            return numberOfDown;
        }
    });
});
