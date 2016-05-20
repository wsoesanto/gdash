"use strict";

define([
    "models/Volume",
    "text!templates/volume/detail.html",
    "views/brick/layout"
], function (Volume, detailTemplate, BrickLayoutView) {
    return Backbone.View.extend({
        el: "#main",
        initialize: function (volumeName) {
            this.volumeName = volumeName;
            // Highlight the Volume menu
            $(".pure-menu-item").removeClass("pure-menu-selected");
            $("#" + volumeName).addClass("pure-menu-selected");
            this.volume = new Volume({id: volumeName});
            this.volume.on("change", this.renderDetail, this);
        },
        render: function () {
            this.volume.fetch();
        },
        renderDetail: function () {
            var compiledTemplate = _.template(detailTemplate)({
                model: this.volume
            });
            this.$el.html(compiledTemplate);
            // Render the brick layout
            var brickLayoutView = new BrickLayoutView(this.volumeName);
            brickLayoutView.render();
            var volumeName = this.volumeName;
            $("#volume-start-button").click(function (e) {
                $.get("/api/volume/" + volumeName + "/start", function() {
                    location.reload();
                });
                e.preventDefault();
            });
        }
    });
});
