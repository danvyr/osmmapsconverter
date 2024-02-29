let lang = navigator.language.slice(0, 2); // Get the first two letters of user's language preference

// Hide elements that don't correspond to the user's preferred language
if (lang === 'en') {
  document.querySelectorAll('.second-language').forEach(elem => elem.style.display = 'none');
} else {
  document.querySelectorAll('.english').forEach(elem => elem.style.display = 'none');
}
