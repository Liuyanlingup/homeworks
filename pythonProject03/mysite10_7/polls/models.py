from django.db import models

# Create your models here.
class StudentInfo(models.Model):
    stu_id = models.CharField(primary_key=True, max_length=20)
    stu_name = models.CharField(max_length=20)
    stu_pwd = models.CharField(max_length=20)



# -----
from django.db import models

# 学生表
class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100, unique=True)  # 学号设为唯一
    score = models.FloatField(default=0)  # 积分允许为小数
    attendance_count = models.IntegerField(default=0)  # 到课次数
    called_count = models.IntegerField(default=0)  # 被点名次数
    # protected = models.BooleanField(default=False)  # 是否有保护权

    def __str__(self):
        return self.name
