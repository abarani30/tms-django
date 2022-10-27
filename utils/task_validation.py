from typing_extensions import Self
import datetime

class TaskInputs:
    
    # class constructor
    def __init__(self, subject, start_date, end_date, employees) -> Self:
        self.subject    = subject
        self.start_date = start_date
        self.end_date   = end_date
        self.employees  = employees

    # used to invoke the the function
    def Validate(self) -> Self:
        self.isSubject()

    # check if the subject is empty or not
    def isSubject(self) -> Self:
        return self.isDate() if self.subject else self.isValid(False)
    
    # check if the start_date and end_date are empty or not
    def isDate(self) -> Self:
        return self.checkDateFormat() if self.start_date and self.end_date else self.isValid(False)
    
    # check the date format
    def checkDateFormat(self) -> Self:
        return self.compareDates() if datetime.datetime.strptime(self.start_date, "%Y-%m-%d") and datetime.datetime.strptime(self.end_date, "%Y-%m-%d") else self.isValid(True)

    # compare both the start_date and end_date
    def compareDates(self) -> Self:
        return self.checkEmployeesList() if self.start_date < self.end_date else self.isValid(False) 
    
    # check the list of employees
    def checkEmployeesList(self) -> Self:
        return self.isValid(True) if len(self.employees) != 0 else self.isValid(False)

    # after all return the boolean 
    def isValid(self, valid) -> bool:
        return valid 