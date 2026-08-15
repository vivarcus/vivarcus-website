/* ============================================================
   Vivarcus Website — Interactions
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const header = document.querySelector(".site-header");
  const mobileToggle = document.querySelector(".mobile-toggle");
  const headerNav = document.querySelector(".header-nav");
  const headerActions = document.querySelector(".header-actions");

  // Sticky header + reading progress
  const progressBar = document.querySelector(".scroll-progress");
  let scrolled = false;
  let ticking = false;

  function render() {
    ticking = false;
    const isScrolled = window.scrollY > 10;
    if (isScrolled !== scrolled) {
      scrolled = isScrolled;
      header.classList.toggle("site-header--scrolled", isScrolled);
    }
    if (progressBar) {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = scrollable > 0 ? window.scrollY / scrollable : 0;
      progressBar.style.setProperty("--progress", Math.min(Math.max(ratio, 0), 1).toFixed(4));
    }
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(render);
    }
  }

  render();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });

  // Mobile menu toggle
  if (mobileToggle) {
    mobileToggle.addEventListener("click", () => {
      const isOpen = mobileToggle.classList.toggle("mobile-toggle--open");
      headerNav.classList.toggle("header-nav--open", isOpen);
      if (headerActions) {
        headerActions.classList.toggle("header-actions--open", isOpen);
      }
      document.body.style.overflow = isOpen ? "hidden" : "";
    });
  }

  // Close mobile menu on nav click
  headerNav?.addEventListener("click", (e) => {
    if (e.target.tagName === "A" && mobileToggle?.classList.contains("mobile-toggle--open")) {
      mobileToggle.click();
    }
  });

  // Highlight active nav link (resolve relative hrefs against current URL)
  const currentPath = window.location.pathname.replace(/\/$/, "") || "/";
  document.querySelectorAll(".header-nav a").forEach((link) => {
    const linkPath = new URL(link.getAttribute("href"), window.location.href).pathname.replace(/\/$/, "");
    if (linkPath === currentPath) {
      link.classList.add("nav-active");
    }
  });

  // Scroll reveal: single elements + staggered groups
  const revealTargets = [];

  document.querySelectorAll("[data-reveal]").forEach((el) => revealTargets.push(el));

  document.querySelectorAll("[data-reveal-group]").forEach((group) => {
    Array.from(group.children).forEach((child, i) => {
      child.dataset.stagger = String(Math.min(i * 90, 540));
      revealTargets.push(child);
    });
  });

  if (reduceMotion) {
    revealTargets.forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
  } else {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const delay = Number(el.dataset.stagger || 0);
          el.style.transitionDelay = delay ? `${delay}ms` : "";
          el.style.opacity = "1";
          el.style.transform = "translateY(0)";
          observer.unobserve(el);
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );

    revealTargets.forEach((el) => {
      el.style.opacity = "0";
      el.style.transform = "translateY(26px)";
      el.style.transition = "opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1), transform 0.7s cubic-bezier(0.22, 1, 0.36, 1)";
      observer.observe(el);
    });
  }

  // Keep looping decorations off the compositor while they are out of view
  const loopers = document.querySelectorAll(".cta-section, .hero");
  if (loopers.length && !reduceMotion) {
    const loopObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          entry.target.classList.toggle("is-inview", entry.isIntersecting);
        });
      },
      { rootMargin: "120px 0px" }
    );
    loopers.forEach((el) => loopObserver.observe(el));
  } else {
    loopers.forEach((el) => el.classList.add("is-inview"));
  }

  // Animated counters
  const counters = document.querySelectorAll("[data-counter]");
  if (counters.length) {
    const animateCounter = (el) => {
      const target = Number(el.dataset.counter);
      if (reduceMotion) {
        el.textContent = String(target);
        return;
      }
      const duration = 1400;
      const start = performance.now();
      const tick = (now) => {
        const t = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = String(Math.round(target * eased));
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };

    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((el) => counterObserver.observe(el));
  }

  // Language switcher
  const langToggles = document.querySelectorAll("[data-lang-toggle]");
  for (let i = 0; i < langToggles.length; i++) {
    langToggles[i].addEventListener("click", () => {
      if (window.I18N) window.I18N.toggle();
    });
  }

  // Hero glow follows the mouse
  const hero = document.querySelector(".hero");
  const heroGlow = document.querySelector(".hero__glow");
  if (hero && heroGlow && !reduceMotion && window.matchMedia("(pointer: fine)").matches) {
    hero.addEventListener("mousemove", (e) => {
      const rect = hero.getBoundingClientRect();
      heroGlow.style.setProperty("--mx", `${e.clientX - rect.left}px`);
      heroGlow.style.setProperty("--my", `${e.clientY - rect.top}px`);
    });
  }
});
