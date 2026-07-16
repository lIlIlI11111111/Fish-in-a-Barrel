// Background service worker: performs the localhost network calls for the bridge.
//
// In Manifest V3 the service worker is event-driven and gets killed when idle, so
// it can't run its own poll loop. Instead the persistent content script pings us
// every tick (which also wakes us if we were asleep); we check the app's pending
// request and, when it matches the pinging tab, tell the content script to scrape,
// then POST the scraped viewers to the app. Keeping the fetch here (extension
// origin) avoids the page's upgrade-insecure-requests CSP.

const api = globalThis.browser ?? globalThis.chrome;

const BASE = "http://127.0.0.1:8422";

// Streamer slug we've already fulfilled for the current active request, so we
// scrape once per request rather than every 500ms tick.
let lastHandled = null;

function slug(url) {
  try {
    return url.trim().replace(/\/+$/, "").split("/").pop().trim().toLowerCase();
  } catch (e) {
    return "";
  }
}

api.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (!msg) return;

  if (msg.type === "poll") {
    const pageSlug = slug((sender.tab && sender.tab.url) || msg.url || "");
    fetch(`${BASE}/request`, { cache: "no-store" })
      .then((r) => r.json())
      .then((req) => {
        if (!req.active) {
          lastHandled = null;
          sendResponse({ scrape: false });
          return;
        }
        const want = slug(req.url);
        if (want && want === pageSlug && want !== lastHandled) {
          lastHandled = want; // fulfil this request once
          console.log("[FiaB bridge] scrape request for", want);
          sendResponse({ scrape: true });
        } else {
          sendResponse({ scrape: false });
        }
      })
      .catch(() => sendResponse({ scrape: false })); // app not running / unreachable
    return true; // keep the message channel open for the async sendResponse
  }

  if (msg.type === "submit") {
    fetch(`${BASE}/viewers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: msg.url, viewers: msg.viewers }),
    })
      .then(() => console.log("[FiaB bridge] submitted", (msg.viewers || []).length, "viewers"))
      .catch((e) => console.log("[FiaB bridge] submit failed:", e));
    return; // no response expected
  }
});
