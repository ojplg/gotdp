# Generated by Django 2.1.5 on 2019-02-08 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selection',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pool.Character'),
        ),
    ]