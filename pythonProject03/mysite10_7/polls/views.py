from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
import random
import pandas as pd
from django.db.models import Window, F
from django.db.models.functions import Rank
# 导入表单
from .forms import UploadFileForm
# Create your views here.
def toLogin_view(request):
    return render(request,'login.html')
def Login_view(request):
   u=request.POST.get("user",'')
   p=request.POST.get("pwd",'')

   if u and p:
      c=StudentInfo.objects.filter(stu_name=u,stu_pwd=p).count()
      if c >= 1:
         return HttpResponse("登录成功！")
      else:
         return HttpResponse("账号密码错误！")
   else:
      return HttpResponse("请输入正确的账号和密码！")

def toregister_view(request):
      return render(request, 'register.html')

   # #点击注册后做的逻辑判断
def register_view(request):
      u = request.POST.get("user", '')
      p = request.POST.get("pwd", '')
      if u and p:
         stu = StudentInfo(stu_id=random.choice('0123456789'),stu_name=u, stu_pwd=p)
         stu.save()
         return HttpResponse("注册成功")
      else:
         return HttpResponse("请输入完整的账号和密码！")

#导入excel
# 上传学生名单的视图
def upload_students(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 读取上传的 Excel 文件
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)  # 使用 pandas 读取 Excel 文件

            # 遍历 DataFrame，将每个学生保存到数据库
            for _, row in df.iterrows():
                student_id = row['student_id']
                name = row['name']
                Student.objects.get_or_create(student_id=student_id, name=name)  # 如果学生已存在则不创建

            return redirect('roll_call')  # 完成后重定向到点名页面
    else:
        form = UploadFileForm()

    return render(request, 'upload_students.html', {'form': form})  # 渲染上传页面

# 开始点名的视图
def roll_call(request):
    students = Student.objects.all()  # 获取所有学生
    selected_student = None  # 初始化被选中的学生

    # 当教师点击“开始点名”按钮时
    if request.method == 'POST' and 'start_roll_call' in request.POST:
        # 设置权重：总分越高，被点名的概率越低
        weights = [1 / (student.score + 1) for student in students]  # 根据分数调整被点名概率
        selected_student = random.choices(students, weights=weights, k=1)[0]  # 随机选择一个学生
        request.session['selected_student_id'] = selected_student.student_id  # 存储被点名学生的ID到session中
        return redirect('confirm_roll_call')  # 跳转到确认点名页面

    return render(request, 'roll_call.html', {'selected_student': selected_student})  # 渲染点名页面

# 确认点名的视图
# def confirm_roll_call(request):
#     # 从 session 中获取被点名的学生
#     student_id = request.session.get('selected_student_id')
#     student = get_object_or_404(Student, student_id=student_id)
#
#     if request.method == 'POST':
#         # 学生是否到课
#         if 'attended' in request.POST:  # 如果选择了到课
#             student.score += 1  # 到课加1分
#             student.attendance_count += 1  # 到课次数加1
#
#             # 处理是否准确重复问题
#             if request.POST['question_repeat'] == 'accurate':
#                 student.score += 0.5  # 重复问题准确，加0.5分
#             else:
#                 student.score -= 1  # 重复问题不准确，扣1分
#
#             # 处理回答问题的准确性（0-3分）
#             answer_accuracy = float(request.POST.get('answer_accuracy', 0))
#             student.score += answer_accuracy  # 根据回答准确性加分
#         else:
#             student.score -= 5  # 未到课扣5分
#
#         student.save()  # 保存更新后的学生信息
#         return redirect('roll_call')  # 返回点名页面，进行下一轮点名
#
#     return render(request, 'confirm_roll_call.html', {'student': student})  # 渲染确认点名页面
def confirm_roll_call(request):
    student_id = request.session.get('selected_student_id')
    student = get_object_or_404(Student, student_id=student_id)
    protection_awarded = False  # 初始化保护权标志

    if request.method == 'POST':
        # 增加学生的被点名次数
        student.called_count += 1

        # 检查学生是否有“保护权”
        if student.called_count % 3 == 0:
            # 如果被点名次数是3的倍数，赋予保护权，自动加2分
            student.score += 2
            protection_awarded = True  # 设置保护权标志
            print(f"Student {student.name} ({student.student_id})获得保护权，自动加2分")
        else:
            # 学生是否到课
            if 'attended' in request.POST:  # 如果选择了到课
                student.score += 1  # 到课加1分
                student.attendance_count += 1  # 到课次数加1

                # 处理是否准确重复问题
                if request.POST['question_repeat'] == 'accurate':
                    student.score += 0.5  # 重复问题准确，加0.5分
                else:
                    student.score -= 1  # 重复问题不准确，扣1分

                # 处理回答问题的准确性（0-3分）
                answer_accuracy = float(request.POST.get('answer_accuracy', 0))
                student.score += answer_accuracy  # 根据回答准确性加分
            else:
                student.score -= 5  # 未到课扣5分

        # 保存更新后的学生信息
        student.save()
        return redirect('roll_call')  # 返回点名页面，进行下一轮点名

    return render(request, 'confirm_roll_call.html', {'student': student, 'protection_awarded': protection_awarded})  # 渲染确认点名页面




# 积分排行榜
def leaderboard(request):
    students = Student.objects.all().order_by('-score')  # 按分数降序排列
    return render(request, 'leaderboard.html', {'students': students})