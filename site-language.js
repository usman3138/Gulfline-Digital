/* Blog language switch: no storage or tracking; every translation is in HTML. */
(() => {
  const buttons = document.querySelectorAll('[data-set-language]');
  function apply(lang) {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.setLanguage === lang));
    for (const element of document.querySelectorAll('[data-label-en]')) {
      element.setAttribute('aria-label', element.getAttribute('data-label-' + lang));
    }
  }
  for (const button of buttons) button.addEventListener('click', () => apply(button.dataset.setLanguage));
  apply(document.documentElement.lang === 'ar' ? 'ar' : 'en');
})();
