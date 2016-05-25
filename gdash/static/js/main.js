require.config({
    paths: {
        text: "https://cdnjs.cloudflare.com/ajax/libs/require-text/2.0.12/text.min",
        highcharts: "https://code.highcharts.com/highcharts",
        highchartsMore: "https://code.highcharts.com/highcharts-more"
    },
    shim: {
        highchartsMore: {
            deps:["highcharts"],
            exports: "HighchartsMore"
        }
    }
});

require([
    // Load our app module and pass it to our definition function
    "app"
], function (App) {
    // The "app" dependency is passed in as "App"
    App.initialize();
});
