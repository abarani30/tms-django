var activePage = window.location.pathname;
var navLinks = document.querySelectorAll('.nav-link');

for (i = 0; i < navLinks.length; i++) {
  link = navLinks[i].attributes.href.nodeValue;

  if (link == activePage) {
    navLinks[i].classList.add("active");
  }
  else if (link != activePage && link != "/") {
    var link = link.slice(1,link.length)
    if (activePage.includes(link)) 
      navLinks[i].classList.add("active");
  }
  else {
    navLinks[i].classList.remove("active");
  }
}
