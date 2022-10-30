from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from myapp.models import Task, Notification
from typing import Dict, List
from redmail import outlook
import datetime, ast, uuid

class SystemTasksView(View):
  template_name: str = "systems_tasks.html"
  employeesList: List[dict] = []
  task: List[dict] = []
  notification: List[dict] = []

  # =============== GET request will be handled below ======== */
  
  def get(self, request):
    notification  = Notification.objects.prefetch_related("emps")

    if not request.user.is_staff and (
      self.getCurrentTask(request.GET.get("receive_task")) or 
      self.getCurrentTask(request.GET.get("achieve_task"))
    ):
      return JsonResponse({"msg": "success"})
    
    if request.user.is_staff and (
      self.getCurrentTask(request.GET.get("confirm_task")) or
      self.getCurrentTask(request.GET.get("delete_task"))
    ):
      return JsonResponse({"msg": "success"})

    return render(request, self.template_name, 
      {
        "employees": self.getAllUsers(),
        "tasks": self.getAllTasks(),
        "unreadable": notification[0].countUnreadableNotifications(request)
      }
    )
  
  # ==================== End of get method ==================== */

  # =============== POST request will be handled below ======== */

  def post(self, request):
    if self.checkHTTPRequest(request):
      return JsonResponse({"errMsg": "لا يمكن ارسال هذا الطلب للخادم"})

    subject, start_date, end_date, employees = self.getFormData(request)
    if not self.valideTaskInputs(subject, start_date, end_date, employees):
      return JsonResponse({"errMsg": "لا يمكن تنفيذ طلبك"})
    start_day: str      = self.getDay(start_date)
    end_day: str        = self.getDay(end_date)
    self.employeesList  = self.isEmployee(employees)
    self.task           = self.createTask(subject, start_date, end_date, start_day, end_day)
    self.notification   = self.createNotification(subject)
    self.AssignAndNotify(self.task, self.notification)
    self.sendEmail(subject)

    return JsonResponse({
      "msg" : "تم تخصيص المهمه بنجاح",
    })
  
  # ==================== End of post method ==================== */

  # get all the active users 
  def getAllUsers(self) -> List[dict]:
    return [
      user for user in User.objects.all().select_related("profile") 
      if user.profile.division == "الانظمة" and user.is_active
    ]

  # get all the tasks in the current month 
  def getAllTasks(self) -> List[dict]:
    return [
      task 
      for task in Task.objects.prefetch_related("employees")
      .filter(start_date__range = (self.getFirstDayOfMonth(), self.getLastDayOfMonth()))
      .order_by("-created_at") 
      if task.user.profile.division == "الانظمة" and task.active
    ]

  # get the first day in a month
  def getFirstDayOfMonth(self) -> str:
    return str(datetime.date.today().replace(day=1))
  
  # get the last day in a month
  def getLastDayOfMonth(self) -> str:
    return str(datetime.date.today().replace(day=31))

  # check if the request
  def checkHTTPRequest(self, request) -> bool:
    return (request.META.get("HTTP_X_CSRFTOKEN") != request.POST.get("csrftoken") or 
    request.headers.get("X-Requested-With") != "XMLHttpRequest" or 
    not request.user.is_staff)
    
  # get the form data from ajax request
  def getFormData(self, request) -> str:
    subject     = request.POST.get("subject")
    start_date  = request.POST.get("start_date")
    end_date    = request.POST.get("end_date")
    employees   = ast.literal_eval(request.POST.get("employees"))
    return subject, start_date, end_date, employees

  # used to validate the task inputs
  def valideTaskInputs(self, subject, start_date, end_date, employees) -> bool:
    return bool(
      subject and 
      start_date and 
      end_date and 
      self.compareDates(start_date, end_date) and 
      len(employees) != 0 and 
      len(self.isEmployee(employees)) == len(employees)
    )

  # used to compare both the start_date and end_date
  def compareDates(self, start_date, end_date) -> bool:
    return start_date <= end_date

  # used to get the day from the current date
  def getDay(self, currentDate) -> str:
    year, month, day = (int(x) for x in currentDate.split('-'))    
    return self.convertDayName((datetime.date(year, month, day)).strftime("%A"))
  
  # used to convert the day name from english to arabic
  def convertDayName(self, day) -> str:
    week: Dict[str] = {
      "Sunday": "الاحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء",
      "Wednesday": "الاربعاء", "Thursday": "الخميس", "Friday": "الجمعه", 
      "Saturday": "السبت"
    }
    return week[day]

  # used to check if the username exists or not
  def isEmployee(self, employees) -> List[dict]:
    return [
      User.objects.get(username=employee) for employee in employees
      if User.objects.filter(username=employee).exists()
    ]

  # used to create and save a new task
  def createTask(self, subject, start_date, end_date, start_day, end_day) -> List[dict]:
    return Task.objects.create(
      user        = self.request.user , subject   = subject,
      start_date  = start_date        , end_date  = end_date,
      start_day   = start_day         , end_day   = end_day,
      no_of_users = len(self.employeesList)
    )

  # used to create and save a new notification
  def createNotification(self, subject) -> List[dict]:
    return Notification.objects.create(user = self.request.user, message = subject)
  
  # used to assign the task and send notification to each employee 
  def AssignAndNotify(self, task, notification) -> any:
    for employee in self.employeesList:
      task.employees.add(employee)
      notification.emps.add(employee)

  # used to send emails for each employee
  def sendEmail(self, subject) -> any:
    for employee in self.employeesList:
      outlook.username = self.request.user.email
      outlook.password = "prestige1"
      outlook.send(
        receivers=[employee.email],
        subject=f"{subject} {uuid.uuid4()}",
        html=f"<b>{subject}</b><br>يرجى النقر على <b>استلمت</b> في حال تم استلامك لهذه المهمه",
      )
    
  # used to get the current task according to the task id
  def getCurrentTask(self, taskId) -> List[dict]:
      if self.request.GET.get("receive_task"):
        return self.updateReceived(Task.objects.filter(pk=taskId).prefetch_related("employees"))
      return self.updateTaskStatus(Task.objects.filter(pk=taskId).prefetch_related("employees"))

  # used to update the received field of the current task
  def updateReceived(self, task) -> bool:
    if task:
      task[0].received = True
      task[0].save()
      return True 
    return False

  # used to indicate if the update to staff user or normal user
  def updateTaskStatus(self, task) -> any:
    if self.request.user.is_staff:
      return self.updateStatusByStaff(task)
    return self.updateStatusByUser(task)  
  
  # used to update the task status by staff (admin)
  def updateStatusByStaff(self, task):
    if task and self.request.GET.get("delete_task"):
      return self.deactivateTask(task[0])
    if task and task[0].status == "بأنتظار الموافقة":
      return self.finalTaskUpdate(task[0], "منجزة")
    return False
  
  # used to update the task status by employee
  def updateStatusByUser(self, task):
    if task and task[0].status == "غير منجزة":
      return self.finalTaskUpdate(task[0], "بأنتظار الموافقة")
    return False

  # used to eliminates the duplication in the previous two methods
  def finalTaskUpdate(self, task, status):
    task.status = status
    task.save()
    return True
  
  # used to deactivate (delete) the current task
  def deactivateTask(self, task):
    if task.status != "منجزة":
      task.active = False
      task.save()
      return True
    return False