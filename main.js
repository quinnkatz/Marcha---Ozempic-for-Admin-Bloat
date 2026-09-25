(() => {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const reduce = document.documentElement.classList.contains("reduce")
    || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const preview = document.documentElement.getAttribute("data-preview");
  const clamp = (n, a, b) => Math.min(b, Math.max(a, n));

  const year = $("#year");
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- loader ---------- */
  const loader = $("#loader");
  const finishLoader = () => {
    if (!loader || loader.classList.contains("is-done")) return;
    loader.classList.add("is-done");
    window.setTimeout(() => {
      loader.style.display = "none";
    }, 900);
    $$(".hero .reveal").forEach((el) => el.classList.add("in"));
  };

  if (preview === "loader" && !reduce) {
    /* hold for screenshots */
  } else if (reduce || !loader) {
    if (loader) loader.style.display = "none";
    $$(".hero .reveal").forEach((el) => el.classList.add("in"));
  } else {
    window.setTimeout(finishLoader, preview ? 40 : 1520);
    window.setTimeout(finishLoader, 2400);
  }

  /* ---------- header ---------- */
  const header = $("#header");
  const toggle = $(".nav-toggle");
  const panel = $("#nav-panel");
  const closeNav = () => {
    if (!toggle || !panel) return;
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
    panel.classList.remove("is-open");
    requestFrame();
  };
  if (toggle && panel) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      panel.classList.toggle("is-open", open);
      requestFrame();
    });
    panel.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeNav));
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeNav();
        closeMenu();
      }
    });
  }

  const processLink = $(".has-sub > a");
  const processItem = $(".has-sub");
  if (processLink && processItem) {
    const setOpen = (open) => {
      processItem.classList.toggle("is-open", open);
      processLink.setAttribute("aria-expanded", String(open));
    };
    processItem.addEventListener("pointerenter", () => setOpen(true));
    processItem.addEventListener("pointerleave", () => setOpen(false));
    processItem.addEventListener("focusin", () => setOpen(true));
    processItem.addEventListener("focusout", (e) => {
      if (!processItem.contains(e.relatedTarget)) setOpen(false);
    });
    processLink.addEventListener("click", (e) => {
      if (window.matchMedia("(max-width: 1040px)").matches) return;
      e.preventDefault();
      setOpen(!processItem.classList.contains("is-open"));
    });
  }

  /* ---------- scene launcher ---------- */
  const launcher = $(".scene-launcher");
  const sceneMenu = $("#scene-menu");
  const closeMenu = () => {
    if (!launcher || !sceneMenu) return;
    launcher.setAttribute("aria-expanded", "false");
    sceneMenu.classList.remove("is-open");
    sceneMenu.hidden = true;
  };
  if (launcher && sceneMenu) {
    launcher.addEventListener("click", () => {
      const open = launcher.getAttribute("aria-expanded") !== "true";
      launcher.setAttribute("aria-expanded", String(open));
      sceneMenu.hidden = false;
      requestAnimationFrame(() => sceneMenu.classList.toggle("is-open", open));
      if (!open) window.setTimeout(() => { if (!sceneMenu.classList.contains("is-open")) sceneMenu.hidden = true; }, 500);
    });
    sceneMenu.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeMenu));
  }

  /* ---------- reveals ---------- */
  const reveals = $$(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach((el) => io.observe(el));
  }

  /* ---------- nav spy ---------- */
  const navLinks = $$("[data-nav]");
  const spyTargets = navLinks
    .map((a) => document.getElementById(a.dataset.nav))
    .filter(Boolean);
  if (spyTargets.length && "IntersectionObserver" in window) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((a) => a.classList.toggle("is-active", a.dataset.nav === entry.target.id));
      });
    }, { rootMargin: "-40% 0px -50% 0px", threshold: 0 });
    spyTargets.forEach((el) => spy.observe(el));
  }

  /* ---------- scroll engine ---------- */
  const scenes = $$("[data-scene]");
  const railSeg = $("[data-rail-seg]");
  const rail = $("[data-rail]");
  const hoursTrack = $("[data-hours-track]");
  const hoursOrb = $("[data-hours-orb]");
  const heroSeg = $(".hero-track span");
  const railName = $("[data-rail-name]");
  const sceneLabels = scenes.map((el, i) => el.dataset.sceneLabel || `${String(i + 1).padStart(2, "0")} · Scene`);
  const howTrack = $("[data-how-track]");
  const shiftTrack = $("[data-shift-track]");
  const shiftBefore = $("[data-shift-before]");
  const shiftAfter = $("[data-shift-after]");
  const shiftDisc = $(".shift-disc");
  const driftDiscs = $$("[data-disc]");
  const howSteps = $$("[data-how-step]");
  const deviceScroll = $("[data-device-scroll]");
  const deviceScreen = $("[data-device-screen]");
  const deviceThumb = $("[data-device-thumb]");
  const plates = $$("[data-plate]");
  const parallaxBits = $$("[data-py]");
  const prevBtn = $("[data-scroll='prev']");
  const nextBtn = $("[data-scroll='next']");
  const mobileBar = $("#mobile-bar");
  const book = $("#book");
  const narrow = window.matchMedia("(max-width: 1040px)");

  const sceneTop = (el) => el.getBoundingClientRect().top + window.scrollY;

  function progressOf(track) {
    if (!track) return 0;
    const rect = track.getBoundingClientRect();
    const total = track.offsetHeight - window.innerHeight;
    if (total <= 0) return 0;
    return clamp(-rect.top / total, 0, 1);
  }

  function setHours(p) {
    if (hoursOrb) {
      const shift = ((p - 0.5) * 18).toFixed(1);
      const grow = (1 + p * 0.035).toFixed(3);
      hoursOrb.style.transform = `translateY(${shift}px) scale(${grow})`;
    }
  }

  function setShift(p) {
    if (!shiftBefore || !shiftAfter) return;
    if (reduce || narrow.matches) {
      shiftBefore.style.transform = "";
      shiftAfter.style.transform = "";
      if (shiftDisc) shiftDisc.style.transform = "";
      return;
    }
    /* Readable hold, a short slide, then a readable hold. No long clipped stretch. */
    let travel = 0;
    if (p > 0.62) travel = 1;
    else if (p > 0.28) travel = (p - 0.28) / 0.34;
    const eased = travel * travel * (3 - 2 * travel);
    shiftBefore.style.transform = `translate3d(${(-eased * 115).toFixed(1)}%, 0, 0)`;
    shiftAfter.style.transform = `translate3d(${((1 - eased) * 108).toFixed(1)}%, 0, 0)`;
    if (shiftDisc) {
      const settled = p * p * (3 - 2 * p);
      const drift = (settled - 0.5) * 22;
      shiftDisc.style.transform = `translate3d(${drift.toFixed(1)}px, ${(drift * 0.35).toFixed(1)}px, 0)`;
    }
  }

  function setHow(p) {
    const sheets = deviceScroll ? [...deviceScroll.children] : [];
    const n = Math.max(sheets.length, howSteps.length, 1);
    let idx = Math.min(n - 1, Math.floor(p * n));
    let frac = p * n - idx;
    if (p >= 0.995 || idx >= n - 1) {
      idx = n - 1;
      frac = 0;
    }
    /* Most of each step holds one full plan. A short slice eases to the next. */
    const travel = frac < 0.8 ? 0 : (frac - 0.8) / 0.2;
    const eased = travel * travel * (3 - 2 * travel);
    if (deviceScroll && deviceScreen && !reduce && !narrow.matches) {
      const sheetH = deviceScreen.clientHeight;
      sheets.forEach((sheet) => {
        sheet.style.height = `${sheetH}px`;
      });
      const shift = Math.min((idx + eased) * sheetH, Math.max(0, n - 1) * sheetH);
      deviceScroll.style.transform = `translate3d(0, ${(-shift).toFixed(1)}px, 0)`;
    }
    const shown = eased > 0.55 && idx < n - 1 ? idx + 1 : idx;
    if (deviceThumb && deviceThumb.parentElement) {
      const bar = deviceThumb.parentElement.clientHeight - deviceThumb.offsetHeight;
      const thumbP = n > 1 ? shown / (n - 1) : 0;
      deviceThumb.style.transform = `translateY(${(thumbP * bar).toFixed(1)}px)`;
    }
    howSteps.forEach((el, i) => el.classList.toggle("is-on", i === shown));
  }

  let currentScene = 0;
  function frame() {
    const y = window.scrollY;

    if (header) header.classList.toggle("scrolled", y > 8);
    if (launcher) launcher.classList.toggle("is-on", y > window.innerHeight * 0.72 && !narrow.matches);

    const marker = y + window.innerHeight * 0.34;
    currentScene = 0;
    scenes.forEach((el, i) => {
      if (sceneTop(el) <= marker) currentScene = i;
    });
    if (railName) {
      const label = sceneLabels[currentScene] || sceneLabels[0];
      if (railName.textContent !== label) railName.textContent = label;
    }
    if (rail && railName && !narrow.matches) {
      const scene = scenes[currentScene];
      const anchor = scene?.querySelector(".eyebrow") || scene?.querySelector("h1, h2");
      if (anchor) {
        const box = anchor.getBoundingClientRect();
        const labelH = railName.offsetHeight || 16;
        const raw = box.height < 48 ? box.top + (box.height - labelH) / 2 : box.top;
        const min = (header ? header.offsetHeight : 78) + 8;
        const max = window.innerHeight - labelH - 24;
        const top = clamp(raw, min, max);
        rail.style.top = `${top.toFixed(1)}px`;
        if (railSeg) railSeg.style.transform = "translateY(0)";
        railName.style.top = `${top.toFixed(1)}px`;
      }
    }
    if (heroSeg) {
      const track = heroSeg.parentElement;
      const span = Math.max(0, track.clientHeight - heroSeg.offsetHeight);
      const local = clamp(y / window.innerHeight, 0, 1);
      heroSeg.style.transform = `translateY(${(local * span).toFixed(1)}px)`;
    }

    if (!reduce) {
      const heroIn = y < window.innerHeight * 1.15;
      if (heroIn) {
        const heroP = clamp(y / window.innerHeight, 0, 1);
        const settled = heroP * heroP * (3 - 2 * heroP);
        const travel = settled * window.innerHeight;
        const rates = { halo: 0.1, orb: 0.07, back: 0.02, mock: -0.01, badge: -0.035, mark: -0.05 };
        parallaxBits.forEach((el) => {
          const key = el.dataset.py;
          const rate = rates[key] ?? 0.02;
          el.style.setProperty("--py", `${(travel * rate).toFixed(1)}px`);
          if (key === "orb") {
            el.style.setProperty("--ps", (1 + travel * 0.000025).toFixed(4));
            el.style.setProperty("--pr", `${(travel * 0.004).toFixed(2)}deg`);
          }
        });
      }
      plates.forEach((plate) => {
        const rect = plate.parentElement.getBoundingClientRect();
        const local = clamp((window.innerHeight - rect.top) / (window.innerHeight + rect.height), 0, 1);
        plate.style.setProperty("--plate", `${((local - 0.5) * 72).toFixed(1)}px`);
      });
      driftDiscs.forEach((disc) => {
        const parent = disc.parentElement;
        if (!parent) return;
        const rect = parent.getBoundingClientRect();
        const local = clamp((window.innerHeight - rect.top) / (window.innerHeight + rect.height), 0, 1);
        const settled = local * local * (3 - 2 * local);
        disc.style.transform = `translate3d(0, ${((settled - 0.5) * 36).toFixed(1)}px, 0)`;
      });
      if (!narrow.matches) {
        setHours(progressOf(hoursTrack));
        setShift(progressOf(shiftTrack));
        setHow(progressOf(howTrack));
      }
    }

    if (prevBtn) prevBtn.disabled = currentScene <= 0;
    if (nextBtn) nextBtn.disabled = currentScene >= scenes.length - 1;

    if (mobileBar && book && narrow.matches) {
      const heroEl = $("#hero");
      const heroBottom = heroEl ? heroEl.getBoundingClientRect().bottom : 0;
      const bookTop = book.getBoundingClientRect().top;
      const navOpen = panel && panel.classList.contains("is-open");
      const show = !navOpen && heroBottom < window.innerHeight * 0.42 && bookTop > window.innerHeight * 0.8;
      mobileBar.classList.toggle("is-on", show);
      mobileBar.hidden = !show;
      document.body.classList.toggle("has-book-bar", show);
    } else if (mobileBar) {
      mobileBar.classList.remove("is-on");
      mobileBar.hidden = true;
      document.body.classList.remove("has-book-bar");
    }
  }

  let ticking = false;
  const requestFrame = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      frame();
    });
  };
  window.addEventListener("scroll", requestFrame, { passive: true });
  window.addEventListener("resize", requestFrame);
  frame();

  function goScene(dir) {
    const next = scenes[clamp(currentScene + dir, 0, scenes.length - 1)];
    if (!next) return;
    const bleed = next.id === "hero" || next.id === "hours" || next.id === "how";
    const pad = bleed || !header ? 0 : header.offsetHeight;
    window.scrollTo({ top: Math.max(0, sceneTop(next) - pad), behavior: reduce ? "auto" : "smooth" });
  }
  if (prevBtn) prevBtn.addEventListener("click", () => goScene(-1));
  if (nextBtn) nextBtn.addEventListener("click", () => goScene(1));

  const eye = $("[data-eye]");
  if (eye && howTrack) {
    eye.addEventListener("click", () => {
      if (narrow.matches || reduce) {
        if (deviceScreen) deviceScreen.scrollBy({ top: 420, behavior: reduce ? "auto" : "smooth" });
        return;
      }
      const step = (howTrack.offsetHeight - window.innerHeight) / 4;
      window.scrollBy({ top: step, behavior: "smooth" });
    });
  }

  $$("[data-step-jump]").forEach((a) => {
    a.addEventListener("click", (e) => {
      if (narrow.matches || reduce || !howTrack) return;
      e.preventDefault();
      const step = Number(a.dataset.stepJump) || 0;
      const span = howTrack.offsetHeight - window.innerHeight;
      const top = sceneTop(howTrack) + (span * step) / 4 + 8;
      window.scrollTo({ top, behavior: "smooth" });
    });
  });

  /* ---------- economics sketch ---------- */
  const econForm = document.querySelector("[data-econ]");
  if (econForm) {
    const emptyEl = econForm.querySelector("[data-math-empty]");
    const resultEl = econForm.querySelector("[data-math-result]");
    const linesEl = econForm.querySelector("[data-math-lines]");
    const monthEl = econForm.querySelector("[data-math-month]");
    const yearEl = econForm.querySelector("[data-math-year]");
    const usd = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    });
    const num = (name) => {
      const el = econForm.elements.namedItem(name);
      if (!el || !("value" in el)) return 0;
      const n = Number(String(el.value).trim());
      return Number.isFinite(n) && n > 0 ? n : 0;
    };
    const paint = () => {
      const missed = num("inquiries") * num("customer");
      const empty = num("slots") * num("appointment");
      const labor = num("staffHours") * num("staffRate") * 4.33;
      const owner = num("ownerHours") * num("ownerRate") * 4.33;
      const month = missed + empty + labor + owner;
      const rows = [
        ["Unanswered leads", missed],
        ["Empty appointments", empty],
        ["Repetitive labor", labor],
        ["Owner attention", owner],
      ].filter((row) => row[1] > 0);
      if (!rows.length) {
        if (resultEl) resultEl.hidden = true;
        if (emptyEl) emptyEl.hidden = false;
        return;
      }
      if (emptyEl) emptyEl.hidden = true;
      if (resultEl) resultEl.hidden = false;
      if (linesEl) {
        linesEl.replaceChildren(...rows.map(([label, amount]) => {
          const li = document.createElement("li");
          const name = document.createElement("span");
          name.textContent = label;
          const value = document.createElement("b");
          value.textContent = usd.format(amount);
          li.append(name, value);
          return li;
        }));
      }
      if (monthEl) monthEl.textContent = usd.format(month);
      if (yearEl) yearEl.textContent = `About ${usd.format(month * 12)} across a year, on these assumptions.`;
    };
    econForm.addEventListener("submit", (e) => e.preventDefault());
    econForm.addEventListener("input", paint);
    paint();
  }

  /* ---------- practice filters ---------- */
  const filterBtns = $$("[data-filter]");
  const tiles = $$("[data-kind]");
  function applyFilter(kind) {
    filterBtns.forEach((btn) => btn.setAttribute("aria-pressed", String(btn.dataset.filter === kind)));
    tiles.forEach((tile) => {
      const show = kind === "all" || tile.dataset.kind === kind;
      tile.hidden = !show;
    });
  }
  filterBtns.forEach((btn) => btn.addEventListener("click", () => applyFilter(btn.dataset.filter)));

  /* ---------- booking ---------- */
  const form = $("#book-form");
  const status = $("[data-form-status]");
  const submitBtn = $("#book-submit");
  const emailOk = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  const setFieldError = (id, message) => {
    const input = document.getElementById(id);
    const err = document.getElementById(`${id}-error`);
    if (!input || !err) return;
    if (message) {
      input.setAttribute("aria-invalid", "true");
      err.hidden = false;
      err.textContent = message;
    } else {
      input.removeAttribute("aria-invalid");
      err.hidden = true;
      err.textContent = "";
    }
  };
  const setStatus = (message, kind) => {
    if (!status) return;
    status.textContent = "";
    status.classList.toggle("is-error", kind === "error");
    status.classList.toggle("is-ok", kind === "ok");
    if (!message) return;
    window.requestAnimationFrame(() => {
      status.textContent = message;
    });
  };
  if (form) {
    ["name", "email", "practice"].forEach((id) => {
      const input = document.getElementById(id);
      if (!input) return;
      input.addEventListener("input", () => setFieldError(id, ""));
      input.addEventListener("change", () => setFieldError(id, ""));
    });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if ($("#company") && $("#company").value) return;
      const brand = window.REFIT_BRAND || { name: "Marcha", email: "hello@runmarcha.com" };
      const name = ($("#name").value || "").trim();
      const email = ($("#email").value || "").trim();
      const practice = ($("#practice").value || "").trim();
      const note = ($("#note").value || "").trim();
      const problems = [];
      if (!name) problems.push(["name", "Add your name."]);
      else setFieldError("name", "");
      if (!emailOk(email)) problems.push(["email", "Use an email we can reply to."]);
      else setFieldError("email", "");
      if (!practice) problems.push(["practice", "Choose a studio or practice."]);
      else setFieldError("practice", "");
      if (problems.length) {
        problems.forEach(([id, message]) => setFieldError(id, message));
        setStatus("Name, email, and studio or practice — then we can write back.", "error");
        const first = document.getElementById(problems[0][0]);
        if (first) first.focus();
        return;
      }
      const subject = encodeURIComponent(`${brand.name} assessment request — ${practice}`);
      const body = encodeURIComponent(
        [
          `Hi ${brand.name} team,`,
          "",
          "We'd like to request the $1,999 Marcha Business Assessment.",
          "",
          `Name: ${name}`,
          `Email: ${email}`,
          `Studio or practice: ${practice}`,
          note ? `Notes: ${note}` : null,
          "",
          "Thanks,",
          name,
        ].filter(Boolean).join("\n")
      );
      if (submitBtn) submitBtn.disabled = true;
      form.setAttribute("aria-busy", "true");
      setStatus("Opening your email…", "ok");
      window.location.href = `mailto:${brand.email}?subject=${subject}&body=${body}`;
      window.setTimeout(() => {
        if (submitBtn) submitBtn.disabled = false;
        form.removeAttribute("aria-busy");
        setStatus(`Your email app should be open. If it isn’t, write us at ${brand.email}.`, "ok");
      }, 700);
    });
  }

  /* ---------- screenshot positions ---------- */
  if (preview && preview !== "loader") {
    reveals.forEach((el) => el.classList.add("in"));
    const jump = () => {
      const mid = (track) => {
        if (!track) return;
        const total = Math.max(0, track.offsetHeight - window.innerHeight);
        window.scrollTo(0, sceneTop(track) + total * 0.55);
      };
      if (preview === "hours") mid(hoursTrack);
      else if (preview === "shift" || preview === "philosophy") mid(shiftTrack);
      else if (preview === "mock" || preview === "how") {
        const total = howTrack ? Math.max(0, howTrack.offsetHeight - window.innerHeight) : 0;
        const at = Number(new URLSearchParams(location.search).get("at"));
        const p = Number.isFinite(at) ? clamp(at, 0, 0.99) : 0.3;
        window.scrollTo(0, sceneTop(howTrack) + total * p);
      }
      else if (preview === "hero" || preview === "menu") window.scrollTo(0, 0);
      else {
        const el = document.getElementById(preview);
        if (el) window.scrollTo(0, sceneTop(el) + 2);
      }
      if (preview === "menu") document.querySelector(".has-sub")?.classList.add("is-open");
      requestAnimationFrame(frame);
    };
    window.setTimeout(jump, 60);
  }
})();
