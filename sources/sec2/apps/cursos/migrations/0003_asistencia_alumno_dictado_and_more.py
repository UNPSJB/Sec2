# Generated by Django 4.1.1 on 2022-12-02 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0002_dictado_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia_alumno',
            name='dictado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cursos.dictado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asistencia_alumno',
            name='fecha_asistencia_alumno',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='asistencia_profesor',
            name='fecha_asistencia_profesor',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
