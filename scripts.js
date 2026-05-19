(function () {
  function setYear() {
    var el = document.getElementById('footer-year');
    if (el) {
      el.textContent = String(new Date().getFullYear());
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setYear);
  } else {
    setYear();
  }
})();
