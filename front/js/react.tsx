// Здесь стартуем React
import React from 'react';
import type {FC} from 'react';
import ReactDOM from 'react-dom/client';
import {rootComponentAttr} from "./pages/common";


interface AppInfo {
    el: HTMLElement,
    component: FC;
}

export async function init(): Promise<void> {
    const appInfos = [] as Array<AppInfo>;

    // find and load apps, requested in view
    const appEls: Array<HTMLElement> = Array.from(document.querySelectorAll(`[${rootComponentAttr}]`));
    for (const el of appEls) {
        const appKey = el.getAttribute(rootComponentAttr);
        const module = await import(`./components/root/${appKey}.tsx`);
        const component: FC = module.default;
        appInfos.push({el, component})
    }

    if (!appInfos.length) {
        return;
    }

    // mount apps
    for (const appInfo of appInfos) {
        const appRoot = ReactDOM.createRoot(appInfo.el);
        const App = appInfo.component;
        appRoot.render(
            <React.StrictMode>
                <App />
            </React.StrictMode>,
        );
    }
}
