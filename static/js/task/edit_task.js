function editTask(taskId) {
  var taskStatus;

  table = document.getElementById("task-table");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td && td.innerText == taskId) {
      taskStatus  = tr[i].getElementsByTagName("td")[6];
      checkbox    = (tr[i].getElementsByTagName("td")[7]).children[0];
      links       = tr[i].getElementsByTagName("td")[8];

      if(checkbox.checked) {
        if (taskStatus.innerText == "منجزة") taskRate.removeAttribute("disabled")
        tr[i].style.background = "#eee"
        links.style.display = "";
      }
      else {
        tr[i].style.background = ""
        tr[i].style.background = ""
        links.style.display = "none";
      }
    }
  }
}

function editDirectorTask(taskId) {
  var taskTitle, admins,

  table = document.querySelector(".director-tasks-table");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td && td.innerText == taskId) {
      taskTitle = tr[i].getElementsByTagName("td")[1];
      admins    = (tr[i].getElementsByTagName("td")[2]).children[0];
      checkbox  = (tr[i].getElementsByTagName("td")[4]).children[0];
      links     = tr[i].getElementsByTagName("td")[5];

      if(checkbox.checked) {
        taskTitle.contentEditable = true;
        if (admins.disabled) admins.removeAttribute("disabled");
        tr[i].style.background = "#eee"
        links.style.display = "";
      }
      else {
        tr[i].style.background = ""
        taskTitle.contentEditable = false;
        if (!admins.disabled) admins.setAttribute("disabled", true);
        tr[i].style.background = ""
        links.style.display = "none";
      }
    }
  }
}