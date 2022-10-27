var taskForm        = document.getElementById("task-form");
var csrf            = document.getElementsByName("csrfmiddlewaretoken");
var taskSubject     = document.getElementById("task-subject");
var startDate       = document.getElementById("start-date");
var endDate         = document.getElementById("end-date");
var taskEmployees   = document.querySelectorAll("input[id='employees']");
var start_date, end_date;

if (taskForm !== null) {
    taskForm.addEventListener("submit", (e)=> {
        e.preventDefault();
 
        var employees = [];
        for (let i = 0; i < taskEmployees.length; i++) {
            if (taskEmployees[i].checked) employees.push(taskEmployees[i].value);
        }

        if (taskSubject.value && startDate.value && endDate.value && taskEmployees.length != 0) {
            
            start_date  = changeDateFormat(startDate.value);
            end_date    = changeDateFormat(endDate.value);
            console.log(start_date, end_date);

            const formData = new FormData();
            
            formData.append('csrftoken', csrf[0].value);
            formData.append("subject", taskSubject.value);
            formData.append("start_date", start_date);
            formData.append("end_date", end_date);
            formData.append("employees", JSON.stringify(employees));

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
                success:(response) => {
                    console.log(response);
                },
                cache: false,
                contentType: false,
                processData: false
            });
        }

    })
}

function changeDateFormat(currentDate) {
    var date  = new Date(currentDate),
    mnth      = ("0" + (date.getMonth() + 1)).slice(-2),
    day       = ("0" + date.getDate()).slice(-2);
    return [date.getFullYear(), mnth, day].join("-")
}