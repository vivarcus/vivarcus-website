/* ============================================================
   Vivarcus Website — Shared helpers for interactive tool pages
   ============================================================ */

/* Print helper used by tool pages with printable output
   (时限日历 / TMF 自查器). The print CSS itself lives in each
   page's own <style> block (body.tools-print-mode …); this only
   toggles the mode class around window.print(). */
(() => {
  const PRINT_CLASS = "tools-print-mode";

  window.Tools = {
    printReport() {
      document.body.classList.add(PRINT_CLASS);
      const cleanup = () => document.body.classList.remove(PRINT_CLASS);
      window.addEventListener("afterprint", cleanup, { once: true });
      // Fallback: some browsers don't fire afterprint (e.g. print dialog cancelled)
      setTimeout(cleanup, 5000);
      window.print();
    },
  };
})();
