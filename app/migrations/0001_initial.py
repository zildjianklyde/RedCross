# Generated by Django 5.1.5 on 2025-01-18 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('blood', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
            ],
        ),
    ]
