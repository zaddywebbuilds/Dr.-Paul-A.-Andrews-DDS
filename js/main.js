/* ============================================================
   Dr. Paul A. Andrews, DDS, PhD — site scripts

   Built on the Oasis main.js (FAQ accordion, intersection-based
   animation/video pausing, conversion tracking hooks) with the
   dental site's own additions: mobile drawer, scroll reveals and
   the enquiry form.
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --------------------------------------------------------
     Current year in the footer
     -------------------------------------------------------- */
  document.querySelectorAll('.js-year').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  /* --------------------------------------------------------
     Mobile drawer menu
     -------------------------------------------------------- */
  const drawer = document.getElementById('menu-drawer');
  const openers = document.querySelectorAll('[data-menu-open]');
  let lastFocused = null;

  const setDrawer = (open) => {
    if (!drawer) return;
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    document.body.style.overflow = open ? 'hidden' : '';
    openers.forEach(o => o.setAttribute('aria-expanded', String(open)));
    if (open) {
      lastFocused = document.activeElement;
      const first = drawer.querySelector('.menu-drawer-close');
      if (first) first.focus();
    } else if (lastFocused) {
      lastFocused.focus();
    }
  };

  openers.forEach(btn => {
    btn.addEventListener('click', (e) => { e.preventDefault(); setDrawer(true); });
  });
  if (drawer) {
    drawer.addEventListener('click', (e) => {
      // Close on backdrop click, the X, or any link inside.
      if (e.target === drawer || e.target.closest('.menu-drawer-close') || e.target.closest('a')) {
        setDrawer(false);
      }
    });
    // Keep tab focus inside the open drawer.
    drawer.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab') return;
      const items = drawer.querySelectorAll('a[href], button');
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) setDrawer(false);
  });

  /* --------------------------------------------------------
     FAQ accordion (from Oasis — unchanged behaviour)
     -------------------------------------------------------- */
  document.querySelectorAll('.faq-item').forEach(item => {
    const btn = item.querySelector('.faq-q, .faq-question');
    if (!btn) return;
    if (btn.tagName !== 'BUTTON') {
      btn.setAttribute('role', 'button');
      btn.setAttribute('tabindex', '0');
    }
    btn.setAttribute('aria-expanded', item.classList.contains('open') ? 'true' : 'false');

    const toggle = () => {
      const willOpen = !item.classList.contains('open');
      const parent = item.parentElement;
      if (parent) {
        parent.querySelectorAll('.faq-item.open').forEach(o => {
          if (o !== item) {
            o.classList.remove('open');
            const ob = o.querySelector('.faq-q, .faq-question');
            if (ob) ob.setAttribute('aria-expanded', 'false');
          }
        });
      }
      item.classList.toggle('open', willOpen);
      btn.setAttribute('aria-expanded', String(willOpen));
    };

    btn.addEventListener('click', toggle);
    btn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });

  /* --------------------------------------------------------
     Scroll reveals — staggered, and skipped under reduced motion
     -------------------------------------------------------- */
  const revealables = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealables.forEach(el => el.classList.add('in'));
  } else {
    const revealObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        // Stagger siblings that share a parent for an editorial cascade.
        const sibs = [...(el.parentElement ? el.parentElement.children : [])]
          .filter(n => n.classList && n.classList.contains('reveal'));
        const i = Math.max(0, sibs.indexOf(el));
        el.style.setProperty('--d', Math.min(i, 5) * 90 + 'ms');
        el.classList.add('in');
        obs.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealables.forEach(el => revealObserver.observe(el));
  }

  /* --------------------------------------------------------
     Review marquee
     The set is cloned once so the track can scroll a full set width
     and loop with no visible seam. Duration is derived from the real
     width, so the reviews always drift at the same slow speed however
     many there are and however wide the screen is.
     -------------------------------------------------------- */
  const track = document.getElementById('review-track');
  if (track) {
    const set = track.querySelector('.review-set');
    const marquee = track.closest('.review-marquee');

    const SPEED = 38; // pixels per second — slow enough to read

    const build = () => {
      // Remove any previous clone before measuring.
      track.querySelectorAll('.review-set[data-clone]').forEach(n => n.remove());
      const width = set.scrollWidth;
      if (!width) return;

      const clone = set.cloneNode(true);
      clone.setAttribute('data-clone', 'true');
      clone.setAttribute('aria-hidden', 'true');
      // Keep the duplicate out of the tab order.
      clone.querySelectorAll('a, button').forEach(el => el.setAttribute('tabindex', '-1'));
      track.appendChild(clone);

      track.style.setProperty('--marquee-duration', (width / SPEED).toFixed(1) + 's');
    };

    build();
    // Re-measure when fonts finish loading or the viewport changes.
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
    let rt;
    window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(build, 200); }, { passive: true });

    // Pause while off screen so it costs nothing when not visible.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        entries.forEach(e => track.classList.toggle('paused', !e.isIntersecting));
      }, { threshold: 0 }).observe(marquee);
    }

    // Touch: tap to pause, tap again to resume.
    if (marquee) {
      marquee.addEventListener('click', (e) => {
        if (e.target.closest('a')) return;
        track.classList.toggle('paused');
      });
    }
  }

  /* --------------------------------------------------------
     Conversion tracking hooks
     No analytics provider is wired up yet; these fire only once
     gtag / fbq exist, so nothing is sent until the owner opts in.
     -------------------------------------------------------- */
  const trackEvent = (name, params = {}) => {
    if (typeof window.gtag === 'function') window.gtag('event', name, params);
    if (typeof window.fbq === 'function') window.fbq('trackCustom', name, params);
  };
  const bind = (selector, event) => {
    document.querySelectorAll(selector).forEach(a => {
      a.addEventListener('click', () => trackEvent(event, { location: window.location.pathname }));
    });
  };
  bind('a[href^="tel:"]', 'phone_click');
  bind('a[href^="mailto:"]', 'email_click');
  bind('a[href*="google.com/maps"]', 'directions_click');
  bind('[data-cta="appointment"]', 'appointment_click');

  /* --------------------------------------------------------
     Enquiry form
     Submits nothing over the network. Until the practice supplies a
     secure, HIPAA-appropriate endpoint, the form hands off to the
     visitor's own mail client so no patient data touches this site.
     -------------------------------------------------------- */
  const form = document.getElementById('enquiry-form');
  if (form) {
    const status = form.querySelector('.form-status');
    const say = (msg, kind) => {
      if (!status) return;
      status.textContent = msg;
      status.className = 'form-status show ' + kind;
    };

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = form.elements.name.value.trim();
      const contact = form.elements.contact.value.trim();
      const method = form.elements.method.value;
      const reason = form.elements.reason.value;
      const notes = (form.elements.notes.value || '').trim();
      const consent = form.elements.consent.checked;

      if (!name || !contact) {
        say('Please add your name and how we can reach you.', 'err');
        return;
      }
      if (!consent) {
        say('Please tick the consent box so we know it is okay to reply.', 'err');
        return;
      }

      const to = form.dataset.to || '';
      if (!to) {
        say('This demo form is not connected yet. A secure destination is set up before launch.', 'err');
        return;
      }

      const body = [
        'Name: ' + name,
        'Preferred contact: ' + method + ' — ' + contact,
        'Reason for enquiry: ' + reason,
        notes ? 'Notes: ' + notes : null,
        '',
        'Sent from the website enquiry form.'
      ].filter(Boolean).join('\n');

      window.location.href = 'mailto:' + to +
        '?subject=' + encodeURIComponent('Website enquiry — ' + name) +
        '&body=' + encodeURIComponent(body);

      say('Opening your email app so you can send this securely.', 'ok');
      trackEvent('enquiry_submit', { reason: reason });
    });
  }

  /* --------------------------------------------------------
     Performance — only animate and play what is on screen
     (from Oasis, kept intact)
     -------------------------------------------------------- */
  if ('IntersectionObserver' in window) {
    const videoObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const v = entry.target;
        if (entry.isIntersecting) {
          const p = v.play();
          if (p && p.catch) p.catch(() => {});
        } else {
          try { v.pause(); } catch (err) {}
        }
      });
    }, { threshold: 0.15, rootMargin: '100px 0px' });

    document.querySelectorAll('video[autoplay]').forEach(v => {
      v.removeAttribute('autoplay');
      videoObserver.observe(v);
    });

    const animTargets = document.querySelectorAll('.svc-ring, .cta-demos, .faq-deco');
    const animObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => entry.target.classList.toggle('anim-on', entry.isIntersecting));
    }, { threshold: 0.05 });
    animTargets.forEach(t => animObserver.observe(t));
  } else {
    document.querySelectorAll('.svc-ring, .cta-demos, .faq-deco')
      .forEach(t => t.classList.add('anim-on'));
  }
});
