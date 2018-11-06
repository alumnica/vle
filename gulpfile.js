const { series } = require('gulp');
const { parallel } = require('gulp');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const autoprefixer = require('gulp-autoprefixer');
const browser = require('browser-sync').create();
const panini = require('panini');
const webpack = require('webpack');
const webpackStream = require('webpack-stream');
const named = require('vinyl-named');
const rimraf = require('rimraf');

// -----------
// File locations
// -----------

const sassPaths = [
  'node_modules/foundation-sites/scss',
  'node_modules/motion-ui/src',
  'node_modules/@fortawesome/fontawesome-free/scss',  
  'node_modules/fullpage.js/dist',  
];

// Delete the "dist" folder
// This happens every time a build starts
function clean(done) {
  rimraf('front_end/dist', done);  
}


// Sass //
function styles(done) {
  return gulp
      .src('front_end/assets/scss/app.scss')
      //sourcemaps
      .pipe(sourcemaps.init({ largeFile: true }))
      // Use sass with the files found, and log any errors
      .pipe(
        sass({
          includePaths: sassPaths,
          outputStyle: 'expanded',
        }).on('error', sass.logError)
      )
      .pipe(
        autoprefixer({
          browsers: [
            'last 2 versions',
            'ie >= 9',
            'android >= 4.4',
            'ios >= 7',
          ],
        })
      )
      .pipe(sourcemaps.write())
      // desitnation of compile files (styleguide and static)
      .pipe(gulp.dest('front_end/dist/assets/css'))      
      .pipe(browser.stream());
  done();
}

// Copy files out of the assets folder
// This task skips over the "img", "js", and "scss" folders, which are parsed separately
function copy() {
  return gulp.src(['front_end/assets/**/*', '!front_end/assets/{js,scss,html}{,/**/*}'])
    .pipe(gulp.dest('front_end/dist/assets'));  
}

// Start a server with BrowserSync to preview the site in
function server(done) {
  browser.init({
    server: {
      baseDir: 'front_end/dist/',
    },
  });
  done();
}

// Reload the browser with BrowserSync
function reload(done) {
  browser.reload();
  done();
}



// Copy page templates into finished HTML files
function pages() {
  var htmlRoot = './assets/html/',
    out = './styleguide/';

  return gulp
    .src('front_end/assets/html/pages/**/*.html')
    .pipe(
      panini({
        root: 'front_end/assets/html/pages/',
        layouts: 'front_end/assets/html/layouts/',
        partials: 'front_end/assets/html/partials/',
        data: 'front_end/assets/html/data/',
        helpers: 'front_end/assets/html/helpers/',
      })
    )
    .pipe(gulp.dest('front_end/dist/'));
}

// Load updated HTML templates and partials into Panini
function resetPages(done) {
  panini.refresh();
  done();
}

// Javascrip bundle
function js(done) {
  gulp
    .src('front_end/assets/js/app.js')
    .pipe(named())
    .pipe(webpackStream(require('./webpack.config.js', webpack)))
    .pipe(gulp.dest('front_end/dist/assets/js'))
  done();
}


// reload JS Parts change of JS
function jsparts(done) {
  return gulp
    .src('front_end/assets/js/parts/**/*.js')
    .pipe(gulp.dest('front_end/dist/assets/js/parts'))
  done();
}


// Watch gulp functions.
function watch() {
  gulp.watch('front_end/assets/scss/**/*.scss').on('all', styles);
  gulp
    .watch('front_end/assets/html/pages/**/*.html')
    .on('all', gulp.series(pages, reload));
  gulp
    .watch('front_end/assets/html/{layouts,partials}/**/*.html')
    .on('all', gulp.series(resetPages, pages, reload));
  gulp.watch('front_end/assets/js/*.js').on('all', gulp.series(js, reload));
  gulp.watch('front_end/assets/js/parts/**/*.js').on('all', gulp.series(jsparts, reload));
}


// Build the 'dist' folder by runnin everything below


exports.build = series(clean, parallel(styles, pages, js, jsparts, copy));
exports.default = series(clean, parallel(styles, pages, js, jsparts, copy), server, watch)

exports.clean = clean;
exports.copy = copy;