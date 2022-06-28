from re import template
from urllib.parse import urlencode
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import Tuitions,Tuitions_and_staffs,Staffs,NewUser,Attendance,AttendanceReport,marks,marks_report,materials,students_and_tuitions
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from django.urls import reverse_lazy
from .forms import RegisterForm
 
# Create your views here
class TuitionView(ListView):
    model = Tuitions
    template_name = "tuition.html"


class userregistration(CreateView):
    form_class = RegisterForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("login")

def staffs_in_tuition(request, name, t):
    context = {}
    context["dataset"] = Tuitions_and_staffs.objects.all().filter(tution_id = name)
    context["name"] = name
    context["t"] = t
    l = []
    for i in context["dataset"]:
        l.append(i.staff_id)
    context["staff"] = NewUser.objects.all().filter(user_name__in = l)
    p = []
    for i in context["staff"]:
        p.append(i.name)
    context["staff_req"] = Staffs.objects.all().filter(name__in = p)
    return render(request, "staffs_in_tuition.html",context)

def staff_view(request,tuition,staff):
    context = {}
    context["tuition"] = tuition
    context["staff"] = staff
    ss = Staffs.objects.all().filter(id = staff)
    context["ss"] = ss
    return render(request,"staff_view.html",context)

# def attendance(request,tuition):
#     context = {}
#     context["dataset"] = Attendance.objects.all().filter(tuition_id = tuition)
#     l = []
#     for i in context["dataset"]:
#         l.append(i.id)
#     print(l)
#     context["data"] = AttendanceReport.objects.all().filter(attendance_id__in = l)
#     return render(request, "attendance.html", context)


def staff_attendance(request, tuition):
    context = {}
    context["dataset"] = Attendance.objects.all().filter(tuition_id=tuition)
    l = []
    for i in context["dataset"]:
        l.append(i.id)
    print(l)
    context["data"] = AttendanceReport.objects.all().filter(
        attendance_id__in=l)
    return render(request, "attendance_staff.html", context)

def marks_view(request, tuition):
    context = {}
    context["dataset"] = marks.objects.all().filter(tuition_id=tuition)
    l = []
    for i in context["dataset"]:
        l.append(i.id)
    print(l)
    context["data"] = marks_report.objects.all().filter(
        marks_id__in=l)
    return render(request, "marks.html", context)


def marks_view_staff(request, tuition):
    context = {}
    context["dataset"] = marks.objects.all().filter(tuition_id=tuition)
    l = []
    for i in context["dataset"]:
        l.append(i.id)
    print(l)
    context["data"] = marks_report.objects.all().filter(
        marks_id__in=l)
    return render(request, "marks_staff.html", context)

def materials_view(request, staff):
    context = {}
    context["dataset"] = materials.objects.all().filter(staff_id=staff)
    return render(request, "materials.html", context)

class update_attendance(UpdateView):
    model = AttendanceReport
    template_name = "general_form.html"
    fields = ("status",)


class update_marks(UpdateView):
    model = marks_report
    template_name = "general_form.html"
    fields = ("marks_obtained","total_marks",)


def view_attendance(request, tuition):
    attendances = Attendance.objects.all().filter(tuition_id = tuition)
    context = {}
    context["object"] = attendances
    return render(request,"view_attendance.html",context)


def view_attendance_report(request, atd):
    attendances = AttendanceReport.objects.all().filter(attendance_id=atd)
    context = {}
    context["object"] = attendances
    return render(request, "attendance.html", context)


def view_attendance_report_staff(request, atd):
    attendances = AttendanceReport.objects.all().filter(attendance_id=atd)
    context = {}
    context["object"] = attendances
    return render(request, "attendance_staff.html", context)


def view_marks(request, tuition):
    attendances = marks.objects.all().filter(tuition_id=tuition)
    context = {}
    context["object"] = attendances
    return render(request, "view_marks.html", context)


def view_marks_report(request, marks):
    attendances = marks_report.objects.all().filter(marks_id=marks)
    context = {}
    context["object"] = attendances
    return render(request, "marks.html", context)


def view_marks_report_staff(request, marks):
    attendances = marks_report.objects.all().filter(marks_id=marks)
    context = {}
    context["object"] = attendances
    return render(request, "marks_staff.html", context)

class create_attendance(CreateView):
    model = Attendance
    template_name = "general_form.html"
    fields = "__all__"


class create_mark(CreateView):
    model = marks
    template_name = "general_form.html"
    fields = "__all__"

class create_attendance_report(CreateView):
    model = AttendanceReport
    template_name = "general_form.html"
    fields = "__all__"


class create_marks_report(CreateView):
    model = marks_report
    template_name = "general_form.html"
    fields = "__all__"

class create_materials(CreateView):
    model = materials
    template_name = "general_form.html"
    fields = "__all__"

class create_tuition(CreateView):
    model = Tuitions
    template_name = "general_form.html"
    fields = "__all__"

class add_staffs(CreateView):
    model = Tuitions_and_staffs
    template_name = "general_form.html"
    fields = "__all__"

class add_students(CreateView):
    model = students_and_tuitions
    template_name = "general_form.html"
    fields = "__all__"

def search(request):
    return render(request,"search.html",{})