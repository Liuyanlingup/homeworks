# Generated by Django 3.2.25 on 2024-10-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('stu_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('stu_name', models.CharField(max_length=20)),
                ('stu_pwd', models.CharField(max_length=20)),
            ],
        ),
    ]
