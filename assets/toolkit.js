/* Shared helpers for the Marcha toolkit. No dependencies, no build step. */
(function (global) {
  "use strict";

  var store = {
    get: function (k) { try { return global.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { global.localStorage.setItem(k, v); } catch (e) {} }
  };

  function initTheme() {
    var root = document.documentElement;
    var saved = store.get("fc-theme");
    root.setAttribute("data-theme", (saved === "light" || saved === "dark") ? saved : "auto");

    function isDark() {
      var t = root.getAttribute("data-theme");
      return t === "dark" || (t === "auto" && global.matchMedia &&
        global.matchMedia("(prefers-color-scheme: dark)").matches);
    }
    var btns = document.querySelectorAll("[data-theme-toggle]");
    function label() {
      Array.prototype.forEach.call(btns, function (b) {
        b.textContent = isDark() ? "Light" : "Dark";
        b.setAttribute("aria-label", isDark() ? "Switch to light theme" : "Switch to dark theme");
      });
    }
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener("click", function () {
        var next = isDark() ? "light" : "dark";
        root.setAttribute("data-theme", next);
        store.set("fc-theme", next);
        label();
      });
    });
    label();
  }

  function money(n, cents) {
    var v = Number(n) || 0;
    return "$" + v.toFixed(cents ? 2 : 0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* download a JS value as a .json file, no server involved */
  function downloadJSON(filename, value) {
    var blob = new Blob([JSON.stringify(value, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 0);
  }

  function readJSONFile(file) {
    return new Promise(function (resolve, reject) {
      var fr = new FileReader();
      fr.onload = function () {
        try { resolve(JSON.parse(String(fr.result))); }
        catch (e) { reject(new Error("That file isn't valid JSON.")); }
      };
      fr.onerror = function () { reject(new Error("Couldn't read that file.")); };
      fr.readAsText(file);
    });
  }

  /* debounced autosave to localStorage, so a half-finished audit survives a refresh */
  function autosave(key, getState, delay) {
    var t = null;
    return function () {
      clearTimeout(t);
      t = setTimeout(function () {
        try { store.set(key, JSON.stringify(getState())); } catch (e) {}
      }, delay || 400);
    };
  }
  function restore(key) {
    var raw = store.get(key);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  }

  global.FC = {
    store: store, initTheme: initTheme, money: money, esc: esc,
    downloadJSON: downloadJSON, readJSONFile: readJSONFile,
    autosave: autosave, restore: restore
  };
})(window);
