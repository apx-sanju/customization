# Generated by Django 5.0.3 on 2024-04-11 12:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Product Name')),
                ('price', models.IntegerField()),
                ('cat', models.IntegerField(choices=[(1, 'Mobile'), (2, 'Shoes'), (3, 'Cloths')], verbose_name='Category')),
                ('pdetails', models.CharField(max_length=50, verbose_name='Product Details')),
                ('is_active', models.BooleanField(default=True)),
                ('pimage', models.ImageField(upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(max_length=50)),
                ('qty', models.IntegerField(default=1)),
                ('amt', models.FloatField()),
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
