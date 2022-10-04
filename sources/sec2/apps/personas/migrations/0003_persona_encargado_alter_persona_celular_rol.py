# Generated by Django 4.1.1 on 2022-10-03 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0002_persona_apellido_persona_celular_persona_cuil_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='encargado',
            field=models.BooleanField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='persona',
            name='celular',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveSmallIntegerField(choices=[(1, 'afiliado'), (2, 'profesor'), (3, 'alumno')])),
                ('desde', models.DateTimeField(auto_now_add=True)),
                ('hasta', models.DateTimeField(blank=True, null=True)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='personas.persona')),
            ],
        ),
    ]
