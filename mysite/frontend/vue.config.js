module.exports = {
  assetsDir: 'static',
  runtimeCompiler: true,
  configureWebpack: {
    devtool: 'source-map'
  },
  transpileDependencies: [
    'vue-echarts',
    'resize-detector'
  ]
}