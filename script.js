const year = document.querySelector("#year");
const portrait = document.querySelector("#portrait");

if (year) {
  year.textContent = new Date().getFullYear();
}

if (portrait) {
  const portraitCard = portrait.closest(".avatar-card");
  if (portrait.complete && portrait.naturalWidth) {
    portraitCard?.classList.add("loaded");
  }

  portrait.addEventListener("load", () => {
    portraitCard?.classList.add("loaded");
  });
  portrait.addEventListener("error", () => {
    portraitCard?.classList.remove("loaded");
  });
}
