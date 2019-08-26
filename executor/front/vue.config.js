const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  productionSourceMap: false,

  devServer: {
    proxy: {
      '^/api/': {
        target: 'http://localhost:8000',
        ws: true,
        changeOrigin: true
      }
    }
  },

  configureWebpack: {
    plugins: [
      new BundleAnalyzerPlugin()
    ],
    optimization: {
      splitChunks: {
        minSize: 10000,
        maxSize: 200000,
      }
    }
  },
};