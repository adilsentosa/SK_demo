# Generated by Django 4.0.6 on 2023-06-22 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jadwal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tugas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tugas')),
                ('waktu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.hari')),
            ],
        ),
    ]
