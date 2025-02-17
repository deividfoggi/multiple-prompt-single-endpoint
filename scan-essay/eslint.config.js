import { FlatCompat } from '@eslint/eslintrc';
import js from '@eslint/js';
import typescriptPlugin from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';

const compat = new FlatCompat({
  baseDirectory: import.meta.url,
});

export default [
  js.configs.recommended,
  ...compat.extends('plugin:@typescript-eslint/recommended'),
  {
    files: ['**/*.ts', '**/*.tsx', '**/*.js'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        ecmaVersion: 2021,
        sourceType: 'module',
      },
      globals: {
        process: 'readonly',
        console: 'readonly',
        module: 'readonly',
        __dirname: 'readonly',
        error: 'readonly',
        res: 'readonly',
        req: 'readonly',
      },
    },
    rules: {
      "prefer-const": "warn",
      "no-constant-binary-expression": "error",
      "constructor-super": "error",
      "no-const-assign": "error",
      "no-this-before-super": "error",
      "no-undef": "error",
      "no-unreachable": "error",
      "no-unused-vars": "warn",
      "no-use-before-define": "error"
    },
    plugins: {
      '@typescript-eslint': typescriptPlugin,
    }
  },
];