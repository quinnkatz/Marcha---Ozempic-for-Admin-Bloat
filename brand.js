/**
 * BRAND CONFIG — swap name, email, and tagline here.
 * Hooks: [data-brand], [data-brand-email], [data-brand-tagline]
 */
window.REFIT_BRAND = {
  name: "Marcha",
  email: "hello@runmarcha.com",
  tagline: "AI tools assessments for medspas, studios, and practices. So you’re not needed at 9pm.",
};

document.addEventListener("DOMContentLoaded", () => {
  const b = window.REFIT_BRAND;
  document.querySelectorAll("[data-brand]").forEach((el) => {
    el.textContent = b.name;
  });
  document.querySelectorAll("[data-brand-email]").forEach((el) => {
    if (el.tagName === "A") {
      el.href = `mailto:${b.email}`;
      el.textContent = b.email;
    } else {
      el.textContent = b.email;
    }
  });
  document.querySelectorAll("[data-brand-tagline]").forEach((el) => {
    el.textContent = b.tagline;
  });
});
