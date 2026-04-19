(() => {
  const header = document.getElementById('siteHeader');
  const cartRoot = document.getElementById('cartDrawerRoot');

  const setHeaderState = () => {
    if (!header) return;
    const solid = window.scrollY > 8;
    header.classList.toggle('header-solid', solid);
  };

  const openCart = () => {
    if (!cartRoot) return;
    cartRoot.classList.remove('hidden');
    cartRoot.setAttribute('aria-hidden', 'false');
    document.documentElement.style.overflow = 'hidden';
  };

  const closeCart = () => {
    if (!cartRoot) return;
    cartRoot.classList.add('hidden');
    cartRoot.setAttribute('aria-hidden', 'true');
    document.documentElement.style.overflow = '';
  };

  const dismissSnackbar = (snackbar) => {
    snackbar.style.opacity = '0';
    window.setTimeout(() => {
      snackbar.remove();
    }, 300);
  };

  const initSnackbars = () => {
    const snackbars = document.querySelectorAll('[data-snackbar]');
    if (!snackbars.length) return;
    snackbars.forEach((snackbar) => {
      window.setTimeout(() => dismissSnackbar(snackbar), 3500);
    });
  };

  window.addEventListener('scroll', setHeaderState, { passive: true });
  window.addEventListener('load', setHeaderState);
  window.addEventListener('load', initSnackbars);

  document.addEventListener('click', (e) => {
    const target = e.target;
    if (!(target instanceof Element)) return;

    const snackbarClose = target.closest('[data-snackbar-close]');
    if (snackbarClose) {
      const snackbar = snackbarClose.closest('[data-snackbar]');
      if (snackbar) dismissSnackbar(snackbar);
      return;
    }

    if (target.closest('[data-cart-open]')) {
      openCart();
      return;
    }

    if (target.closest('[data-cart-close]')) {
      closeCart();
      return;
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeCart();
  });
})();

