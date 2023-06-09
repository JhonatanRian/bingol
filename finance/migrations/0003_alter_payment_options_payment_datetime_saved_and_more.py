# Generated by Django 4.1.4 on 2023-01-02 04:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0002_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['datetime_saved'], 'verbose_name': 'Pagamento', 'verbose_name_plural': 'Pagamentos'},
        ),
        migrations.AddField(
            model_name='payment',
            name='datetime_saved',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='payment',
            table='payment',
        ),
    ]
