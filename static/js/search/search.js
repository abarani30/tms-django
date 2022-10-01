function search() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.querySelector(".table");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}


/*
function getCurrentMonth() {
  var year          = new Date().getFullYear();
  var currentMonth  = new Date().getMonth() + 1;
  var startDate     = year + "-" + currentMonth + "-" + "01"
  var lastDate      = year + "-" + currentMonth + "-" + "31"
  
  return [startDate, lastDate]
}

*/

function editUser(employeerName) {
  var table, tr, td, i, links, checkbox;

  table = document.getElementById("table");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td && td.innerText == employeerName) {
      checkbox        = (tr[i].getElementsByTagName("td")[6]).children[0];
      links           = (tr[i].getElementsByTagName("td")[7]);

      if(checkbox.checked) {
        tr[i].style.background = "#eee"
        links.style.display = "";
      }
      else {
        tr[i].style.background = ""
        links.style.display = "none";
      }
    }
  }
}


$(function() {
  $('#datepicker1').datepicker();
  $('#datepicker2').datepicker();
});
