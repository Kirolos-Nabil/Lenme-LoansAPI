# Generated by Django 4.2.4 on 2023-08-28 11:43

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
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_balance', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_amount', models.FloatField()),
                ('loan_period', models.PositiveIntegerField()),
                ('annual_interest_rate', models.FloatField(blank=True, null=True)),
                ('lenme_fee', models.FloatField()),
                ('total_loan_amount', models.FloatField(blank=True, null=True)),
                ('funded_date', models.DateTimeField(blank=True, null=True)),
                ('loan_status', models.CharField(choices=[('Pending', 'Pending'), ('Funded', 'Funded'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.borrower')),
                ('investor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_app.investor')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_duedate', models.DateField()),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('amount', models.FloatField()),
                ('is_completed', models.BooleanField(default=False)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.loan')),
            ],
        ),
    ]
