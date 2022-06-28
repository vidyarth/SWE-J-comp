from django.urls import path, include
from .views import TuitionView, add_staffs, add_students, create_attendance_report, create_mark, create_marks_report, create_materials, create_tuition, search,staffs_in_tuition,userregistration,marks_view,materials_view,update_attendance,staff_attendance,marks_view_staff,update_marks,staff_view,view_attendance,view_attendance_report,view_attendance_report_staff,view_marks,view_marks_report,view_marks_report_staff,create_attendance

urlpatterns = [
    path("",TuitionView.as_view(),name = "tuitions"),
    path("create_tuition/", create_tuition.as_view(), name="create_tuitions"),
    path("add_staff/", add_staffs.as_view(), name="add_staffs"),
    path("add_student/", add_students.as_view(), name="add_student"),
    path("staffs-in-tuitions/<int:name>/<str:t>",staffs_in_tuition,name ="staffs_in_tuitions"),
    path("attendance/<int:atd>",view_attendance_report,name ="attendance"),
    path("marks/<int:marks>", view_marks_report, name="marks"),
    path("materials/<int:staff>", materials_view, name="materials"),
    path("login/", include("django.contrib.auth.urls")),
    path("staff_attendance/<int:atd>",view_attendance_report_staff,name="staff_attendance"),
    path("staff_marks/<int:marks>",view_marks_report_staff, name="staff_marks"),
    path("update-attendance/<int:pk>/",update_attendance.as_view(),name="update-attendace"),
    path("update-marks/<int:pk>/",update_marks.as_view(), name="update-marks"),
    path("reg", userregistration.as_view(), name="reg"),
    path("staff-view/<int:tuition>/<int:staff>/",staff_view,name="staff_view"),
    path("view-attendance/<int:tuition>/",view_attendance,name = "view_attendance"),
    path("view-marks/<int:tuition>/",
         view_marks, name="view_marks"),
    path("add_attendance/",create_attendance.as_view(),name="create_attendance"),
    path("add_marks/", create_mark.as_view(), name="create_marks"),
    path("add_attendance_report/", create_attendance_report.as_view(), name="create_attendance_report"),
    path("add_marks_report/", create_marks_report.as_view(),
         name="create_marks_report"),
    path("add_materials/", create_materials.as_view(),
         name="create_materials"),
    path("search/",search,name="search")
    
]
