# Generated by Django 3.1.4 on 2020-12-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('I', 'Inverstor'), ('B', 'Borrower')], max_length=1),
        ),
    ]
