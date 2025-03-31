# Generated by Django 5.1.3 on 2025-03-31 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(max_length=50)),
                ('weight', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('physician_id', models.ManyToManyField(related_name='physician', to='patients.patient')),
            ],
        ),
    ]
