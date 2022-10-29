function achieveTask(taskId) {
  if (taskId) {
    $.ajax({
      type: "GET",
      url: `/tasks/systems/?achieve_task=${taskId}`,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
      mode: "same-origin",
      success: function(response) {
        console.log(response)
        window.location.reload();
      },
      cache: false,
      contentType: false,
      processData: false

    }
  )};    
}