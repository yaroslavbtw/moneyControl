# Generated by Django 4.1.5 on 2023-02-11 20:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='expenses',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Expenses'},
        ),
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
