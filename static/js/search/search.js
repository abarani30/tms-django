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
  var currentUsername, currentEmail, currentDivision, currentAccount, 
  table, tr, td, i, links, checkbox;

  table = document.getElementById("table");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td && td.innerText == employeerName) {
      currentUsername = tr[i].getElementsByTagName("td")[1];
      currentEmail    = tr[i].getElementsByTagName("td")[2];
      currentDivision = (tr[i].getElementsByTagName("td")[3]).children[0];
      currentAccount  = (tr[i].getElementsByTagName("td")[4]).children[0];
      checkbox        = (tr[i].getElementsByTagName("td")[6]).children[0];
      links           = (tr[i].getElementsByTagName("td")[7]);

      if(checkbox.checked) {
        currentUsername.contentEditable = true;
        currentEmail.contentEditable    = true;
        tr[i].style.background = "#eee"
        if (currentDivision.disabled)  currentDivision.removeAttribute("disabled");
        if (currentAccount.disabled)  currentAccount.removeAttribute("disabled");
        links.style.display = "";
      }
      else {
        tr[i].style.background = ""
        currentUsername.contentEditable = false;
        currentEmail.contentEditable    = false;
        if (!currentDivision.disabled)  currentDivision.setAttribute("disabled", true);
        if (!currentAccount.disabled)   currentAccount.setAttribute("disabled", true);
        links.style.display = "none";
      }
    }
  }
}

function updateUser(employeerName) {
  var table, tr, td, i, j, uDivision, uAccountType;

  table = document.getElementById("table");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td && td.innerText == employeerName) {
      uDivision = (tr[i].getElementsByTagName("td")[2]).children[0];
      uAccountType = (tr[i].getElementsByTagName("td")[3]).children[0];
      console.log(uDivision.value)
      console.log(uAccountType.value)
      for (j = 0; j < 4; j++) 
        if (j != 2 && j != 3) 
          console.log(tr[i].getElementsByTagName("td")[j].innerText)
    }
  }
}

$(function() {
  $('#datepicker1').datepicker();
  $('#datepicker2').datepicker();
});
