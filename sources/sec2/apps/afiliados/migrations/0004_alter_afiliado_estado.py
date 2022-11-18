# Generated by Django 4.1.1 on 2022-11-13 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afiliados', '0003_alter_afiliado_cuit_empleador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afiliado',
            name='estado',
            field=models.PositiveSmallIntegerField(choices=[(1, 'pendiente de aceptación'), (2, 'activo'), (3, 'inactivo')]),
        ),
    ]
