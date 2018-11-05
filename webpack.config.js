module.exports = {
  mode: 'development',

  output: {
    filename: 'bundle.js',
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
          presets: [['latest', { modules: false }]],
        },
      },
    ],
  },
};
