# Generated by Django 2.2.5 on 2019-09-07 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=5, verbose_name='NAME')),
                ('todo', models.CharField(max_length=50, verbose_name='TODO')),
            ],
        ),
    ]
