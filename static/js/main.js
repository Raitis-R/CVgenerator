// CV ģeneratora front-end skripts
document.addEventListener("DOMContentLoaded", function () {
  // "Drukāt / saglabāt PDF" poga
  document.querySelectorAll("[data-print]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      window.print();
    });
  });

  // Dizaina maiņa priekšskatījumā bez lapas pārlādes
  var select = document.getElementById("theme-select");
  var doc = document.getElementById("cv-document");
  if (select && doc) {
    select.addEventListener("change", function () {
      doc.classList.remove("cv-classic", "cv-modern", "cv-minimal");
      doc.classList.add("cv-" + select.value);
    });
  }

  // Ziņojumi pazūd paši pēc 5 sekundēm
  document.querySelectorAll(".alert-success").forEach(function (alert) {
    setTimeout(function () {
      alert.classList.remove("show");
      setTimeout(function () { alert.remove(); }, 300);
    }, 5000);
  });
});
