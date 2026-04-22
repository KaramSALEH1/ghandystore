(() => {
  const header = document.getElementById('siteHeader');
  const cartRoot = document.getElementById('cartDrawerRoot');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileMenuToggle = document.querySelector('[data-mobile-menu-toggle]');

  const setHeaderState = () => {
    if (!header) return;
    const solid = window.scrollY > 8;
    header.classList.toggle('header-solid', solid);
  };

  const isCartOpen = () => Boolean(cartRoot && !cartRoot.classList.contains('hidden'));
  const isMobileMenuOpen = () => Boolean(mobileMenu && !mobileMenu.classList.contains('hidden'));

  const setScrollLocked = (locked) => {
    if (locked) {
      document.documentElement.style.overflow = 'hidden';
      return;
    }
    if (isCartOpen() || isMobileMenuOpen()) return;
    document.documentElement.style.overflow = '';
  };

  const openCart = () => {
    if (!cartRoot) return;
    cartRoot.classList.remove('hidden');
    cartRoot.setAttribute('aria-hidden', 'false');
    setScrollLocked(true);
  };

  const closeCart = () => {
    if (!cartRoot) return;
    cartRoot.classList.add('hidden');
    cartRoot.setAttribute('aria-hidden', 'true');
    setScrollLocked(false);
  };

  const openMobileMenu = () => {
    if (!mobileMenu) return;
    mobileMenu.classList.remove('hidden');
    mobileMenu.setAttribute('aria-hidden', 'false');
    if (mobileMenuToggle instanceof Element) {
      mobileMenuToggle.setAttribute('aria-expanded', 'true');
    }
    setScrollLocked(true);
  };

  const closeMobileMenu = () => {
    if (!mobileMenu) return;
    mobileMenu.classList.add('hidden');
    mobileMenu.setAttribute('aria-hidden', 'true');
    if (mobileMenuToggle instanceof Element) {
      mobileMenuToggle.setAttribute('aria-expanded', 'false');
    }
    setScrollLocked(false);
  };

  const toggleMobileMenu = () => {
    if (!mobileMenu) return;
    if (isMobileMenuOpen()) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
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

    const backButton = target.closest('[data-back]');
    if (backButton) {
      window.history.back();
      return;
    }

    const snackbarClose = target.closest('[data-snackbar-close]');
    if (snackbarClose) {
      const snackbar = snackbarClose.closest('[data-snackbar]');
      if (snackbar) dismissSnackbar(snackbar);
      return;
    }

    if (target.closest('[data-mobile-menu-toggle]')) {
      toggleMobileMenu();
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

    if (isMobileMenuOpen()) {
      if (target.closest('#mobileMenu a')) {
        closeMobileMenu();
        return;
      }
      if (!target.closest('#mobileMenu') && !target.closest('[data-mobile-menu-toggle]')) {
        closeMobileMenu();
      }
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeCart();
      closeMobileMenu();
    }
  });
})();

