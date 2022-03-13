# Generated by Django 4.0.3 on 2022-03-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('Address', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('Xray_image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
