# Fish-in-a-Barrel Viewer Bridge (browser extension)

Scrapes the piczel.tv viewer list — including the logged-in-only **shared-IP
indicators** — from your live watch page and hands it to the Fish-in-a-Barrel
raffle app running on your machine. The app then counts only one viewer per
shared-IP group, neutralizing IP-sharing.

## How it works

1. The app runs a tiny HTTP server on `http://127.0.0.1:8422` (configurable in
   `config.ini` under `[extension] port`). A browser extension cannot listen on a
   port, so the app is the server and this extension is the client.
2. When you click **Load from site (extension)** in the app, it posts a scrape
   request for the current stream URL.
3. The **content script** on the piczel tab pings the app (via the background
   service worker) a couple times a second. When it sees a request matching its
   tab, it scrapes the viewer list (names + 2-char shared-IP group ids) and the
   background posts it back to the app.

The content script drives the loop on purpose: a Manifest V3 background service
worker is killed when idle and can't run a reliable timer, but the content script
lives as long as the tab is open and wakes the worker each ping.

If the extension doesn't answer within ~2 seconds (not installed, app not running,
or no matching tab), the app asks you to paste the viewer list manually instead.

## Loading it (unpacked)

**Chrome / Edge / Brave**
1. Go to `chrome://extensions`.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked** and select this `extension/` folder.

**Firefox**
1. Go to `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on…**.
3. Select `extension/manifest.json`. (Temporary add-ons are removed on restart.)

## Debugging

- After changing any extension file, click the **reload** icon on the extension in
  `chrome://extensions` (or re-load the temporary add-on in Firefox), then reload
  the piczel tab so the new content script runs.
- The service worker showing **"(inactive)"** is normal — it's event-driven and
  sleeps between pings. It wakes on each content-script ping; you don't need to
  keep its inspector open.
- Open the **piczel tab's** DevTools console: you should see
  `[FiaB bridge] content script active on …` on load, and
  `[FiaB bridge] scraped N viewers, submitting` when you click Load in the app. If
  you don't see the "active" line, the content script isn't injected (wrong URL —
  it only runs on `https://piczel.tv/watch/*` — or the extension needs reloading).
- In the service worker console (`chrome://extensions` → the extension →
  "service worker") you should see `scrape request for <name>` and
  `submitted N viewers`. A `submit failed` / fetch error there means the app isn't
  running or the port doesn't match `config.ini`.

## Notes

- Keep the port here (`background.js`, `BASE`) in sync with `config.ini` if you
  change it.
- The extension only touches `https://piczel.tv/watch/*` pages and your localhost
  server — nothing else.
- The manual copy/paste flow still works as a fallback and never needs the
  extension.
