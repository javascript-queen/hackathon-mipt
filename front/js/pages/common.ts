import {onDomLoaded} from "../utils/on_dom_loaded";


export const main = async () => {
    console.debug('Vite OK.');

    onDomLoaded(async () => {

        // Init react root components if any are present on page
        if (document.querySelector(`[${rootComponentAttr}]`)) {
            const module = await import('../react');
            module.init();
        }

        // Init various stuff here
        // initMainBurgerMenuOpenerCloser();
    });
};

/**
 * E.g.:
 * <div data-js-root="some-react-powered-block">
 *     <div class="spinner"></div>
 * </div>
 */
export const rootComponentAttr = 'data-js-component';
