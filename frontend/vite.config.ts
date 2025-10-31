import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: true, // allow access from Docker network
    watch: {
      usePolling: true, // force polling mode (needed in Docker)
      interval: 100, // check every 100ms
    }
  },
});
