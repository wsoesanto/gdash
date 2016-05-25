"use strict";

define([
  "text!templates/volume/layout.html",
  "views/volume/list"
], function(layoutTemplate, ListView) {
  return Backbone.View.extend({
    el: $("#main-container"),
    initialize: function(router) {
      this.router = router;
    },
    render: function() {
      this.$el.append(_.template(layoutTemplate));
      this.listView = new ListView(this.router);
      this.listView.render();

      $("#menuLink").click(this.showMenu);
    },
    showMenu: function() {
      var activeClass = "active";
      $("#layout").toggleClass(activeClass);
      $("#menu").toggleClass(activeClass);
      $("#menuLink").toggleClass(activeClass);
    }
  });
});
