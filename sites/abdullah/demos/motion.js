/* Shared motion for the demo sites: headline word reveal, staggered hero entrance,
   scroll-driven reveals, scroll progress bar and magnetic buttons. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;
  var accent = getComputedStyle(document.documentElement).getPropertyValue('--ag-accent').trim() || '#c9a86a';

  var css = [
    '.mo-w{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.1em;margin-bottom:-.1em}',
    '.mo-w>span{display:inline-block;animation:moRise 1.1s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,0s)}',
    '@keyframes moRise{from{transform:translateY(110%)}to{transform:none}}',
    '.mo-enter{animation:moUp 1.1s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,.4s)}',
    '@keyframes moUp{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}',
    '.mo-bar{position:fixed;top:0;left:0;right:0;height:2px;z-index:70;background:' + accent + ';transform-origin:left;transform:scaleX(0)}',
    '.btn{transition:transform .5s cubic-bezier(.16,1,.3,1),box-shadow .4s ease!important}',
    '@supports (animation-timeline: view()){',
    '.mo-reveal{animation:moReveal linear both;animation-timeline:view();animation-range:entry 0% entry 60%}',
    '.mo-bar{animation:moGrow linear both;animation-timeline:scroll(root)}',
    '.mo-par{animation:moPar linear both;animation-timeline:scroll(root);animation-range:0 100vh}',
    '}',
    '@keyframes moReveal{from{opacity:0;translate:0 56px;filter:blur(6px)}to{opacity:1;translate:0 0;filter:none}}',
    '@keyframes moGrow{to{transform:scaleX(1)}}',
    '@keyframes moPar{to{translate:0 18%;opacity:.35}}'
  ].join('');
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  var bar = document.createElement('div');
  bar.className = 'mo-bar';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);

  /* Split the first h1 into words that rise in one after another */
  var h1 = document.querySelector('h1');
  if (h1) {
    var i = 0;
    Array.prototype.slice.call(h1.childNodes).forEach(function (node) {
      if (node.nodeType === 3) {
        var frag = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
          var w = document.createElement('span'); w.className = 'mo-w';
          var inner = document.createElement('span'); inner.textContent = part;
          inner.style.setProperty('--d', (0.12 + i++ * 0.08) + 's');
          w.appendChild(inner); frag.appendChild(w);
        });
        h1.replaceChild(frag, node);
      } else if (node.nodeType === 1) {
        var w2 = document.createElement('span'); w2.className = 'mo-w';
        var inner2 = document.createElement('span');
        inner2.style.setProperty('--d', (0.12 + i++ * 0.08) + 's');
        h1.replaceChild(w2, node); inner2.appendChild(node); w2.appendChild(inner2);
      }
    });
    var after = 0.25 + i * 0.08;
    var sib = h1.nextElementSibling, n = 0;
    while (sib) {
      sib.classList.add('mo-enter');
      sib.style.setProperty('--d', (after + n++ * 0.12) + 's');
      sib = sib.nextElementSibling;
    }
    var heroSide = h1.parentElement && h1.parentElement.nextElementSibling;
    if (heroSide && heroSide.closest('header')) { heroSide.classList.add('mo-enter'); heroSide.style.setProperty('--d', after + 's'); }
  }

  /* Scroll reveals for content blocks below the hero */
  var sel = (window.MOTION_REVEAL || 'section h2, section .head, section article, section .dish, section .panel, section li, section dl > div, section .info > div, .vista, .cta, .quiz');
  document.querySelectorAll(sel).forEach(function (el) {
    if (!el.closest('header') && !el.closest('.ag')) el.classList.add('mo-reveal');
  });
  document.querySelectorAll(window.MOTION_PARALLAX || '.vista svg').forEach(function (el) { el.classList.add('mo-par'); });

  /* Magnetic buttons */
  if (window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.btn').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.22) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.32) + 'px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }
})();
