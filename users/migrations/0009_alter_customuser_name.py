# Generated by Django 4.1.4 on 2023-01-04 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customuser_datetime_created_alter_customuser_bonus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=155),
        ),
    ]
