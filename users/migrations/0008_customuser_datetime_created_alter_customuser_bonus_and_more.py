# Generated by Django 4.1.4 on 2023-01-03 18:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data de criação '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bonus',
            field=models.DecimalField(blank=True, decimal_places=2, default=10.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=models.CharField(max_length=14, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='money',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7),
        ),
    ]
