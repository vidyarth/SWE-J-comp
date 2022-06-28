from csv import list_dialects
from django.contrib import admin
from .models import NewUser,Admin,Staffs,Students,Attendance,AttendanceReport,Tuitions,Courses,Parents,Parents_and_wards,students_and_tuitions,Tuitions_and_staffs,marks,marks_report,materials
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.admin import widgets
from django.urls import reverse
# Register your models here.

class UserAdminConfig(UserAdmin):
    ordering = ('-start_date',)
    list_display = ('email','user_name','is_active','user_type','is_staff',)
    fieldsets = ( (None,{'fields':('email','user_name','name',)}),
                  ('permissions', {'fields': ('is_staff', 'is_active',)}),
                  ('personal',{'fields':('user_type',)})
         )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','user_name','name','password1','password2','is_active','is_staff','user_type')
        }),
    )

admin.site.register(materials)
admin.site.register(NewUser,UserAdminConfig)

admin.site.register(Admin)

admin.site.register(Staffs)

admin.site.register(Students)

admin.site.register(Attendance)

admin.site.register(AttendanceReport)

admin.site.register(Tuitions)

admin.site.register(Courses)

admin.site.register(Parents)
admin.site.register(Parents_and_wards)
admin.site.register(Tuitions_and_staffs)
admin.site.register(students_and_tuitions)
admin.site.register(marks)
admin.site.register(marks_report)

