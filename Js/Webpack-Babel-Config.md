## Webpack-Babel-Config


``Webpack`` is modular manager for js. ``Babel`` is transcompiler for ES+.<br>
These two library can join!<br>
We should check 3 files. ``package.json`` ``webpack.config.js`` ``.babelrc``

```json
{
  "author": "sangmoon",
  "license": "ISC",
  "devDependencies": {
    "babel-core": "^6.26.0",
    "babel-loader": "^7.1.2",
    "babel-plugin-transform-async-to-generator": "^6.24.1",
    "babel-polyfill": "^6.26.0",
    "babel-preset-es2015": "^6.24.1",
    "webpack": "^3.10.0",
    "webpack-dev-server": "^2.11.1"
  },
  "babel": {
    "presets": [
      "es2015"
    ]
  }
}
```

```json
var path = require('path');

module.exports = {
  //....
  module:{
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        loader: 'babel-loader',
        
      }
    ]   
  },

  resolve: {
    modules:['node_modules'],
    extensions: ['.js', '.json', '.css']
  },

  devServer: {
    port: 8000
  },
  // 애플리케이션의타겟 환경
  target: 'web'

};
```

```json
{
  "presets": ["es2015"],
  "plugins": ["transform-async-to-generator"]
}
```

Through this setting, you can use webpack-babel collaboration!