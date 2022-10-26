var taskForm        = document.getElementById("task-form");
var csrf            = document.getElementsByName("csrfmiddlewaretoken");
var taskSubject     = document.getElementById("task-subject");
var startDate       = document.getElementById("start-date");
var endDate         = document.getElementById("end-date");
var taskEmployees   = document.querySelectorAll("input[id='employees']");


if (taskForm !== null) {
    taskForm.addEventListener("submit", (e)=> {
        e.preventDefault();
 
        var employees = [];
        for (let i = 0; i < taskEmployees.length; i++) {
            if (taskEmployees[i].checked) employees.push(taskEmployees[i].value);
        }

        const formData = new FormData();
        formData.append('csrftoken', csrf[0].value);
        formData.append("subject", taskSubject.value);
        formData.append("start_date", startDate.value);
        formData.append("end_date", endDate.value);
        formData.append("employees", employees);


        $.ajax({
            url: '/tasks/systems/',
            type: "POST",
            enctype: "multipart/form-data",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrf[0].value,  
            },
            mode: "same-origin",
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        })

    })
}