"use strict";

define([
    "models/VolumeInfo"
], function (Model) {
    return Backbone.Collection.extend({
        model: Model,
        url: "/api/volumes/info"
    });
});
