const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const clean = require('clean-webpack-plugin');

module.exports = [{
  mode: 'development',
  watch: true,
  entry: './sources/index.js',
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'webapp/static/webapp/js')
  },
  devServer: {
    contentBase: path.join(__dirname, 'webapp/templates/design'),
    compress: true,
    writeToDisk: true,
    port: 9000
  },
  module: {
    rules: [{
      test: /\.css$/,
      use: ['style-loader', 'css-loader']
    }, {
      test: /\.js$/,
      loaders: ['babel-loader']
    }, {
      test: /\.s[ac]ss$/i,
      use: [
        // fallback to style-loader in development
        MiniCssExtractPlugin.loader,
        'css-loader',
        'sass-loader'
      ]
    }, {
      test: /\.(eot|svg|ttf|woff|woff2)$/i,
      loader: "file-loader",
      options: {
        name: '../fonts/[name].[ext]',
      }
    }, {
      test: /\.(png|jpe?g|gif|ico)$/i,
      loader: 'file-loader',
      options: {
        name: '../img/[name].[ext]',
      }
    }]
  },
  plugins: [
    new clean.CleanWebpackPlugin({
      root: path.join(__dirname, 'webapp/static/webapp'),
      verbose: true
    }),
    new MiniCssExtractPlugin({
      filename: '../css/[name].bundle.css',
      allChunks: true
    }),
    new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        moment: 'moment'
    })
  ]
}];