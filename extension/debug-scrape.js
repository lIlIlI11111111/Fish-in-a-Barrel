// Paste this whole file into the piczel tab's DevTools console. It opens the
// "user list" panel (the viewer list is collapsed by default), prints structural
// counts, and copies the viewer-list container HTML to the clipboard.
(async function () {
  var q = function (s) { return document.querySelectorAll(s).length; };

  // The viewer list only renders when the chat's user-list panel is expanded.
  var toggle = document.querySelector('button[title="Toggle user list"]');
  if (!q('button > b') && toggle) {
    toggle.click();
    for (var t = 0; t < 40 && !q('button > b'); t++) {
      await new Promise(function (r) { setTimeout(r, 50); });
    }
    console.log('opened user-list panel via toggle');
  } else if (!toggle) {
    console.log('could not find the "Toggle user list" button');
  }

  console.log(
    'buttons:', q('button'),
    '| button>b:', q('button > b'),
    '| b:', q('b'),
    '| shared-IP:', q('[aria-label="Shared-IP indicator"]'),
    '| iframes:', q('iframe')
  );
  document.querySelectorAll('iframe').forEach(function (f, i) {
    console.log('iframe', i, f.src);
  });
  var anchor =
    document.querySelector('[aria-label="Shared-IP indicator"]') ||
    document.querySelector('button b') ||
    Array.prototype.find.call(document.querySelectorAll('button'), function (b) {
      return b.textContent.trim();
    });
  if (anchor) {
    var n = anchor;
    for (var i = 0; i < 9 && n.parentElement && n.parentElement !== document.body; i++) {
      n = n.parentElement;
    }
    copy(n.outerHTML);
    console.log('Copied container HTML,', n.outerHTML.length, 'chars');
  } else {
    console.log('No viewer element found in the top document (likely an iframe or shadow DOM).');
  }
})();
