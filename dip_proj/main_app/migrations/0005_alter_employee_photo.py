# Generated by Django 4.0.3 on 2022-04-28 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_timesheet_task_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
