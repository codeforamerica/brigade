var path = require('path');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');

var rootAssetPath = './brigade/static';

var publicPath = process.env.ASSET_PATH || '/assets/';

module.exports = {
  entry: {
    application: rootAssetPath + '/js/application.js',
    style: rootAssetPath + '/scss/style.scss',
  },

  output: {
    path: path.resolve('./brigade/build/public'),
    filename: '[name].[chunkhash].js',
    chunkFilename: '[id].[chunkhash].js',
    publicPath: publicPath
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
        test: /\.s?css$/i,
        use: ExtractTextPlugin.extract({
          use: [
            {
              loader: 'css-loader'
            },
            {
              loader: 'sass-loader',
              options: {
                includePaths: require("bourbon-neat").includePaths
              }
            }
          ]
        }),
      },
      {
        test: /\.(jpe?g|png|gif|txt|ico|eot|woff|ttf|otf|svg([\?]?.*))$/i,
        loaders: [
          'file-loader?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]',
          // 'image-loader?bypassOnDebug&optimizationLevel=7&interlaced=false'
        ]
      },
      {
        test: /\.pdf$/i,
        loaders: [
          'file-loader?context=' + rootAssetPath + '&name=[path][name].[ext]',
        ]
      }
    ]
  },

  plugins: [
    new ExtractTextPlugin('[name].[contenthash].css'),
    new CopyWebpackPlugin([
      'brigade/static/robots.txt'
    ]),
    new ManifestRevisionPlugin(path.join('brigade', 'build', 'manifest.json'), {
      rootAssetPath: rootAssetPath,
      extensionsRegex: /\.js/,
    })
  ]
};
