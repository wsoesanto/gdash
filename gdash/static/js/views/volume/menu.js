"use strict";

define([
    "text!templates/volume/menu.html"
], function (menuTemplate) {
    return Backbone.View.extend({
        initialize: function (model) {
            this.model = model;
        },
        render: function () {
            return _.template(menuTemplate)({
                model: this.model
            });
        }
    });
});
