module.exports = {
    env: {
        browser: true,
    },
    root: true,
    parser: '@typescript-eslint/parser',
    plugins: [
        '@typescript-eslint',
    ],
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        "plugin:compat/recommended"
    ],
    globals: {
        GN: 'readonly',
    },
    "rules": {
        "no-cond-assign": "off",
        "semi": 2,
        "@typescript-eslint/semi": 2,
    },
    "settings": {
        "polyfills": [
            "Promise",
        ]
    }
};
