// Display settings for every page of the site: colours, size of text, typeface, spacing, column width, underlined
// links; and for the text of a book justification, paragraph style, correction marks, page numbers, the reader's place
// and the bar of buttons that appears at the top of a chapter when the reader has scrolled down. The choices are kept in this browser (localStorage) and
// nowhere else. The site works without this file: the settings button is made here, so that a reader whose
// browser does not run scripts sees no control that does nothing. Styles: site.css, "Display settings".
(function () {
  'use strict';
  var KEY = 'tb-display', PLACES = 'tb-place', KEEP = 100;
  var root = document.documentElement;
  var DEF = { theme: 'auto', font: 'serif', align: 'justify', para: 'indent', size: 1, lh: 1.6, width: 36, ls: 0, ws: 0,
              corr: 1, links: 1, pb: 0, place: 1, bar: 1 };
  var CHOICES = { theme: ['auto', 'light', 'sepia', 'dark'], font: ['serif', 'sans', 'default'],
                  align: ['justify', 'left'], para: ['indent', 'block'] };
  var STEPS = { size: [0.8, 0.9, 1, 1.1, 1.25, 1.4, 1.6, 1.8, 2], lh: [1.3, 1.45, 1.6, 1.8, 2, 2.3],
                width: [24, 30, 36, 44, 54, 66], ls: [0, 0.03, 0.06, 0.09, 0.12], ws: [0, 0.08, 0.16, 0.24, 0.32] };
  var UNIT = { size: '', lh: '', width: 'rem', ls: 'em', ws: 'em' };
  var FLAGS = ['corr', 'links', 'pb', 'place', 'bar'];
  var s = load();

  function get(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function put(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }

  // Only values from the lists above are accepted: what is stored ends up in the page's styles.
  function load() {
    var raw = {}, out = {}, k;
    try { raw = JSON.parse(get(KEY)) || {}; } catch (e) { raw = {}; }
    for (k in DEF) out[k] = DEF[k];
    for (k in CHOICES) if (CHOICES[k].indexOf(raw[k]) >= 0) out[k] = raw[k];
    for (k in STEPS) if (STEPS[k].indexOf(raw[k]) >= 0) out[k] = raw[k];
    FLAGS.forEach(function (f) { if (raw[f] === 0 || raw[f] === 1) out[f] = raw[f]; });
    if (!('pb' in raw) && get('showpb') === '1') out.pb = 1;     // the choice made before these settings existed
    return out;
  }

  function save() {
    var out = {}, k;
    for (k in DEF) if (s[k] !== DEF[k]) out[k] = s[k];
    put(KEY, JSON.stringify(out));
  }

  function attr(name, value) { if (value) root.setAttribute(name, value); else root.removeAttribute(name); }

  function apply() {
    var k;
    attr('data-theme', s.theme === 'auto' ? '' : s.theme);
    attr('data-font', s.font === DEF.font ? '' : s.font);
    attr('data-align', s.align === DEF.align ? '' : s.align);
    attr('data-para', s.para === DEF.para ? '' : s.para);
    attr('data-corr', s.corr ? '' : 'off');
    attr('data-links', s.links ? '' : 'off');
    attr('data-bar', s.bar ? '' : 'off');
    for (k in STEPS) {
      if (s[k] === DEF[k]) root.style.removeProperty('--tb-' + k);
      else root.style.setProperty('--tb-' + k, s[k] + UNIT[k]);
    }
    root.classList.toggle('showpb', !!s.pb || location.hash.indexOf('#pg-') === 0);
  }

  root.classList.add('tb-js');
  apply();                       // before the page is drawn: this file is loaded in the head, without "defer"

  // ---- the reader's place: for each book the chapter last read, and in each chapter the block at the top of the
  // window and how far down that block the window is (c: { file: [block, part] }) ----

  var where = location.pathname.match(/\/books\/([^\/]+)\/([^\/]*)$/);
  var bookId = where && where[1], file = where && (where[2] || 'index.html');
  var bar = null;     // the bar at the top of a chapter, once it exists
  // Set when the reader came here by an arrow of that bar: the chapter then opens with the bar still in view.
  var BARNAV = 'tb-bar-nav', fromBar = false;
  try { fromBar = !!file && sessionStorage.getItem(BARNAV) === file; sessionStorage.removeItem(BARNAV); } catch (e) {}

  function places() {
    var p;
    try { p = JSON.parse(get(PLACES)); } catch (e) {}
    return p && typeof p === 'object' ? p : {};
  }

  // The height that the bar covers at the top of the window (the same whether it is in view or not).
  function covered() { return bar && s.bar ? bar.offsetHeight : 0; }

  // The first block not wholly above the top of the reading area, and the part of it (0 to 1) that is above.
  function spot(article) {
    var kids = article.children, top = covered(), i, r;
    for (i = 0; i < kids.length; i++) {
      r = kids[i].getBoundingClientRect();
      if (r.bottom > top) return { i: i, o: r.height > 0 ? Math.max(0, Math.min(0.99, (top - r.top) / r.height)) : 0 };
    }
    return { i: Math.max(0, kids.length - 1), o: 0 };
  }

  function toSpot(article, at) {
    var e = article.children[at.i], r;
    if (!e) return;
    r = e.getBoundingClientRect();
    window.scrollBy(0, r.top + at.o * r.height - covered());
  }

  function savePlace(article) {
    var at = spot(article), p = places(), old = p[bookId], c = old && typeof old.c === 'object' && old.c || {}, ids;
    if (old && old.f && !(old.f in c) && old.b > 0) c[old.f] = [old.b, 0];     // a place kept before the chapters had their own
    at.o = Math.round(at.o * 100) / 100;
    if (window.pageYOffset < 2) at = { i: 0, o: 0 };
    if (at.i || at.o) c[file] = [at.i, at.o]; else delete c[file];
    p[bookId] = { f: file, b: at.i, t: Date.now(), c: c };
    ids = Object.keys(p);
    if (ids.length > KEEP) {
      ids.sort(function (a, b) { return (p[a].t || 0) - (p[b].t || 0); });
      ids.slice(0, ids.length - KEEP).forEach(function (id) { delete p[id]; });
    }
    put(PLACES, JSON.stringify(p));
  }

  function chapterPlace(article) {
    var p = places()[bookId], nav = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
    var touched = false, moved = false, timer = 0, at = null, c;
    if (p) {
      c = p.c && p.c[file];
      if (c && c.length === 2 && c[0] >= 0 && c[1] >= 0 && c[1] < 1) at = { i: Math.floor(c[0]), o: +c[1] };
      else if (p.f === file && p.b > 0) at = { i: p.b, o: 0 };
    }
    var title = false;
    if (!(s.place && at && (at.i || at.o))) {
      // No place kept in this chapter. Reached by an arrow of the bar: to just above its title, the bar still in view.
      at = fromBar && bar ? { i: 0, o: 0 } : null;
      title = !!at;
    }
    function go() {
      if (touched) return;
      toSpot(article, at);
      if (title) window.scrollBy(0, -Math.min(16, Math.max(0, article.getBoundingClientRect().top - covered() + 16)));
    }
    // Back, forward and reload are left to the browser, which returns to the place itself.
    if (at && !location.hash && (!nav || nav.type === 'navigate')) {
      ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) {
        window.addEventListener(ev, function () { touched = true; }, { passive: true, once: true });
      });
      go();
      window.addEventListener('load', go);      // again when the pictures above have taken their room
    }
    window.addEventListener('scroll', function () {
      moved = true;
      if (!s.place || timer) return;
      timer = setTimeout(function () { timer = 0; if (s.place) savePlace(article); }, 400);
    }, { passive: true });
    // Leaving the page (the next chapter, say) within that time: keep the place as it is now.
    window.addEventListener('pagehide', function () { if (s.place && moved) savePlace(article); });
  }

  function resumeLink() {
    var p = places()[bookId], h = document.getElementById('contents'), old = document.querySelector('.tb-resume'), a, para, t;
    if (old) old.parentNode.removeChild(old);
    if (!s.place || !p || !h || !/^\d+\.html$/.test(p.f)) return;
    a = document.createElement('a');
    a.href = p.f;
    t = document.querySelector('nav.toc a[href="' + p.f + '"]');
    a.textContent = 'Continue reading' + (t ? ': ' + t.textContent : '');
    para = document.createElement('p');
    para.className = 'tb-resume';
    para.appendChild(a);
    h.parentNode.insertBefore(para, h);
  }

  // ---- the settings button and its panel (every page) ----

  var LINES = { tight: 'M4 8h16M4 12h16M4 16h16', loose: 'M4 5h16M4 12h16M4 19h16',
    narrow: 'M10 5v14M14 5v14M2 12h5M5 10l2 2-2 2M22 12h-5M19 10l-2 2 2 2',
    wide: 'M3 5v14M21 5v14M11 12H6M8 10l-2 2 2 2M13 12h5M16 10l2 2-2 2',
    justify: 'M3 6h18M3 10h18M3 14h18M3 18h18', left: 'M3 6h18M3 10h12M3 14h16M3 18h9',
    indent: 'M8 4h13M3 8h18M3 12h11M8 16h13M3 20h18', block: 'M3 4h18M3 8h11M3 15h18M3 19h11',
    place: 'M7 3h10v18l-5-4-5 4z', reset: 'M4 12a8 8 0 1 0 2.6-5.9M4 4v5h5',
    more: 'M5 9l7 7 7-7', bar: 'M4 5h16v14H4zM4 9h16M7 7h.01M11 7h2M17 7h.01',
    menu: 'M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M15.6 8.4l-2.1 5.1-5.1 2.1 2.1-5.1z',
    book: 'M12 7v13M12 7C10 5.6 7 5 3 5v13c4 0 7 .6 9 2c2-1.4 5-2 9-2V5c-4 0-7 .6-9 2z',
    contents: 'M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01', prev: 'M15 5l-7 7 7 7', next: 'M9 5l7 7-7 7',
    display: 'M4 7h8M16 7h4M4 17h4M12 17h8M12 7a2 2 0 1 0 4 0a2 2 0 1 0-4 0M8 17a2 2 0 1 0 4 0a2 2 0 1 0-4 0' };
  function svg(name, cls) {
    return '<svg' + (cls ? ' class="' + cls + '"' : '') + ' viewBox="0 0 24 24" aria-hidden="true"><path d="' + LINES[name] + '"/></svg>';
  }
  function txt(cls, text, style) {
    return '<span aria-hidden="true" class="' + cls + '"' + (style ? ' style="' + style + '"' : '') + '>' + text + '</span>';
  }
  var ui = null;      // { refresh: function } once the panel exists

  function el(tag, props, html) {
    var e = document.createElement(tag), k;
    for (k in props) e.setAttribute(k, props[k]);
    if (html) e.innerHTML = html;
    return e;
  }

  function buildUI(article) {
    var header = document.querySelector('header.site');
    if (!header) return;
    var refreshers = [];
    // The same picture as in the bar of a chapter, and in the same place in the window (site.css).
    var btn = el('button', { type: 'button', 'class': 'tb-btn', 'aria-expanded': 'false', 'aria-controls': 'tb-panel',
                             'aria-label': 'Display settings', title: 'Display settings' }, svg('display'));
    header.appendChild(btn);
    var panel = el('div', { id: 'tb-panel', 'class': 'tb-panel', role: 'group', 'aria-label': 'Display settings', hidden: '' });
    var adv = el('div', { id: 'tb-adv', 'class': 'tb-adv', hidden: '' });
    var status = el('span', { 'class': 'tb-sr', role: 'status' });
    var tip = el('div', { 'class': 'tb-tip', 'aria-hidden': 'true', hidden: '' });
    var barBtn = null, opener = btn, showBar = function () {};
    var menu = null, menuBtn = null;      // the menu of the bar (the site, the book, its contents) and its button

    // A change of size, spacing or width moves the text: the reader of a chapter stays at the same words.
    function changed() {
      var at = article && window.pageYOffset > 0 ? spot(article) : null;
      apply(); save(); refresh();
      if (at) toSpot(article, at);
      showBar();
    }
    function refresh() { refreshers.forEach(function (f) { f(); }); }

    function choice(parent, key, label, options) {       // options: [value, name, picture]
      var row = el('div', { 'class': 'tb-row', role: 'radiogroup', 'aria-label': label });
      options.forEach(function (o) {
        var lab = el('label', { 'class': 'tb-opt', 'data-tip': o[1] });
        var input = el('input', { type: 'radio', name: 'tb-' + key, value: o[0], 'aria-label': o[1] });
        input.addEventListener('change', function () { s[key] = o[0]; changed(); });
        refreshers.push(function () { input.checked = s[key] === o[0]; });
        lab.appendChild(input);
        lab.insertAdjacentHTML('beforeend', o[2].indexOf('<svg') === 0 ? '<span>' + o[2] + '</span>' : o[2]);
        row.appendChild(lab);
      });
      parent.appendChild(row);
    }

    function stepper(parent, key, label, less, more, say) {       // less, more: [name, picture]
      var row = el('div', { 'class': 'tb-row', role: 'group', 'aria-label': label });
      var steps = STEPS[key], dots = el('span', { 'class': 'tb-dots', 'aria-hidden': 'true' });
      var down = el('button', { type: 'button', 'aria-label': less[0], 'data-tip': less[0] }, less[1]);
      var up = el('button', { type: 'button', 'aria-label': more[0], 'data-tip': more[0] }, more[1]);
      steps.forEach(function () { dots.appendChild(el('i')); });
      function move(by) {
        var i = steps.indexOf(s[key]) + by;
        if (i < 0 || i >= steps.length) return;
        s[key] = steps[i];
        changed();
        status.textContent = label + ': ' + (say ? say(s[key]) : (i + 1) + ' of ' + steps.length);
        if (down.disabled) up.focus(); else if (up.disabled) down.focus();     // the end of the scale: keep the keyboard's place
      }
      down.addEventListener('click', function () { move(-1); });
      up.addEventListener('click', function () { move(1); });
      refreshers.push(function () {
        var i = steps.indexOf(s[key]), k;
        down.disabled = i <= 0;
        up.disabled = i >= steps.length - 1;
        for (k = 0; k < steps.length; k++) dots.children[k].className = k === i ? 'on' : '';
      });
      row.appendChild(down); row.appendChild(dots); row.appendChild(up);
      parent.appendChild(row);
    }

    function toggle(row, key, label, picture, after) {
      var b = el('button', { type: 'button', 'aria-label': label, 'data-tip': label }, picture);
      b.addEventListener('click', function () { s[key] = s[key] ? 0 : 1; changed(); if (after) after(); });
      refreshers.push(function () { b.setAttribute('aria-pressed', s[key] ? 'true' : 'false'); });
      row.appendChild(b);
    }

    // basic
    choice(panel, 'theme', 'Colours', [
      ['auto', 'Colours: as this device is set', txt('tb-sw tb-sw-auto', '')],
      ['light', 'Colours: light', txt('tb-sw tb-sw-light', 'A')],
      ['sepia', 'Colours: sepia', txt('tb-sw tb-sw-sepia', 'A')],
      ['dark', 'Colours: dark', txt('tb-sw tb-sw-dark', 'A')]]);
    stepper(panel, 'size', 'Size of the text', ['Smaller text', txt('tb-a-small', 'A')], ['Larger text', txt('tb-a-large', 'A')],
            function (v) { return Math.round(v * 100) + '%'; });
    choice(panel, 'font', 'Typeface', [
      ['serif', 'Typeface: serif', txt('tb-f-serif', 'Aa')],
      ['sans', 'Typeface: sans serif', txt('tb-f-sans', 'Aa')],
      ['default', 'Typeface: the one set in this browser', txt('tb-f-default', 'Aa')]]);
    stepper(panel, 'lh', 'Space between lines', ['Lines closer together', svg('tight')], ['Lines further apart', svg('loose')]);
    var moreRow = el('div', { 'class': 'tb-row' });
    var more = el('button', { type: 'button', 'aria-expanded': 'false', 'aria-controls': 'tb-adv', 'aria-label': 'More settings',
                              'data-tip': 'More settings' }, svg('more'));
    more.addEventListener('click', function () {
      adv.hidden = !adv.hidden;
      more.setAttribute('aria-expanded', adv.hidden ? 'false' : 'true');
      more.firstChild.style.transform = adv.hidden ? '' : 'rotate(180deg)';
    });
    moreRow.appendChild(more);
    panel.appendChild(moreRow);

    // advanced
    stepper(adv, 'width', 'Width of the column', ['Narrower column', svg('narrow')], ['Wider column', svg('wide')]);
    var pair = el('div', { 'class': 'tb-row tb-wrap' });
    adv.appendChild(pair);
    choice(pair, 'align', 'Right-hand edge', [
      ['justify', 'Even right-hand edge (justified)', svg('justify')],
      ['left', 'Ragged right-hand edge, no hyphenation', svg('left')]]);
    choice(pair, 'para', 'Paragraphs', [
      ['indent', 'Paragraphs: first line indented', svg('indent')],
      ['block', 'Paragraphs: a space between them', svg('block')]]);
    stepper(adv, 'ls', 'Space between letters', ['Letters closer together', txt('', 'abc', 'letter-spacing:-0.03em')],
            ['Letters further apart', txt('', 'abc', 'letter-spacing:0.25em;margin-right:-0.25em')]);
    stepper(adv, 'ws', 'Space between words', ['Words closer together', txt('', 'ab cd')],
            ['Words further apart', txt('', 'ab cd', 'word-spacing:0.5em')]);
    var flags = el('div', { 'class': 'tb-row', role: 'group', 'aria-label': 'Shown or not' });
    toggle(flags, 'links', 'Underline links (all pages)', txt('tb-i-link', 'abc'));
    toggle(flags, 'corr', 'Mark corrected misprints with dots', txt('tb-i-corr', 'abc'));
    toggle(flags, 'pb', 'Show the page numbers of the printed book (each links to the scanned page)', txt('tb-i-pb', '12'));
    toggle(flags, 'place', 'Remember my place in each book', svg('place'), function () {
      if (s.place) { if (article && bookId) savePlace(article); } else try { localStorage.removeItem(PLACES); } catch (e) {}
    });
    toggle(flags, 'bar', 'Show a bar of buttons at the top of a chapter when I have scrolled down', svg('bar'));
    adv.appendChild(flags);
    var resetRow = el('div', { 'class': 'tb-row' });
    var reset = el('button', { type: 'button', 'aria-label': 'Back to the settings the site starts with',
                               'data-tip': 'Back to the settings the site starts with' }, svg('reset'));
    reset.addEventListener('click', function () {
      for (var k in DEF) s[k] = DEF[k];
      changed();
      status.textContent = 'The settings are as the site starts with.';
    });
    resetRow.appendChild(reset);
    adv.appendChild(resetRow);
    panel.appendChild(adv);
    panel.appendChild(status);
    panel.appendChild(tip);

    header.appendChild(panel);
    var old = document.querySelector('.pbtoggle');     // the checkbox for readers without the script
    if (old) old.parentNode.removeChild(old);
    refresh();

    // The bar at the top of a chapter (Tom, 2026-11-21): made here, like the button, and only where there is a text
    // to read. It comes into view when the header has gone out of it. Its links are those of the page's own pager.
    function buildBar() {
      var pager = document.querySelector('nav.pager'), inner = el('div'), mid = el('span');
      if (!article || !pager) return;
      function link(name, label, from) {
        var a = from ? el('a', { href: from.getAttribute('href'), 'aria-label': label, title: label }, svg(name))
                     : el('span', { 'class': 'tb-none', 'aria-hidden': 'true' }, svg(name));
        if (from && from.rel) {
          a.rel = from.rel;
          a.addEventListener('click', function () {
            try { sessionStorage.setItem(BARNAV, from.getAttribute('href')); } catch (e) {}
          });
        }
        return a;
      }
      function words(a) { return a ? a.textContent.replace(/^[←\s]+|[→\s]+$/g, '') : ''; }
      var prev = pager.querySelector('a[rel=prev]'), next = pager.querySelector('a[rel=next]');
      bar = el('nav', { 'class': 'tb-bar', 'aria-label': 'This book' });
      // On the left, a menu of three lines: the site, the book, its contents (Tom, 2026-11-21).
      var home = header.querySelector('.sitename a'), logo = home && home.querySelector('svg');
      var crumb = document.querySelector('.crumbs a'), toc = pager.querySelector('a:not([rel])'), ul = el('ul');
      function line(href, picture, text) {
        var li = el('li'), a = el('a', { href: href }), words = el('span');
        if (typeof picture === 'string') a.innerHTML = picture; else if (picture) a.appendChild(picture.cloneNode(true));
        words.textContent = text;
        a.appendChild(words);
        li.appendChild(a);
        ul.appendChild(li);
      }
      if (home) line(home.getAttribute('href'), logo, home.textContent);
      if (crumb) line(crumb.getAttribute('href'), svg('book', 'tb-ic'), crumb.textContent);
      if (toc) line(toc.getAttribute('href'), svg('contents', 'tb-ic'), 'Contents');
      menuBtn = el('button', { type: 'button', 'class': 'tb-nav-btn', 'aria-expanded': 'false', 'aria-controls': 'tb-menu',
                               'aria-label': 'This site and this book', title: 'This site and this book' }, svg('menu'));
      menu = el('div', { id: 'tb-menu', 'class': 'tb-menu', hidden: '' });
      menu.appendChild(ul);
      inner.appendChild(menuBtn);
      mid.appendChild(link('prev', 'Previous: ' + words(prev), prev));
      mid.appendChild(link('next', 'Next: ' + words(next), next));
      inner.appendChild(mid);
      barBtn = el('button', { type: 'button', 'class': 'tb-set-btn', 'aria-expanded': 'false', 'aria-controls': 'tb-panel', 'aria-label': 'Display settings',
                              title: 'Display settings' }, svg('display'));
      inner.appendChild(barBtn);
      inner.appendChild(menu);
      bar.appendChild(inner);
      header.parentNode.insertBefore(bar, header.nextSibling);
      root.classList.add('tb-hasbar');
      // Arriving from the picture on the book's page (#start, the chapter's heading): the browser has gone to the
      // heading before this bar existed, and Safari on the Mac and the iPad then leaves the heading half under it.
      // Put the heading just below the bar, now and again when the pictures above have taken their room, unless
      // the reader has moved in the meantime. Back, forward and reload are left to the browser.
      (function () {
        var st = location.hash === '#start' && document.getElementById('start');
        var n = window.performance && performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
        if (!st || (n && n.type !== 'navigate')) return;
        var moved = false;
        ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) {
          window.addEventListener(ev, function () { moved = true; }, { passive: true, once: true });
        });
        var place = function () {
          if (moved) return;
          var top = st.getBoundingClientRect().top - bar.offsetHeight;
          if (Math.abs(top) > 1) window.scrollBy(0, top);
        };
        place();
        window.addEventListener('load', function () { place(); setTimeout(place, 150); setTimeout(place, 600); });
      })();
      if (fromBar) {      // it was in view in the chapter just left: here it is in place at once, without sliding in
        bar.classList.add('tb-now');
        setTimeout(function () { bar.classList.remove('tb-now'); }, 500);
      }
      // In view: the reader has it switched on and the header is out of view; and as long as the panel is open in it.
      showBar = function () {
        var held = !menu.hidden || (!panel.hidden && panel.parentNode !== header);
        bar.classList.toggle('tb-on', held || (!!s.bar && header.getBoundingClientRect().bottom < 0));
      };
      window.addEventListener('scroll', showBar, { passive: true });
      window.addEventListener('resize', showBar);
      barBtn.addEventListener('click', function () { open(panel.hidden || opener !== barBtn, barBtn); });
      menuBtn.addEventListener('click', function () { openMenu(menu.hidden); });
      showBar();
    }

    function openMenu(yes) {
      var i, t;
      if (!menu || menu.hidden === !yes) return;
      if (yes) open(false);
      menu.hidden = !yes;
      menuBtn.setAttribute('aria-expanded', yes ? 'true' : 'false');
      if (yes) for (i = 0; i < menu.querySelectorAll('span').length; i++) {     // a title too long for the menu fades out
        t = menu.querySelectorAll('span')[i];
        t.classList.toggle('tb-cut', t.scrollWidth > t.clientWidth + 1);
      }
      showBar();
    }

    function open(yes, from) {
      var home = from === barBtn ? bar.firstChild : header;
      if (yes && panel.parentNode !== home) home.appendChild(panel);
      if (yes) { opener = from; openMenu(false); }
      panel.hidden = !yes;
      btn.setAttribute('aria-expanded', yes && opener === btn ? 'true' : 'false');
      if (barBtn) barBtn.setAttribute('aria-expanded', yes && opener === barBtn ? 'true' : 'false');
      tip.hidden = true;
      showBar();
    }
    btn.addEventListener('click', function () { open(panel.hidden || opener !== btn, btn); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { open(false); opener.focus(); }
      else if (e.key === 'Escape' && menu && !menu.hidden) { openMenu(false); menuBtn.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!panel.hidden && !panel.contains(e.target) && !btn.contains(e.target) && !(barBtn && barBtn.contains(e.target))) open(false);
      if (menu && !menu.hidden && !menu.contains(e.target) && !menuBtn.contains(e.target)) openMenu(false);
    });
    buildBar();

    // The names of the controls, shown beside them for a mouse or a keyboard (a touch screen has no hovering).
    function showTip(target) {
      var t = target && target.closest && target.closest('[data-tip]'), r, p, left;
      if (!t || !panel.contains(t)) { tip.hidden = true; return; }
      tip.textContent = t.getAttribute('data-tip');
      tip.style.whiteSpace = 'nowrap';
      tip.hidden = false;
      r = t.getBoundingClientRect(); p = panel.getBoundingClientRect();
      if (tip.offsetWidth > p.width - 8) tip.style.whiteSpace = 'normal';
      left = r.left - p.left + r.width / 2 - tip.offsetWidth / 2;
      left = Math.max(4, Math.min(left, p.width - tip.offsetWidth - 6));
      tip.style.left = left + 'px';
      // below the control, or above it when there is no room below inside the panel: the panel in the bar is a
      // scroll box, and Safari and Firefox cut off a tip that runs past its foot (Tom, 2026-11-23: the reset button)
      tip.style.top = (r.bottom + 4 + tip.offsetHeight > p.bottom - panel.clientTop - 2
        ? r.top - p.top + panel.scrollTop - tip.offsetHeight - 4
        : r.bottom - p.top + panel.scrollTop + 4) + 'px';
    }
    if (window.matchMedia && matchMedia('(hover: hover)').matches) {
      panel.addEventListener('mouseover', function (e) { showTip(e.target); });
      panel.addEventListener('mouseleave', function () { tip.hidden = true; });
    }
    panel.addEventListener('focusin', function (e) {
      var keyboard = false;
      try { keyboard = e.target.matches(':focus-visible'); } catch (x) {}
      if (keyboard) showTip(e.target); else tip.hidden = true;
    });
    panel.addEventListener('focusout', function () { tip.hidden = true; });

    ui = { refresh: function () { refresh(); showBar(); } };
  }

  function ready() {
    var article = document.querySelector('article.book');
    buildUI(article);
    if (article) { if (bookId) { chapterPlace(article); if (ui) ui.refresh(); } }     // the bar: in view at once if the page opened scrolled
    else if (bookId && file === 'index.html') resumeLink();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();

  // ---- the carousel of covers on the home page: a new order on every load, a row without an end, and two arrows
  // (shown only where there is a mouse: site.css). Each click moves the row on by as many books as are in view,
  // starting and stopping gently; a swipe does the same by the page's own styles. The row has no end because, each
  // time it comes to rest, books are moved from the far end of the list to the other, a whole group at a time, so
  // that the group in view stays in the middle; no book is in the page twice. The pictures are links with the
  // titles as their alt text; nothing here changes that. ----

  function carousel() {
    var box = document.querySelector('nav.carousel'), list = box && box.querySelector('ul');
    if (!list) return;
    var items = Array.prototype.slice.call(list.children), i, j, t, run = 0, moving = false, touching = false, timer = 0;
    for (i = items.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      t = items[i]; items[i] = items[j]; items[j] = t;
    }
    items.forEach(function (li) { list.appendChild(li); });
    list.scrollLeft = 0;

    // The distance from one book to the next, and the number of books in view.
    function one() {
      var a = list.children[0], b = list.children[1];
      return b ? b.getBoundingClientRect().left - a.getBoundingClientRect().left : list.clientWidth;
    }
    function inView(w) { return Math.max(1, Math.round(list.clientWidth / w)); }

    // Bring the group in view to the middle of the list by moving whole groups from one end to the other; the
    // row is shifted by the same distance in the same moment, so nothing is seen to move. Not while a reader is
    // going through the links with the keyboard: the Tab key must come to the end of the list.
    function centre() {
      var w = one(), n = inView(w), total = list.children.length, at, k, f;
      if (w <= 0 || total < 4 * n) return;
      f = document.activeElement;
      if (f && list.contains(f) && f.matches && f.matches(':focus-visible')) return;
      at = Math.round(list.scrollLeft / w);
      k = Math.round((Math.floor((total - n) / 2) - at) / n) * n;      // books to bring to the front (or, negative, to send to the back)
      if (!k) return;
      list.style.scrollSnapType = 'none';
      for (i = 0; i < Math.abs(k); i++) {
        if (k > 0) list.insertBefore(list.lastElementChild, list.firstElementChild);
        else list.appendChild(list.firstElementChild);
      }
      list.scrollLeft = (at + k) * w;
      if (!moving) list.style.scrollSnapType = '';
    }

    function rest() {
      clearTimeout(timer);
      timer = setTimeout(function () { if (!moving && !touching) centre(); }, 140);
    }

    var prev = el('button', { type: 'button', 'class': 'tb-prev', title: 'Back', 'aria-label': 'Earlier books in the row' }, svg('prev'));
    var next = el('button', { type: 'button', 'class': 'tb-next', title: 'More books', 'aria-label': 'More books' }, svg('next'));
    function move(dir) {
      var id = ++run, start = 0, DUR = 650, from, to, w, n;
      centre();
      w = one(); n = inView(w);
      from = list.scrollLeft;
      to = Math.max(0, Math.min(list.scrollWidth - list.clientWidth, (Math.round(from / (w * n)) + dir) * w * n));
      if (to === from) return;
      if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) { list.scrollLeft = to; rest(); return; }
      moving = true;
      list.style.scrollSnapType = 'none';         // or the browser pulls the row back between frames
      function frame(now) {
        if (id !== run) return;                   // another click has taken over
        if (!start) start = now;
        var p = Math.min(1, (now - start) / DUR);
        p = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;      // slow, fast, slow
        list.scrollLeft = from + (to - from) * p;
        if (p < 1) { requestAnimationFrame(frame); return; }
        moving = false;
        list.style.scrollSnapType = '';
        centre();
      }
      requestAnimationFrame(frame);
    }
    prev.addEventListener('click', function () { move(-1); });
    next.addEventListener('click', function () { move(1); });
    list.addEventListener('scroll', rest, { passive: true });
    list.addEventListener('touchstart', function () { touching = true; }, { passive: true });
    ['touchend', 'touchcancel'].forEach(function (ev) {
      list.addEventListener(ev, function () { touching = false; rest(); }, { passive: true });
    });
    window.addEventListener('resize', rest);
    box.insertBefore(prev, list);
    box.appendChild(next);
    centre();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', carousel); else carousel();

  // A change made in another tab or window reaches this one.
  window.addEventListener('storage', function (e) {
    if (e.key !== KEY && e.key !== null) return;
    s = load(); apply();
    if (ui) ui.refresh();
  });
  // A page brought back by the Back button is shown as it was left: bring it up to date.
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    s = load(); apply();
    if (ui) ui.refresh();
    if (bookId && file === 'index.html' && !document.querySelector('article.book')) resumeLink();
  });
})();
