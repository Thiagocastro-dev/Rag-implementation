import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import { quasar, transformAssetUrls } from '@quasar/vite-plugin';
import path from 'path';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const host = env.HOST || '0.0.0.0';
  const port = parseInt(env.PORT, 10) || 3000;

  return {
    plugins: [
      vue({
        template: { transformAssetUrls }
      }),
      quasar()
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },
    server: {
      host: host,
      port: port,
      open: true
    }
  };
});