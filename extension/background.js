// Background service worker: bridges the Fish-in-a-Barrel app and piczel.tv.
//
// The app hosts a localhost HTTP server (the extension can't listen on a port),
// so we poll GET /request. When the app has an active scrape request whose stream
// matches an open piczel watch tab, we ask that tab's content script to scrape
// the viewer list and POST it back to /viewers. Doing the localhost fetch here in
// the background (with host_permissions) avoids page-CSP / CORS problems.

const api = globalThis.browser ?? globalThis.chrome;

const BASE = "http://127.0.0.1:8422";
const POLL_MS = 500;

// Last streamer slug we already fulfilled, so we don't re-scrape repeatedly for
// the same request while it stays active.
let lastHandled = null;

function slug(url) {
  try {
    return url.trim().replace(/\/+$/, "").split("/").pop().trim().toLowerCase();
  } catch (e) {
    return "";
  }
}

async function findWatchTab(wantSlug) {
  const tabs = await api.tabs.query({ url: "https://piczel.tv/watch/*" });
  return tabs.find((t) => slug(t.url) === wantSlug) || null;
}

function scrapeTab(tabId) {
  return new Promise((resolve) => {
    api.tabs.sendMessage(tabId, { type: "scrapeViewers" }, (resp) => {
      if (api.runtime.lastError) resolve(null);
      else resolve(resp || null);
    });
  });
}

async function poll() {
  try {
    const res = await fetch(`${BASE}/request`, { cache: "no-store" });
    const req = await res.json();

    if (!req.active) {
      lastHandled = null;
      return;
    }

    const wantSlug = slug(req.url);
    if (wantSlug === lastHandled) return; // already handled this active request

    const tab = await findWatchTab(wantSlug);
    if (!tab) return; // no matching open piczel tab; keep polling

    const scraped = await scrapeTab(tab.id);
    if (!scraped) return;

    await fetch(`${BASE}/viewers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: scraped.url, viewers: scraped.viewers }),
    });
    lastHandled = wantSlug;
  } catch (e) {
    // App not running / server unreachable — stay quiet and keep polling.
  }
}

setInterval(poll, POLL_MS);
