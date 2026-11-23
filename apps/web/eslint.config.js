import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ["**/*.{ts,tsx}"],
    languageOptions: { ecmaVersion: 2022, globals: globals.browser },
    plugins: { "react-hooks": reactHooks, "react-refresh": reactRefresh },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "react-refresh/only-export-components": ["warn", { allowConstantExport: true }],
      "no-restricted-syntax": [
        "error",
        {
          selector: "JSXAttribute[name.name='style']",
          message: "No inline styles. Use Tailwind classes or a class from src/styles.",
        },
        {
          selector: "JSXAttribute[name.name='dangerouslySetInnerHTML']",
          message: "Do not render raw HTML.",
        },
      ],
      "no-restricted-globals": [
        "error",
        { name: "fetch", message: "Call the API through src/lib/apiClient.ts." },
      ],
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["@/features/*/*"],
              message: "Import a feature through its index.ts, never its internal files.",
            },
          ],
        },
      ],
    },
  },
  {
    // The one HTTP client is the only place allowed to call fetch.
    files: ["src/lib/apiClient.ts"],
    rules: { "no-restricted-globals": "off" },
  },
);
