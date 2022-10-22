var activePage = window.location.pathname;
var navLinks = document.querySelectorAll('.nav-link');

const employeesPages = [
  "/systems_employees.html", "/maintenance_employees.html",
  "/adminstration_employees.html", "cms_employees.html"
]

const tasksPages = [
  "/systems_tasks.html", "/maintenance_employees.html",
  "/director_tasks.html"
]

for (i = 0; i < navLinks.length; i++) {
  link = navLinks[i].attributes.href.nodeValue;
  
  if (link != "/" && 
    ! employeesPages.includes(activePage) &&
    !tasksPages.includes(activePage)
  ) 
    link = "/" + link

  if (link == activePage) {
    navLinks[i].classList.add("active");
  }
  else if (employeesPages.includes(activePage) && link == "#employees") {
    navLinks[i].classList.add("active");
  }
  else if (tasksPages.includes(activePage) && link == "#tasks") {
    navLinks[i].classList.add("active");
  }
  else {
    navLinks[i].classList.remove("active");
  }
}

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))

var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
