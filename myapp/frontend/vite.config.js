// vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [
    react(),
    {
      name: "fix-base-path",
      transformIndexHtml(code) {
        return code.replaceAll(
          "https://_to_be_replaced_",
          "qrc:///myapp/frontend/dist/"
        );
      },
    },
  ],
  base: "https://_to_be_replaced_",
});
