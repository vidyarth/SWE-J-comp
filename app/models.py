from django.urls import reverse
from enum import unique
from multiprocessing.sharedctypes import Value
from platform import mac_ver
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from grpc import Status
# Create your models here.



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, user_name, email, name, password, user_type, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError("Super user invalid")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Super user invalid")
        return self.create_user(user_name, email, name, password, user_type, **other_fields)

    def create_user(self, user_name, email, name, password, user_type, **other_fields):
        if not email:
            raise ValueError(gettext_lazy("You must provide an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          name=name, user_type=user_type, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    mylist = [('1', "admin"), ('2', "student"),
              ('3', "teacher"), ('4', "parent")]
    user_type = models.CharField(max_length=15, choices=mylist)
    start_date = models.DateField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'name', 'user_type']

    def __str__(self):
        return self.user_name


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    phone_no = models.CharField(max_length=10)

    def __str__(self):
        return str(self.admin)


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    phone_no = models.CharField(max_length=10)
    subject = models.CharField(max_length = 20)

    def __str__(self):
        return str(self.admin)


class Tuitions(models.Model):
    id = models.AutoField(primary_key=True)
    tuition_name = models.CharField(max_length=25)
    tuition_owner = models.ForeignKey(Admin, on_delete=models.CASCADE)
    place = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    def __str__(self):
        return self.tuition_name

    def get_absolute_url(self):
        return reverse('tuitions')
    

class Tuitions_and_staffs(models.Model):
    tution_id = models.ForeignKey(Tuitions,on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staffs,on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.tution_id) + "  | " +str(self.staff_id))
    
    def get_absolute_url(self):
        return reverse('tuitions')

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    tuition_id = models.ForeignKey(Tuitions, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.course_name

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    gender_list = [('1', "male"), ('2', "female"),
              ('3', "others")]
    gender = models.CharField(max_length=15, choices=gender_list)
    profile_pic = models.FileField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    phone_no = models.CharField(max_length=10)

    def __str__(self):
        return str(self.admin)

class students_and_tuitions(models.Model):
    students_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    tuitions_id = models.ForeignKey(Tuitions,on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.tuitions_id) + "  | " + str(self.students_id))
    
    def get_absolute_url(self):
        return reverse('tuitions')

class Parents(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return (str(self.admin))
class Parents_and_wards(models.Model):
    parent_id = models.ForeignKey(Parents,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    def __str__(self):
        return (str(self.parent_id) + "  | " + str(self.student_id))

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255)
    tuition_id = models.ForeignKey(Tuitions, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    attendance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('staff_attendance', args=[str(self.id)])

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status_list = [('1', "present"), ('2', "absent")]
    status = models.CharField(max_length=20, choices=status_list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.student_id) 
    def get_absolute_url(self): 
        return reverse('staff_attendance', args=[str(self.attendance_id)])

class marks(models.Model):
    id = models.AutoField(primary_key = True)
    tuition_id = models.ForeignKey(Tuitions,on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('staff_marks', args=[str(self.id)])

class marks_report(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    marks_id = models.ForeignKey(marks, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    total_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.student_id)

    def get_absolute_url(self):
        return reverse('staff_marks', args=[str(self.marks_id)])

class materials(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.DO_NOTHING);
    topic = models.CharField(max_length=255);
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.topic)
    
    def get_absolute_url(self):
        return reverse('staff_marks', args=[str(self.marks_id)])

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == '1':
            Admin.objects.create(admin=instance)
        if instance.user_type == '2':
            Students.objects.create(admin=instance)
        if instance.user_type == '3':
            Staffs.objects.create(admin=instance,name = instance.name)
        if instance.user_type == '4':
            Parents.objects.create(admin=instance)

# @receiver(post_save, sender=NewUser)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.user_type == 1:
#         instance.admin.save()
#     if instance.user_type == 2:
#         instance.students.save()
#     if instance.user_type == 3:
#         instance.staffs.save()
#     if instance.user_type == 4:
#         instance.parents.save()
