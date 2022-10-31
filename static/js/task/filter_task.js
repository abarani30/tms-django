function filterTasks() {
  console.log("ali")
  var status = document.getElementById("task-status").value;
  var employee = document.getElementById("employees").value;
  
  var table, tr, statusColumn, i, statusValue, employeesColumn, employees, isEmpty = 0;

  table = document.getElementById("task-table");
  tr    = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    employeesColumn   = tr[i].getElementsByTagName("td")[2];
    statusColumn      = tr[i].getElementsByTagName("td")[7];

    if (statusColumn && employeesColumn) {
      statusValue = statusColumn.innerText;

      if (employee != "الكل") {
        var employees = Array.from(employeesColumn.children[0].selectedOptions)
        .map(({ value }) => value);
        
        if (statusValue == status && employees.includes(employee)) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
          isEmpty ++;
          if (isEmpty == tr.length - 1) {
            alert("لا يوجد بيانات حسب اختياراتك")
            resetTable();
          }
        }
      }

      else {
        if (statusValue == status) {
          tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
            isEmpty ++;
            if (isEmpty == tr.length - 1) {
              alert("لا يوجد بيانات حسب اختياراتك")
              resetTable();
            }
          }
      }
    }
  }
}



function resetTable() {
  var table, tr;
  table = document.getElementById("task-table");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    tr[i].style.display = "";
  }
}