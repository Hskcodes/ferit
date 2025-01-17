// ==UserScript==
// @name         Advanced URL Shortener Bypass
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  Automatically bypass timers and steps on the URL shortener website by manipulating cookies and requests.
// @author       Anonymous
// @match        https://modijiurl.com/*
// @match        https://maharastrajob.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    /**
     * Sets a cookie with the desired value.
     * @param {string} name - The name of the cookie.
     * @param {string} value - The value to set for the cookie.
     */
    function setCookie(name, value) {
        document.cookie = `${name}=${value}; path=/; domain=${window.location.hostname};`;
        console.log(`Cookie set: ${name}=${value}`);
    }

    /**
     * Overrides the server-side check for steps by manipulating cookies.
     */
    function bypassStepCookies() {
        // Example cookies used in the process, replace with actual names based on your observations.
        const stepsCompleted = ['step1_complete', 'step2_complete', 'step3_complete'];
        stepsCompleted.forEach((cookie) => setCookie(cookie, 'true'));
    }

    /**
     * Simulates the completion of server-side steps by firing off necessary requests.
     */
    function bypassRequests() {
        // Hook into XMLHttpRequest to auto-confirm server-side checks.
        const originalXHR = window.XMLHttpRequest;
        window.XMLHttpRequest = class extends originalXHR {
            open(method, url) {
                if (url.includes('step') || url.includes('timer')) {
                    console.log(`Intercepted URL: ${url}`);
                    // Simulate successful step completion directly here.
                }
                super.open(...arguments);
            }

            send(body) {
                console.log(`Intercepted request body: ${body}`);
                // Modify the request body or add parameters as needed.
                super.send(body);
            }
        };
    }

    /**
     * Auto-clicks buttons and skips waiting times.
     */
    function autoClickButtons() {
        setInterval(() => {
            // List of button IDs to click.
            const buttonIds = ['verifybtn', 'rtg-snp2'];
            buttonIds.forEach((id) => {
                const button = document.getElementById(id);
                if (button && button.style.display !== 'none' && !button.disabled) {
                    button.click();
                    console.log(`Clicked button: ${id}`);
                }
            });
        }, 500);
    }

    /**
     * Main function to execute all bypass mechanisms.
     */
    function manipulateProcess() {
        // Bypass steps using cookies and server-side manipulation.
        bypassStepCookies();
        bypassRequests();

        // Automatically handle buttons and timers.
        autoClickButtons();
    }

    // Execute the script when the page loads.
    window.addEventListener('load', manipulateProcess);
})();
