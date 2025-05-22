/* main.js — global client-side helpers
   ------------------------------------------------------------ */

/* Auto-dismiss Bootstrap alerts after 4 s --------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert:not(.alert-important)");
  alerts.forEach((alert) => {
    setTimeout(() => {
      // Use Bootstrap 5′s native dismissal
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });
});

