from django import forms  # 导入 Django 的表单模块

# 定义文件上传表单类
class UploadFileForm(forms.Form):
    # 定义一个 FileField 用于处理文件上传，label 是显示在表单中的标签
    file = forms.FileField(label="Select an Excel file")
