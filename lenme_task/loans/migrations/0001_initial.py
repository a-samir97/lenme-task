# Generated by Django 3.1.4 on 2020-12-16 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_amount', models.FloatField(default=0)),
                ('loan_period', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('F', 'Funded'), ('C', 'Completed'), ('R', 'Requested')], default='R', max_length=1)),
                ('total_loan_amount', models.PositiveIntegerField()),
                ('borrower_accepted_at', models.DateField()),
            ],
        ),
    ]
