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
      $("#client-button").click(this.readClientLayout(this));
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
        _this.$el.delegate("li a", "click", _this.renderGraph($("#brick-chart")));
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
    renderGraph: function($chart) {
      return function(event) {
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

        $chart.highcharts({
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
      };
    },
    readClientLayout: function(_this) {
      return function() {
        var layoutData = {
          layouts: {},
          subfolders: {}
        };
        var layoutText = $("#client-layout").val();
        _.each(layoutText.split('\n'), function(dirLayoutsText) {
          if (dirLayoutsText === "") {
            return;
          }
          _.each(dirLayoutsText.split(' '), function(dirLayoutText) {
            var dirLayoutArr = dirLayoutText.split(',');
            var dirsArr = dirLayoutArr[0].split('/');
            var dirLayout = layoutData;
            _.each(dirsArr, function(dirname) {
              if (dirname === "") {
                return;
              }
              if (_.isUndefined(dirLayout.subfolders[dirname])) {
                dirLayout.subfolders[dirname] = {
                  layouts: {},
                  subfolders: {}
                };
              }
              dirLayout = dirLayout.subfolders[dirname];
            });
            var layouts = dirLayout.layouts;
            layouts[dirLayoutArr[4] + ":" + dirLayoutArr[5]] = {
              start: Number(dirLayoutArr[2]),
              end: Number(dirLayoutArr[3])
            };
          });
        });
        var $content = _this.renderDirTree("root", layoutData, _this);
        var $clientTree = $("#client-directory-tree");
        $clientTree.html($content);
        $clientTree.delegate("li a", "click", _this.renderGraph($("#client-brick-chart")));
      };
    }
  });
});
