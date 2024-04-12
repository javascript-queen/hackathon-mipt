import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import * as path from 'path';
import glob from 'glob';


// todo complete this for prod server
// import {viteManifestPlugin} from "./front/vite/vite_manifest_plugin";
const webManifestFile = 'conf/manifest.json';
const viteManifestFile = 'conf/static/build/manifest.json';


// where Vite-output manifest and assets dir will be actually served from
const BASE_URL = '/static/build';
// where Vite will output the manifest and assets/* (built files)
const OUT_DIR = 'gn' + BASE_URL;


// to make everything under '/front' dir importable without '/front' prefix
const alias = glob.sync(path.resolve(__dirname, './front/*')).reduce(
    (accum, val) => {
        const name = path.basename(val) ;
        accum[`/${name}/`] = `/front/${name}/` ;
        return accum;
    },
    {},
);


export default defineConfig({
    base: BASE_URL,  // base url for parent of Vite built manifest and assets dir
    build: {
        outDir: path.resolve(__dirname, OUT_DIR),  // Django-specific path
        emptyOutDir: true,  // clear output dir when building
        manifest: 'assets.json',

        // es2020 is the oldest possible target with vite
        target: 'es2020',
        rollupOptions: {
            input: [
                path.resolve(__dirname, 'front/js/main.tsx'),
                path.resolve(__dirname, 'front/css/main.scss'),
            ],
        }
    },
    plugins: [
        // todo complete this for prod server
        // viteManifestPlugin(webManifestFile, viteManifestFile, __dirname),
        react(),
    ],
    resolve: {
        alias: alias,
    },
    server: {
        hmr: {
            host: '127.0.0.1',
        },
        cors: {
            "origin": "*",
            "methods": "GET,HEAD,PUT,PATCH,POST,DELETE",
            "preflightContinue": false,
            "optionsSuccessStatus": 204,
        }
    },
});
