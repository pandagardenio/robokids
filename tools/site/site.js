// A Year of Robots: small helpers for the website. Source: tools/site/site.js.
// Everything is saved only in this browser (localStorage) and the site works without it.
(function () {
  "use strict";

  var DONE_KEY = "robokids-done";
  var ORDER = []; // filled from the calendar cards when present

  function load(key, fallback) {
    try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; } catch (e) { return fallback; }
  }
  function save(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch (e) { return false; }
  }
  function doneSet() { return load(DONE_KEY, []); }
  function isDone(k) { return doneSet().indexOf(k) !== -1; }
  function setDone(k, on) {
    var d = doneSet().filter(function (x) { return x !== k; });
    if (on) d.push(k);
    save(DONE_KEY, d);
    refresh();
  }

  function refresh() {
    var done = doneSet();
    document.querySelectorAll("[data-week].week-card").forEach(function (el) {
      el.classList.toggle("is-done", done.indexOf(el.dataset.week) !== -1);
    });
    document.querySelectorAll("[data-done]").forEach(function (b) {
      b.setAttribute("aria-pressed", done.indexOf(b.dataset.done) !== -1 ? "true" : "false");
    });
    document.querySelectorAll("[data-done-box]").forEach(function (c) {
      c.checked = done.indexOf(c.dataset.doneBox) !== -1;
    });
    document.querySelectorAll("[data-phase-count]").forEach(function (el) {
      var keys = el.dataset.phaseCount.split(",");
      var n = keys.filter(function (k) { return done.indexOf(k) !== -1; }).length;
      el.textContent = n ? n + " / " + keys.length + " done" + (n === keys.length ? " 🏆" : "") : "";
    });
    var bar = document.querySelector(".progress-bar span");
    if (bar) {
      var weeks = done.filter(function (k) { return /^w\d+$/.test(k); }).length;
      bar.style.width = (weeks / 50 * 100) + "%";
      var txt = document.querySelector(".progress-text");
      if (weeks === 50) txt.textContent = "🏆 All 50 weeks done! Time for the certificate!";
      else if (weeks) txt.textContent = "🌟 " + weeks + " of 50 weeks done. Keep going!";
      var cont = document.querySelector("[data-continue]");
      if (cont && weeks && ORDER.length) {
        var next = ORDER.filter(function (c) { return done.indexOf(c.dataset.week) === -1; })[0];
        if (next) {
          cont.href = next.getAttribute("href");
          cont.textContent = "🚀 Continue: " + next.querySelector("b").textContent;
        }
      }
    }
  }

  // ---- done buttons and checkboxes
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-done]");
    if (b) {
      var on = b.getAttribute("aria-pressed") !== "true";
      setDone(b.dataset.done, on);
      if (on) cheer(b);
    }
    var p = e.target.closest("[data-print]");
    if (p) window.print();
    var c = e.target.closest("[data-copy]");
    if (c) copy(c);
  });
  document.addEventListener("change", function (e) {
    var c = e.target.closest("[data-done-box]");
    if (c) setDone(c.dataset.doneBox, c.checked);
  });

  // ---- copy program
  function copy(btn) {
    var code = document.getElementById(btn.dataset.copy);
    var text = code.textContent;
    var ok = function () {
      var old = btn.textContent;
      btn.textContent = "✅ Copied! Now paste it in MakeCode";
      btn.classList.add("copied");
      setTimeout(function () { btn.textContent = old; btn.classList.remove("copied"); }, 3500);
    };
    var fallback = function () {
      var r = document.createRange(); r.selectNodeContents(code);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      try { document.execCommand("copy"); ok(); } catch (e) { btn.textContent = "Press Ctrl+C (Mac: Cmd+C)"; }
    };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(ok, fallback);
    else fallback();
  }

  // ---- a little celebration
  function cheer(el) {
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var r = el.getBoundingClientRect();
    var bits = ["⭐", "🎉", "🤖", "✨", "💚"];
    for (var i = 0; i < 14; i++) {
      var s = document.createElement("span");
      s.textContent = bits[i % bits.length];
      s.style.cssText = "position:fixed;z-index:50;pointer-events:none;font-size:22px;transition:transform 1s ease-out,opacity 1s;" +
        "left:" + (r.left + r.width / 2) + "px;top:" + (r.top + r.height / 2) + "px";
      document.body.appendChild(s);
      (function (s, a) {
        requestAnimationFrame(function () {
          s.style.transform = "translate(" + Math.cos(a) * 120 + "px," + (Math.sin(a) * 120 - 40) + "px) rotate(" + (a * 90) + "deg)";
          s.style.opacity = "0";
        });
        setTimeout(function () { s.remove(); }, 1100);
      })(s, (i / 14) * Math.PI * 2);
    }
  }

  // ---- Robot Journal drawing pad
  function pad(host) {
    var key = "robokids-drawing-" + host.dataset.key;
    var colors = ["#2b2340", "#ea6c12", "#db2777", "#2563eb", "#16a34a", "#eab308", "#7c3aed"];
    var color = colors[0], size = 6, erasing = false;
    host.innerHTML =
      '<div class="pad-tools" role="toolbar" aria-label="Drawing tools">' +
      colors.map(function (c, i) { return '<button type="button" class="pad-color" style="background:' + c + '" data-c="' + c + '" aria-label="Color ' + (i + 1) + '" aria-pressed="' + (i === 0) + '"></button>'; }).join("") +
      '<button type="button" class="btn btn-ghost" data-size>✏️ Thin</button>' +
      '<button type="button" class="btn btn-ghost" data-erase aria-pressed="false">🧽 Eraser</button>' +
      '<button type="button" class="btn btn-ghost" data-clear>🗑️ Start again</button>' +
      '<button type="button" class="btn btn-ghost" data-save>💾 Save picture</button></div>' +
      '<canvas class="pad-canvas" aria-label="Drawing area: draw your robot with a finger or the mouse"></canvas>' +
      '<p class="pad-note">Draw your robot with a finger or the mouse. It stays in this browser.</p>';
    var cv = host.querySelector("canvas"), ctx = cv.getContext("2d");
    var W = 1200, H = 900;
    cv.width = W; cv.height = H;
    function blank() { ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); }
    blank();
    var saved = load(key, null);
    if (saved) { var img = new Image(); img.onload = function () { ctx.drawImage(img, 0, 0, W, H); }; img.src = saved; }
    function persist() { save(key, cv.toDataURL("image/jpeg", 0.7)); }
    var drawing = false, last = null;
    function pos(e) { var r = cv.getBoundingClientRect(); return { x: (e.clientX - r.left) * W / r.width, y: (e.clientY - r.top) * H / r.height }; }
    cv.addEventListener("pointerdown", function (e) { drawing = true; last = pos(e); cv.setPointerCapture(e.pointerId); line(last, last); });
    cv.addEventListener("pointermove", function (e) { if (!drawing) return; var p = pos(e); line(last, p); last = p; });
    function end() { if (drawing) { drawing = false; persist(); } }
    cv.addEventListener("pointerup", end); cv.addEventListener("pointercancel", end);
    function line(a, b) {
      ctx.strokeStyle = erasing ? "#fff" : color; ctx.lineWidth = erasing ? size * 4 : size;
      ctx.lineCap = "round"; ctx.lineJoin = "round";
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x + 0.01, b.y); ctx.stroke();
    }
    host.addEventListener("click", function (e) {
      var t = e.target.closest("button"); if (!t) return;
      if (t.dataset.c) {
        color = t.dataset.c; erasing = false;
        host.querySelectorAll(".pad-color").forEach(function (b) { b.setAttribute("aria-pressed", b === t); });
        host.querySelector("[data-erase]").setAttribute("aria-pressed", "false");
      } else if (t.hasAttribute("data-size")) {
        size = size === 6 ? 16 : size === 16 ? 32 : 6;
        t.textContent = size === 6 ? "✏️ Thin" : size === 16 ? "🖍️ Medium" : "🖌️ Thick";
      } else if (t.hasAttribute("data-erase")) {
        erasing = !erasing; t.setAttribute("aria-pressed", erasing);
      } else if (t.hasAttribute("data-clear")) {
        if (confirm("Start a new drawing? This one will be gone.")) { blank(); try { localStorage.removeItem(key); } catch (e2) {} }
      } else if (t.hasAttribute("data-save")) {
        var a = document.createElement("a");
        a.download = "my-robot-" + host.dataset.key + ".png"; a.href = cv.toDataURL("image/png"); a.click();
      }
    });
  }

  ORDER = Array.prototype.slice.call(document.querySelectorAll(".week-card[data-week^='w']"));
  document.querySelectorAll(".journal-pad").forEach(pad);
  refresh();
})();
