require.config({
    paths: {
        text: "https://cdnjs.cloudflare.com/ajax/libs/require-text/2.0.12/text.min",
        async: "https://cdnjs.cloudflare.com/ajax/libs/requirejs-plugins/1.0.3/async.min",
        propertyParser: "https://cdnjs.cloudflare.com/ajax/libs/requirejs-plugins/1.0.3/propertyParser.min",
        goog: "https://cdnjs.cloudflare.com/ajax/libs/requirejs-plugins/1.0.3/goog.min"
    }
});

require([
    // Load our app module and pass it to our definition function
    "app"
], function (App) {
    // The "app" dependency is passed in as "App"
    App.initialize();
});
