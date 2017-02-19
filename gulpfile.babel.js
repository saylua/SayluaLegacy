import gulp from 'gulp';
import sass from 'gulp-sass';
import gutil from 'gulp-util';
import watch from 'gulp-watch';
import concat from 'gulp-concat';
import cleanCSS from 'gulp-clean-css';
import sourcemaps from 'gulp-sourcemaps';

import glob from 'glob';
import stream from 'stream';
import webpack from 'webpack';

import webpackConfig from './webpack.config.js';
import tempConfig from './temporary.config.js';

const paths = tempConfig.paths;
const dests = tempConfig.dests;

gulp.task('build-sass', () => {
  // Compile our initial, root level styles
  let rootGlob = "saylua/static-source/scss/**/*.scss";

  gulp.src(rootGlob)
    .pipe(sass())
    .on('error', sass.logError)
    .pipe(concat('styles.min.css'))
    .pipe(sourcemaps.init())
    .pipe(cleanCSS())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dests.sass));

  // Compile our module SCSS into separate payloads.
  let moduleGlob = "saylua/modules/*/";
  let moduleFolders = glob.sync(moduleGlob);

  moduleFolders.map((folder) => {
    let moduleFilesGlob = folder + "/static-source/scss/**/*.scss";
    let moduleFiles = glob.sync(moduleFilesGlob);

    let packageName = folder.split("/").splice(-2)[0];

    let outputName = packageName + '.min.css';
    let outputPath = "saylua/modules/" + packageName + "/static/css/";

    gulp.src(moduleFilesGlob)
      .pipe(sass({
        'includePaths': "saylua/static-source/scss/"
      })
      .on('error', sass.logError))
      .pipe(concat(outputName))
      .pipe(sourcemaps.init())
      .pipe(cleanCSS())
      .pipe(sourcemaps.write())
      .pipe(gulp.dest(outputPath));
  });
});


gulp.task('build-js', ['build-es']);
gulp.task('build-es6', ['build-es']);
gulp.task('build-es', [], function() {
  // Create a local copy of the config.
  let config = webpackConfig;

  process.env.NODE_ENV = process.env.NODE_ENV || "production";
  const DEVELOPMENT = (process.env.NODE_ENV === "development");

  // Set our webpack environs
  config['plugins'].push(
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
    })
  );


  // Set additional dev options
  if (DEVELOPMENT) {
    config['devtool'] = 'inline-source-map';
    config.watch = true;
  } else {
    // Minify output in production.
    config['plugins'].push(
      new webpack.optimize.UglifyJsPlugin({
        "compress": {
          "warnings": false
        }
      })
    );
  }

  // Pre-configure compiler, stream.
  let compiler = webpack(webpackConfig);
  let _stream = new stream.Stream();

  // Build info config
  let statsConfig = {
    "assetsSort": "name",
    "colors": true,
    "chunks": false,
    "chunkModules": false
  };

  // Determine whether or not to 'watch'
  if (DEVELOPMENT) {
    compiler.watch({}, (err, stats) => {
      statsConfig.assets = false;
      gutil.log(stats.toString(statsConfig));
    });
  } else {
    compiler.run((err, stats) => {
      if (err || stats.hasErrors()) {
        gutil.log(err);
        _stream.emit('end');
      } else {
        gutil.log(stats.toString(statsConfig));
      }
    });

    return _stream;
  }
});


// Build everything. Check under every stone. Leave no survivors.
gulp.task('build', ['build-es', 'build-sass']);


// Rerun the task when a file changes
gulp.task('watch', () => {
  process.env.NODE_ENV = "development";

  // Special treatment for sass files.
  const reportChange = (vinyl) => {
    let event = vinyl.event;
    event = event[0].toUpperCase() + event.slice(1);

    process.stdout.write("\x1b[33m[Watching]\x1b[0m " + event + ": " + vinyl.path + "\n");
  };

  watch([paths.sass + "/**/*"], { 'usePolling': true }, (vinyl) => {
    reportChange(vinyl);
    gulp.start('build-sass');
  });


  // Watch is automatically determined by using the node-env in `build-es`, so we can continue as usual.
  watch([paths.es6 + "/**/*"], { 'usePolling': true }, (vinyl) => {
    reportChange(vinyl);
  });
  gulp.start('build-es');


  // Print the paths we're watching, because we're nice.
  let _paths = Object.keys(paths).map(key => paths[key]);
  process.stdout.write(`\nWatching:`);
  process.stdout.write(`\n========================\n`);
  process.stdout.write(`${ _paths.join('\n') }\n\n`);


  // Purely for aesthetic reasons.
  // Prevents the "Finished" line from printing.
  return new stream.Stream();
});


// The default task (called when you run `gulp` from cli)
gulp.task('default', ['build']);