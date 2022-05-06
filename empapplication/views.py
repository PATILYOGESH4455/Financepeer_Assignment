from django.shortcuts import render, redirect
from .models import Employee, UserImportData
from .forms import EmployeeForm
import json
from django.http import HttpResponse


def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/show")
            except:
                pass
    else:
        form = EmployeeForm()

    return render(request, "indexhome.html", {'form': form})


def show(request):
    employees = Employee.objects.all()
    form = EmployeeForm()
    return render(request, "show.html", {'employees': employees, 'form': form})


def update(request, emp_id):
    employee = Employee.objects.get(id=emp_id)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('/show')
    return render(request, "update.html", {'form': form, 'employee': employee})


def delete(request, emp_id):
    employee = Employee.objects.get(id=emp_id)
    employee.delete()
    return redirect("/show")


def jsonImportFun(request):
    try:
        file = request.FILES['fileupload']

    except:
        return HttpResponse('Please Select File')
        pass
    data = json.load(file)
    # print(data)
    # Iterating through the json
    # list
    # print('fsdafsdf',type(data))
    for i in data:
        user_id = i['userId']
        title = i['title']
        body = i['body']
        data_id = i['id']
        temp = UserImportData(UserId=user_id, data_id=data_id, title=title, body=body)
        temp.save()

    dataObj = UserImportData.objects.all()
    # contex = {dataObj:}
    for i in dataObj:
        print(i.data_id, i.UserId, i.title, i.body)
        return render(request, 'show.html', {'dataObj': dataObj})
    return redirect("/show")
