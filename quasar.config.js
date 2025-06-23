const { configure } = require('@quasar/app-vite');

module.exports = configure(function () {
  return {
    framework: {
      config: {},
      plugins: []
    },
    build: {
      target: {
        browser: ['es2019', 'edge88', 'firefox78', 'chrome87', 'safari13.1'],
        node: 'node16'
      },
      vueRouterMode: 'hash'
    },
    devServer: {
      open: true,
      port: 3000
    }
  };
});