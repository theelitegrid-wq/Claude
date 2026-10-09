/* Demo AI agent widget. Scripted replies, configured per page through window.AGENT. */
(function () {
  var C = window.AGENT;
  if (!C) return;

  var css = [
    '.ag{--a:var(--ag-accent,#1f6f5c);--af:var(--ag-accent-fg,#fff);--b:var(--ag-bg,#fff);--f:var(--ag-fg,#14201c);--m:var(--ag-muted,#5e6b66);--l:var(--ag-line,#e2e7e4);--s:var(--ag-soft,#f2f5f3);',
    'position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:60;font-family:var(--ag-font,system-ui,sans-serif);color:var(--f)}',
    '.ag *{box-sizing:border-box}.ag [hidden]{display:none!important}',
    '.ag-launch{display:flex;align-items:center;gap:10px;margin-left:auto;border:0;cursor:pointer;background:var(--a);color:var(--af);font:600 15px/1 inherit;font-family:inherit;padding:14px 18px;border-radius:999px;box-shadow:0 10px 30px -8px rgba(0,0,0,.35)}',
    '.ag-launch:focus-visible,.ag-chip:focus-visible,.ag-send:focus-visible,.ag-x:focus-visible{outline:2px solid var(--a);outline-offset:3px}',
    '.ag-dot{width:9px;height:9px;border-radius:50%;background:currentColor;box-shadow:0 0 0 0 currentColor;animation:agp 2.2s infinite}',
    '@keyframes agp{0%{box-shadow:0 0 0 0 rgba(255,255,255,.55)}70%{box-shadow:0 0 0 9px rgba(255,255,255,0)}100%{box-shadow:0 0 0 0 rgba(255,255,255,0)}}',
    '.ag-panel{width:min(380px,calc(100vw - 32px));height:min(560px,calc(100vh - 120px));display:flex;flex-direction:column;background:var(--b);border:1px solid var(--l);border-radius:18px;overflow:hidden;box-shadow:0 30px 70px -20px rgba(0,0,0,.45);margin-bottom:12px;transform-origin:bottom right;animation:agin .28s cubic-bezier(.2,.8,.2,1)}',
    '@keyframes agin{from{opacity:0;transform:translateY(10px) scale(.97)}to{opacity:1;transform:none}}',
    '.ag-head{display:flex;align-items:center;gap:12px;padding:14px 16px;border-bottom:1px solid var(--l)}',
    '.ag-av{width:36px;height:36px;border-radius:50%;background:var(--a);color:var(--af);display:grid;place-items:center;font-weight:700;font-size:15px;flex:none}',
    '.ag-name{font-weight:650;font-size:15px}',
    '.ag-sub{font-size:12.5px;color:var(--m);display:flex;align-items:center;gap:6px}',
    '.ag-sub i{width:7px;height:7px;border-radius:50%;background:#2fb57a;display:inline-block}',
    '.ag-x{margin-left:auto;background:none;border:0;color:var(--m);font-size:22px;line-height:1;cursor:pointer;padding:4px 8px;border-radius:8px}',
    '.ag-log{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:var(--b)}',
    '.ag-m{max-width:85%;padding:10px 13px;border-radius:14px;font-size:14.5px;line-height:1.45;animation:agin .22s ease-out;white-space:pre-line}',
    '.ag-m.bot{background:var(--s);border-bottom-left-radius:4px}',
    '.ag-m.me{align-self:flex-end;background:var(--a);color:var(--af);border-bottom-right-radius:4px}',
    '.ag-act{align-self:center;font-size:12px;color:var(--m);border:1px dashed var(--l);border-radius:999px;padding:5px 11px;display:flex;gap:6px;align-items:center}',
    '.ag-act b{color:#2fb57a}',
    '.ag-typing{display:flex;gap:4px;padding:12px 14px}',
    '.ag-typing span{width:6px;height:6px;border-radius:50%;background:var(--m);opacity:.5;animation:agt 1s infinite}',
    '.ag-typing span:nth-child(2){animation-delay:.15s}.ag-typing span:nth-child(3){animation-delay:.3s}',
    '@keyframes agt{50%{opacity:1;transform:translateY(-3px)}}',
    '.ag-chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 16px 10px}',
    '.ag-chip{border:1px solid var(--l);background:var(--b);color:var(--f);font:inherit;font-size:13px;padding:7px 11px;border-radius:999px;cursor:pointer}',
    '.ag-chip:hover{border-color:var(--a);color:var(--a)}',
    '.ag-form{display:flex;gap:8px;padding:12px;border-top:1px solid var(--l)}',
    '.ag-in{flex:1;min-width:0;border:1px solid var(--l);background:var(--b);color:var(--f);border-radius:999px;padding:10px 14px;font:inherit;font-size:14.5px}',
    '.ag-in:focus{outline:none;border-color:var(--a)}',
    '.ag-send{border:0;background:var(--a);color:var(--af);border-radius:999px;padding:0 16px;font:inherit;font-weight:600;font-size:14px;cursor:pointer}',
    '.ag-note{font-size:11px;color:var(--m);text-align:center;padding:0 12px 10px}',
    '@media (prefers-reduced-motion:reduce){.ag *{animation:none!important}}'
  ].join('');

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var root = document.createElement('div');
  root.className = 'ag';
  root.innerHTML =
    '<div class="ag-panel" role="dialog" aria-label="Chat with ' + C.name + '" hidden>' +
      '<div class="ag-head"><div class="ag-av" aria-hidden="true">' + C.name.charAt(0) + '</div>' +
      '<div><div class="ag-name"></div><div class="ag-sub"><i></i>AI assistant, replies instantly</div></div>' +
      '<button class="ag-x" type="button" aria-label="Close chat">&times;</button></div>' +
      '<div class="ag-log" aria-live="polite"></div>' +
      '<div class="ag-chips"></div>' +
      '<form class="ag-form"><label for="ag-input" class="ag-sr" style="position:absolute;left:-9999px">Message</label>' +
      '<input id="ag-input" class="ag-in" autocomplete="off" placeholder="Type a message">' +
      '<button class="ag-send" type="submit">Send</button></form>' +
      '<div class="ag-note">Demo assistant with scripted replies</div>' +
    '</div>' +
    '<button class="ag-launch" type="button"><span class="ag-dot" aria-hidden="true"></span><span></span></button>';
  document.body.appendChild(root);

  var panel = root.querySelector('.ag-panel');
  var log = root.querySelector('.ag-log');
  var chips = root.querySelector('.ag-chips');
  var form = root.querySelector('.ag-form');
  var input = root.querySelector('.ag-in');
  var launch = root.querySelector('.ag-launch');
  root.querySelector('.ag-name').textContent = C.name;
  launch.lastChild.textContent = C.launchLabel || 'Ask ' + C.name;
  var started = false;
  var busy = false;

  function scroll() { log.scrollTop = log.scrollHeight; }

  function add(cls, text) {
    var el = document.createElement('div');
    el.className = cls;
    el.textContent = text;
    log.appendChild(el);
    scroll();
    return el;
  }

  function addAct(text) {
    var el = document.createElement('div');
    el.className = 'ag-act';
    var b = document.createElement('b');
    b.textContent = '✓';
    el.appendChild(b);
    el.appendChild(document.createTextNode(text));
    log.appendChild(el);
    scroll();
  }

  function setChips(list) {
    chips.innerHTML = '';
    (list || []).forEach(function (c) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'ag-chip';
      b.textContent = c;
      b.addEventListener('click', function () { send(c); });
      chips.appendChild(b);
    });
  }

  function find(text) {
    var t = text.toLowerCase();
    for (var i = 0; i < C.replies.length; i++) {
      var r = C.replies[i];
      for (var j = 0; j < r.k.length; j++) if (t.indexOf(r.k[j]) !== -1) return r;
    }
    return C.fallback;
  }

  function botSay(r) {
    busy = true;
    var t = document.createElement('div');
    t.className = 'ag-m bot ag-typing';
    t.innerHTML = '<span></span><span></span><span></span>';
    log.appendChild(t);
    scroll();
    var delay = Math.min(1600, 500 + r.a.length * 9);
    setTimeout(function () {
      t.remove();
      add('ag-m bot', r.a);
      (r.acts || []).forEach(function (a, i) {
        setTimeout(function () { addAct(a); }, 350 * (i + 1));
      });
      setChips(r.chips || C.chips);
      busy = false;
    }, delay);
  }

  function send(text) {
    text = text.trim();
    if (!text || busy) return;
    add('ag-m me', text);
    setChips([]);
    botSay(find(text));
  }

  function open() {
    panel.hidden = false;
    launch.setAttribute('aria-expanded', 'true');
    if (!started) {
      started = true;
      add('ag-m bot', C.greeting);
      setChips(C.chips);
    }
  }

  function close() {
    panel.hidden = true;
    launch.setAttribute('aria-expanded', 'false');
    launch.focus();
  }

  launch.addEventListener('click', function () { panel.hidden ? open() : close(); });
  root.querySelector('.ag-x').addEventListener('click', close);
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    send(input.value);
    input.value = '';
  });
  document.querySelectorAll('[data-open-agent]').forEach(function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); open(); input.focus(); });
  });

})();
