// Content script: scrapes the piczel.tv viewer list on demand.
//
// The page is a React SPA with obfuscated CSS-module class names, so we key off
// stable structural landmarks instead of classes:
//   - a viewer is a <button> whose direct child is a <b> holding the username,
//   - a shared-IP badge is a descendant <button aria-label="Shared-IP indicator">
//     whose text is the 2-char group id (e.g. "5B"),
//   - the "Banned" section is excluded so banned users never enter the raffle.

const api = globalThis.browser ?? globalThis.chrome;

// Collect the container(s) of any "Banned" section so we can skip those users.
// The section's collapsible header is a <button> whose text starts with "Banned"
// and which holds an svg chevron; the banned users live in that button's parent
// container (alongside the header). We match only the header <button> itself — a
// broader match would also hit ancestor elements (the svg is their descendant too)
// and wrongly exclude the whole list.
function bannedRoots() {
  const roots = [];
  for (const el of document.querySelectorAll("button")) {
    const text = (el.textContent || "").trim();
    if (/^Banned\b/.test(text) && el.querySelector("svg")) {
      if (el.parentElement) roots.push(el.parentElement);
    }
  }
  return roots;
}

function isInBanned(node, roots) {
  return roots.some((root) => root.contains(node));
}

function scrapeViewers() {
  const banned = bannedRoots();
  const viewers = [];
  const seen = new Set();

  for (const b of document.querySelectorAll("button > b")) {
    const button = b.parentElement;
    if (!button || button.tagName !== "BUTTON") continue;
    if (isInBanned(button, banned)) continue;

    const name = (b.textContent || "").trim();
    if (!name || seen.has(name)) continue;
    seen.add(name);

    const badge = button.querySelector('button[aria-label="Shared-IP indicator"]');
    const group = badge ? (badge.textContent || "").trim() || null : null;

    viewers.push({ name, group });
  }

  return viewers;
}

// The viewer list only exists in the DOM while the chat's "user list" panel is
// expanded (it's collapsed by default). The list entries are the only `button > b`
// on the page, so their presence is our "panel is open" signal.
function userListOpen() {
  return document.querySelector("button > b") !== null;
}

function userListToggle() {
  return document.querySelector('button[title="Toggle user list"]');
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Open the user-list panel if needed, scrape, then restore the panel to how we
// found it (only closing it again if we were the ones who opened it).
async function ensureUserListAndScrape() {
  const toggle = userListToggle();
  let opened = false;
  if (!userListOpen() && toggle) {
    toggle.click();
    opened = true;
    for (let i = 0; i < 40 && !userListOpen(); i++) await wait(50); // up to ~2s for render
  }
  const viewers = scrapeViewers();
  if (opened && toggle) toggle.click(); // leave the streamer's UI as we found it
  return viewers;
}

// The content script lives as long as the piczel tab is open, so it drives the
// loop and acts as a heartbeat that wakes the (idle-prone) service worker. Every
// tick it asks the background whether the app has a pending scrape request for
// this page; if so, it opens+scrapes the user list and hands it back to be POSTed.
const POLL_MS = 500;

function tick() {
  api.runtime.sendMessage({ type: "poll", url: location.href }, async (resp) => {
    if (api.runtime.lastError) return; // worker restarting; retry next tick
    if (resp && resp.scrape) {
      const viewers = await ensureUserListAndScrape();
      console.log("[FiaB bridge] scraped", viewers.length, "viewers, submitting");
      api.runtime.sendMessage({ type: "submit", url: location.href, viewers });
    }
  });
}

setInterval(tick, POLL_MS);
console.log("[FiaB bridge] content script active on", location.href);
