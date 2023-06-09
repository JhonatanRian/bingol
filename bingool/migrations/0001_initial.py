# Generated by Django 4.1.4 on 2022-12-21 00:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação ')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('value', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor')),
                ('initials', models.CharField(max_length=2, verbose_name='Iniciais')),
                ('num_balls', models.IntegerField(verbose_name='Numero de bolas para conseguir este prêmio')),
            ],
            options={
                'verbose_name': 'Prêmio',
                'verbose_name_plural': 'Prêmios',
                'db_table': 'award',
            },
        ),
        migrations.CreateModel(
            name='Ball',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação ')),
                ('number', models.IntegerField(verbose_name='Bola')),
                ('drawn', models.BooleanField(default=False, verbose_name='Sorteado')),
            ],
            options={
                'verbose_name': 'Bola',
                'verbose_name_plural': 'Bolas',
                'db_table': 'ball',
            },
        ),
        migrations.CreateModel(
            name='BallsCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação ')),
                ('ball', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bingool.ball')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bingo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação ')),
                ('ball_drawn', models.IntegerField(verbose_name='Bola sorteada')),
            ],
            options={
                'verbose_name': 'Bingo',
                'verbose_name_plural': 'Bingos',
                'db_table': 'bingo',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação ')),
                ('state', models.CharField(choices=[('new', 'Nova'), ('inlive', 'Em jogo'), ('finalized', 'Fora de jogo')], default='new', max_length=100, verbose_name='Estado da cartela')),
                ('bought', models.BooleanField(default=False, verbose_name='Comprado')),
                ('balls', models.ManyToManyField(related_query_name='cards', through='bingool.BallsCards', to='bingool.ball', verbose_name='Bolas')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cartela',
                'verbose_name_plural': 'Cartelas',
                'db_table': 'card',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação ')),
                ('datetime_to_start', models.DateTimeField(verbose_name='Data e o Horario a ser iniciado')),
                ('date_to_start', models.DateField(verbose_name='Data a ser iniciada')),
                ('started', models.BooleanField(default=False, verbose_name='iniciou')),
                ('finalized', models.BooleanField(default=False, verbose_name='finalizou')),
                ('automatic', models.BooleanField(default=False, verbose_name='Sorteio automatico')),
                ('unitary_value_card', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Unidade da cartela')),
                ('number_cards_allowed', models.IntegerField(verbose_name='Numero de cartelas permitida por usuario')),
                ('value_award_all', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor total do prêmio')),
                ('results', models.JSONField(blank=True, verbose_name='dados da partida')),
            ],
            options={
                'verbose_name': 'Partida',
                'verbose_name_plural': 'Partidas',
                'db_table': 'match',
            },
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação ')),
                ('amount_received', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Valor a receber')),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingool.award')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingool.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vencedor',
                'verbose_name_plural': 'Vencedores',
                'db_table': 'winner',
            },
        ),
        migrations.AddField(
            model_name='ballscards',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bingool.card'),
        ),
        migrations.AddField(
            model_name='ball',
            name='bingo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingool.bingo'),
        ),
        migrations.AddField(
            model_name='award',
            name='_match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingool.match'),
        ),
    ]
