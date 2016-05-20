"use strict";

var gulp = require('gulp');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');
var path = require('path');

var sassPath = path.join('sass', '**', '*.scss');
var staticCssPath = path.join('static', 'css');

gulp.task('default', ['sass:watch']);

gulp.task('sass', function () {
    return gulp.src(sassPath)
        .pipe(sass().on('error', sass.logError))
        .pipe(cleanCSS())
        .pipe(gulp.dest(staticCssPath));
});

gulp.task('sass:watch', function () {
    gulp.watch(sassPath, ['sass']);
});
