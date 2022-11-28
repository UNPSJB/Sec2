# Generated by Django 4.1.1 on 2022-11-28 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictado',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, help_text='costo', max_digits=10),
            preserve_default=False,
        ),
    ]
