"use strict";

define([
    "lib/jQueryFileTree",
    "highchartsMore"
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

            var xAxisData = [];
            var yAxisData = [];
            $layouts.children().each(function () {
                xAxisData.push(
                    $(this).attr("host")
                );
                yAxisData.push({
                    low: Number($(this).attr("start")),
                    high: Number($(this).attr("end"))
                });
            });

            $("#brick-chart").highcharts({
                exporting: {
                    enabled: false
                },
                title: {
                    text: "Volume's layout"
                },
                chart: {
                    type: 'columnrange',
                    inverted: true,
                    animation: false
                },
                plotOptions: {
                    columnrange: {
                        dataLabels: {
                            enabled: true,
                            formatter: function () {
                                return "0x" + this.y.toString(16);
                            }
                        },
                        animation: false
                    }
                },
                series: [{
                    name: 'Range',
                    data: yAxisData
                }],
                xAxis: {
                    categories: xAxisData
                },
                yAxis: {
                    visible: false
                }
            });

            // var data = new google.visualization.DataTable();
            // data.addColumn("string", "Host");
            // data.addColumn("number", "Populartiy");
            // data.addColumn({type: "string", role: "tooltip"});
            // _.each(layoutsArr, function (layout) {
            //     data.addRow([layout.host, layout.end - layout.start, "Range: " + layout.start + " to " + layout.end]);
            // });
            //
            // var options = {
            //     title: "Bricks Layout"
            // };
            //
            // var chart = new google.visualization.PieChart(document.getElementById("brick-chart"));
            // chart.draw(data, options);
        }
    });
});