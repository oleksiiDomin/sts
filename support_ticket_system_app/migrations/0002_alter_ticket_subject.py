# Generated by Django 4.2.16 on 2024-09-06 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_ticket_system_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='subject',
            field=models.TextField(max_length=100, verbose_name='Subject'),
        ),
    ]
