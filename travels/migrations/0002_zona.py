# Generated by Django 3.1.7 on 2021-03-13 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('descripcion', models.CharField(blank=True, max_length=256, null=True)),
                ('latitud', models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True)),
                ('longitud', models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True)),
            ],
        ),
    ]
