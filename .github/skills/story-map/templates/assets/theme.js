(() => {
  const root = document.documentElement;
  const button = document.getElementById("theme-toggle");
  const label = document.getElementById("theme-label");
  const storageKey = "story-map-theme";

  if (!button || !label) {
    return;
  }

  try {
    const savedTheme = localStorage.getItem(storageKey);
    if (savedTheme === "light" || savedTheme === "dark") {
      root.dataset.theme = savedTheme;
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      root.dataset.theme = "dark";
    }
  } catch {
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      root.dataset.theme = "dark";
    }
  }

  const updateControl = () => {
    const isDark = root.dataset.theme === "dark";
    label.textContent = isDark ? "Light theme" : "Dark theme";
    button.setAttribute("aria-label", `Switch to ${isDark ? "light" : "dark"} theme`);
    button.setAttribute("aria-pressed", String(isDark));
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) {
      themeColor.content = isDark ? "#171a18" : "#f5f3ef";
    }
  };

  button.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    try {
      localStorage.setItem(storageKey, root.dataset.theme);
    } catch {
      // Theme switching still works for the current page when storage is unavailable.
    }
    updateControl();
  });

  updateControl();
})();
