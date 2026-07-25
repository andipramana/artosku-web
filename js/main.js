(() => {
  "use strict";

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- Footer year ----
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---- Tester request form ----
  // Submits straight to Supabase's REST API with the publishable key — no
  // backend of our own needed. The key is not secret (RLS is the actual
  // security boundary: anon can only INSERT here, never read the list back).
  const SUPABASE_URL = "https://klafrhlcxyyxdbrdenwk.supabase.co";
  const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_qWDO6IWishBFPgZnLnDGJw_9CIZs2eR";

  const testerForm = document.getElementById("testerForm");
  const testerStatus = document.getElementById("testerFormStatus");
  if (testerForm && testerStatus) {
    testerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = testerForm.email.value.trim();
      if (!email) return;

      const submitBtn = testerForm.querySelector("button[type=submit]");
      submitBtn.disabled = true;
      testerStatus.textContent = "Mengirim...";
      testerStatus.className = "tester-form__status";

      try {
        const res = await fetch(`${SUPABASE_URL}/rest/v1/tester_requests`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            apikey: SUPABASE_PUBLISHABLE_KEY,
            Authorization: `Bearer ${SUPABASE_PUBLISHABLE_KEY}`,
          },
          body: JSON.stringify({ email }),
        });

        // 409 = the unique index on lower(trim(email)) rejected a repeat
        // submission — not a real failure, so it gets the same reassuring
        // message as a fresh signup instead of the generic error path.
        if (res.status === 409) {
          testerStatus.textContent = "Email sudah terdaftar. Jika belum menerima informasi closed testing, tunggu pembaruan dari kami.";
          testerStatus.className = "tester-form__status is-success";
          testerForm.reset();
          return;
        }

        if (!res.ok) throw new Error(`Request failed: ${res.status}`);

        testerStatus.textContent = "Terima kasih! Emailmu sudah didaftarkan untuk closed testing. Kami akan mengabari setelah akunmu ditambahkan sebagai tester.";
        testerStatus.className = "tester-form__status is-success";
        testerForm.reset();
      } catch (err) {
        testerStatus.textContent = "Gagal mengirim, coba lagi sebentar lagi ya.";
        testerStatus.className = "tester-form__status is-error";
      } finally {
        submitBtn.disabled = false;
      }
    });
  }

  // ---- "Already invited?" reveal ----
  // The Play Store badge only makes sense for someone already whitelisted
  // as a tester — showing it to everyone up front just invites people who
  // aren't invited yet to tap it and hit a broken/blocked listing. Keep it
  // hidden behind a deliberate click instead.
  document.querySelectorAll(".already-invited").forEach((btn) => {
    btn.addEventListener("click", () => {
      const badge = btn.nextElementSibling;
      if (badge) badge.hidden = false;
      btn.hidden = true;
    });
  });

  // ---- Smooth-scroll only for in-page anchor links ----
  // `scroll-behavior: smooth` used to be set globally on <html>. That also
  // applies to ordinary mouse-wheel scrolling in Chrome/Edge on Windows,
  // where each discrete wheel tick gets turned into its own eased scroll
  // animation — a well-known cause of stepped/jittery-feeling scroll while
  // just reading the page. Scope smooth scrolling to anchor-link navigation
  // only, and leave native wheel/trackpad scrolling untouched.
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href").slice(1);
      const target = id ? document.getElementById(id) : null;
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "start" });
    });
  });

  // ---- Navbar glass on scroll ----
  const navbar = document.getElementById("navbar");
  const onNavScroll = () => {
    if (window.scrollY > 12) navbar.classList.add("is-scrolled");
    else navbar.classList.remove("is-scrolled");
  };
  onNavScroll();
  window.addEventListener("scroll", onNavScroll, { passive: true });

  // ---- Mobile menu ----
  const menuToggle = document.getElementById("menuToggle");
  const mobileMenu = document.getElementById("mobileMenu");
  if (menuToggle && mobileMenu) {
    const closeMenu = () => {
      menuToggle.setAttribute("aria-expanded", "false");
      mobileMenu.classList.remove("is-open");
      document.body.style.overflow = "";
    };
    const openMenu = () => {
      menuToggle.setAttribute("aria-expanded", "true");
      mobileMenu.classList.add("is-open");
      document.body.style.overflow = "hidden";
    };
    menuToggle.addEventListener("click", () => {
      const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
      isOpen ? closeMenu() : openMenu();
    });
    mobileMenu.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeMenu));
  }

  // ---- Scroll reveal ----
  const revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  // ---- Contact form (mailto handoff) ----
  // This is a static site with no backend and no third-party form service
  // wired in, so "submitting" the form means building a mailto: URL from the
  // field values and handing off to the visitor's own configured email
  // client with the message pre-filled. The name/message/type fields all
  // carry the native `required` attribute, so the browser blocks the submit
  // event (and shows its own validation UI) until they're filled in — no
  // extra validation logic needed here.
  const contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const name = contactForm.elements.name.value.trim();
      const type = contactForm.elements.type.value;
      const message = contactForm.elements.message.value.trim();

      const subject = `[Artosku] ${type} — dari ${name}`;
      const body = `Nama: ${name}\nJenis: ${type}\n\nPesan:\n${message}`;

      const mailto =
        "mailto:contact.artosku@gmail.com" +
        `?subject=${encodeURIComponent(subject)}` +
        `&body=${encodeURIComponent(body)}`;

      window.location.href = mailto;
    });
  }

  if (prefersReducedMotion) return; // skip parallax/tilt/cursor-glow entirely

  // ---- Cursor glow (desktop only) ----
  // NOTE: pointermove can fire hundreds of times/sec on some mice/trackpads.
  // Writing custom properties (which repaint a fixed, full-viewport
  // radial-gradient) on every raw event — instead of gating through rAF like
  // the scroll handler below does — was a source of visible jank. Throttle it
  // the same way.
  const cursorGlow = document.querySelector(".cursor-glow");
  if (cursorGlow && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    let glowActive = false;
    let glowTicking = false;
    let lastX = 0, lastY = 0;
    window.addEventListener(
      "pointermove",
      (e) => {
        lastX = e.clientX;
        lastY = e.clientY;
        if (!glowTicking) {
          requestAnimationFrame(() => {
            cursorGlow.style.setProperty("--mx", `${lastX}px`);
            cursorGlow.style.setProperty("--my", `${lastY}px`);
            if (!glowActive) {
              cursorGlow.classList.add("is-active");
              glowActive = true;
            }
            glowTicking = false;
          });
          glowTicking = true;
        }
      },
      { passive: true }
    );
  }

  // ---- Parallax on scroll (hero landscape layers) ----
  const parallaxLayers = document.querySelectorAll(".parallax-layer");
  const hero = document.querySelector(".hero");
  let ticking = false;

  const updateScrollParallax = () => {
    ticking = false;
    if (!hero) return;
    const rect = hero.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > window.innerHeight) return;
    const progress = -rect.top; // px scrolled past hero top
    parallaxLayers.forEach((layer) => {
      const speed = parseFloat(layer.dataset.speed || "0.1");
      layer.style.transform = `translate3d(0, ${progress * speed * 0.35}px, 0)`;
    });
  };

  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        requestAnimationFrame(updateScrollParallax);
        ticking = true;
      }
    },
    { passive: true }
  );

  // ---- Mouse parallax + 3D tilt on hero visual ----
  const heroVisual = document.getElementById("heroVisual");
  const phoneMock = document.getElementById("phoneMock");
  // NOTE: .floating-card / .floating-dot / .floating-spark carry a CSS
  // `animation` that drives `transform` (bob / spin-slow). Writing an inline
  // style.transform on those same elements would fight the CSS animation for
  // the `transform` property and cause visible jitter. So the mouse-tilt
  // effect below only ever writes to each element's inner `.floating-tilt`
  // wrapper, which has no CSS animation of its own — data-speed still lives
  // on the outer element.
  const floaters = Array.from(
    document.querySelectorAll(".floating-card, .floating-dot, .floating-spark")
  ).map((el) => ({
    speed: parseFloat(el.dataset.speed || "0.3"),
    target: el.querySelector(".floating-tilt") || el,
  }));

  if (heroVisual && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    let rafId = null;
    let targetX = 0, targetY = 0, currentX = 0, currentY = 0;

    heroVisual.addEventListener("pointermove", (e) => {
      const rect = heroVisual.getBoundingClientRect();
      targetX = (e.clientX - rect.left) / rect.width - 0.5; // -0.5..0.5
      targetY = (e.clientY - rect.top) / rect.height - 0.5;
      if (!rafId) rafId = requestAnimationFrame(tick);
    });

    heroVisual.addEventListener("pointerleave", () => {
      targetX = 0;
      targetY = 0;
      if (!rafId) rafId = requestAnimationFrame(tick);
    });

    function tick() {
      currentX += (targetX - currentX) * 0.08;
      currentY += (targetY - currentY) * 0.08;

      if (phoneMock) {
        phoneMock.style.setProperty("--rx", `${6 - currentY * 14}deg`);
        phoneMock.style.setProperty("--ry", `${-10 + currentX * 20}deg`);
      }
      floaters.forEach(({ speed, target }) => {
        target.style.setProperty("--tilt-x", `${currentX * 30 * speed}px`);
        target.style.setProperty("--tilt-y", `${currentY * 30 * speed}px`);
        target.style.transform = `translate(var(--tilt-x, 0), var(--tilt-y, 0))`;
      });

      if (Math.abs(targetX - currentX) > 0.001 || Math.abs(targetY - currentY) > 0.001) {
        rafId = requestAnimationFrame(tick);
      } else {
        rafId = null;
      }
    }
  }
})();
