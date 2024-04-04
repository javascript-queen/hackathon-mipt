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
    // const provide = WG?.provide || {};

    const appInfos = [] as Array<AppInfo>;

    // find and load apps, requested in view
    const appEls: Array<HTMLElement> = Array.from(document.querySelectorAll(`[${rootComponentAttr}]`));
    for (const el of appEls) {
        const appKey = el.getAttribute(rootComponentAttr);
        const module = await import(`./components/root/${appKey}.tsx`);
        const component: FC = module.default;
        appInfos.push({el, component})
        // for (const key in provide) {
        //     app.provide(key, provide[key]);
        // }
    }

    if (!appInfos.length) {
        return;
    }

    // todo full type def ?
    // WG = {store: ...}
    // const windowStore = WG?.store || {};

    // init stores, requested in view
    // if (Object.keys(windowStore).length > 0) {
    //     const pinia = createPinia();
    //     for (const appInfo of appInfos) {
    //         appInfo.app.use(pinia);
    //     }
    //     for (const storeType in StoreList) {
    //         const data = windowStore[storeType];
    //         if (data) {
    //             StoreList[storeType]().$patch(data);
    //         }
    //     }
    // }

    // mount apps
    for (const appInfo of appInfos) {
        const appRoot = ReactDOM.createRoot(appInfo.el);
        const App = appInfo.component;
        appRoot.render(
            <React.StrictMode>
                <App />
            </React.StrictMode>,
        );

        // appInfo.app.directive('click-outside', {
        //     beforeMount: (el, binding) => {
        //         el.clickOutsideEvent = event => {
        //             if (!(el == event.target || el.contains(event.target))) {
        //                 binding.value();
        //             }
        //         };
        //         document.addEventListener("click", el.clickOutsideEvent);
        //     },
        //     unmounted: el => {
        //         document.removeEventListener("click", el.clickOutsideEvent);
        //     },
        // });
    }
}
