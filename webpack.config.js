module.exports = {
  mode: 'development',

  output: {
    filename: 'app.js',
  },

  resolve: {
    alias: {
      jquery: 'jquery/src/jquery',
    },
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules)/,
        loader: 'babel-loader',
        query: {
          presets: ['@babel/preset-env'],
        },
      },
    ],
  },
};
