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

api.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "scrapeViewers") {
    sendResponse({ url: location.href, viewers: scrapeViewers() });
  }
  return true;
});
