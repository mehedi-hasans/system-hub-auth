# Generated by Django 4.2.7 on 2023-11-30 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='course_id',
            new_name='courseid',
        ),
    ]
