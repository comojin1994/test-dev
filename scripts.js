(function () {
  function setYear() {
    var el = document.getElementById('footer-year');
    if (el) {
      el.textContent = String(new Date().getFullYear());
    }
  }

  function setupBackToTop() {
    var btn = document.getElementById('back-to-top');
    if (!btn) return;
    function onScroll() {
      if (window.scrollY > 200) {
        btn.classList.add('is-visible');
      } else {
        btn.classList.remove('is-visible');
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    onScroll();
  }

  function init() {
    setYear();
    setupBackToTop();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
