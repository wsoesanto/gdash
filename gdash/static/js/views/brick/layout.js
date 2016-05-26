"use strict";

define([
  "text!templates/brick/dir-tree.html",
  "highchartsMore"
], function(dirTreeTemplate) {
  return Backbone.View.extend({
    el: "#directory-tree",
    dirTreeTemplate: _.template(dirTreeTemplate),
    initialize: function(volumeName) {
      this.volumeName = volumeName;
    },
    render: function() {
      this.$el.html("Unable to get file tree information");

      var _this = this;
      $.ajax({
        url: "/api/volume/" + this.volumeName + "/bricks/range",
        type: 'GET'
      }).done(function(data) {
        var $content = _this.renderDirTree("root", data, _this);
        _this.$el.html($content);
        _this.$el.delegate("li a", "click", _this.renderGraph);
      });
    },
    renderDirTree: function(name, dirLayout, _this) {
      var content = _this.dirTreeTemplate({
        name: name,
        layouts: dirLayout.layouts
      });
      var $content = $(content);
      var $subfoldersContent = $();
      _.each(dirLayout.subfolders, function(subfolderLayout, subfolderName) {
        $subfoldersContent = $subfoldersContent.add(_this.renderDirTree(subfolderName, subfolderLayout, _this));
      });
      $content.find(".directory").append($subfoldersContent);
      return $content;
    },
    renderGraph: function(event) {
      var $el = $(event.target);
      var $layouts = $el.next();

      var xAxisData = [];
      var yAxisData = [];
      $layouts.children().each(function() {
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
              formatter: function() {
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
    }
  });
});