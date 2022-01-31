import App from './App.svelte';
import ThreadApp from "./ThreadApp.svelte";

let app;
if (location.pathname.search(/tests$/) !== -1) {
    app = new App({
        target: document.body,
    });
} else {
    app = new ThreadApp({
        target: document.body,
    });
}


export default app;
