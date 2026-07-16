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
3. This extension polls the app, and when it sees a request matching an open
   `piczel.tv/watch/<name>` tab, it scrapes that tab and posts the viewer list
   (names + 2-char shared-IP group ids) back to the app.

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

## Notes

- Keep the port here (`background.js`, `BASE`) in sync with `config.ini` if you
  change it.
- The extension only touches `https://piczel.tv/watch/*` pages and your localhost
  server — nothing else.
- The manual copy/paste flow still works as a fallback and never needs the
  extension.
