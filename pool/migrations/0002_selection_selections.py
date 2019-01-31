# Generated by Django 2.1.5 on 2019-01-31 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome', models.CharField(choices=[('L', 'Lives'), ('D', 'Dies')], max_length=1)),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pool.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Selections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picks', models.ManyToManyField(to='pool.Selection', verbose_name='list of selections')),
            ],
        ),
    ]
