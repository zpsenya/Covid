# Generated by Django 4.1.2 on 2022-10-30 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='id_doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.users'),
        ),
    ]