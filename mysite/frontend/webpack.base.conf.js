var path = require('path')
// 获取根目录
function resolve(dir) {
  return path.join(__dirname, '..', dir)
}

module.exports = {
  resolve: {
    alias: {
      '@': resolve('src'),
      'static': resolve(__dirname, '../static'),//增加这一行代码
    }
  }
}