var path = require('path');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var rootAssetPath = './brigade/static';

module.exports = {
  entry: {
    application: rootAssetPath + '/js/application.js',
    style: rootAssetPath + '/css/style.css',
  },

  output: {
    path: path.resolve('./brigade/build/public'),
    publicPath: 'http://localhost:5000/assets/',
    filename: '[name].[chunkhash].js',
    chunkFilename: '[id].[chunkhash].js'
  },

  resolve: {
    extensions: ['.js', '.css']
  },

  module: {
    rules: [
      {
        test: /\.js$/i,
        use: 'script-loader',
        exclude: /node_modules/
      },
      {
        test: /\.css$/i,
        use: ExtractTextPlugin.extract({ use: 'css-loader' }),
      },
      {
        test: /\.(jpe?g|png|gif|txt|svg([\?]?.*))$/i,
        loaders: [
          'file-loader?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]',
          // 'image-loader?bypassOnDebug&optimizationLevel=7&interlaced=false'
        ]
      },
    ]
  },

  plugins: [
    new ExtractTextPlugin('[name].[chunkhash].css'),
    new ManifestRevisionPlugin(path.join('brigade', 'build', 'manifest.json'), {
      rootAssetPath: rootAssetPath,
      ignorePaths: ['pdf/'],
      extensionsRegex: /\.js/,
    })
  ]
};
