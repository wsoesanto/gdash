"use strict";

define([
    "lib/jQueryFileTree",
    "async",
    "propertyParser",
    "goog!visualization,1,packages:[corechart,geochart]"
], function () {
    return Backbone.View.extend({
        el: "#directory-tree",
        initialize: function (volumeName) {
            this.volumeName = volumeName;
        },
        render: function () {
            this.$el.fileTree({
                root: "/",
                script: "/volume/" + this.volumeName + "/bricks/range/dir-tree"
            }, this.renderPie);
        },
        renderPie: function (event) {
            var $el = $(event.target);
            var $layouts = $el.next();
            var layoutsArr = [];
            $layouts.children().each(function () {
                var layout = {
                    host: $(this).attr("host"),
                    start: $(this).attr("start"),
                    end: $(this).attr("end")
                };
                layoutsArr.push(layout);
            });

            var data = new google.visualization.DataTable();
            data.addColumn("string", "Host");
            data.addColumn("number", "Populartiy");
            data.addColumn({type: "string", role: "tooltip"});
            _.each(layoutsArr, function (layout) {
                data.addRow([layout.host, layout.end - layout.start, "Range: " + layout.start + " to " + layout.end]);
            });

            var options = {
                title: "Bricks Layout"
            };

            var chart = new google.visualization.PieChart(document.getElementById("brick-chart"));
            chart.draw(data, options);
        }
    });
});