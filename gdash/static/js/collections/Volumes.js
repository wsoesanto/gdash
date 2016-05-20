"use strict";

define([
    "models/Volume"
], function (Model) {
    return Backbone.Collection.extend({
        model: Model,
        url: "/api/volumes"
    });
});
