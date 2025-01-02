# Generated by Django 5.1.1 on 2025-01-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('blood_type', models.CharField(max_length=3)),
                ('contact_info', models.CharField(max_length=255)),
                ('last_donation_date', models.DateField()),
            ],
        ),
    ]