# Generated by Django 4.1.1 on 2024-05-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0010_profesor_dictados_alter_dictado_legajo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictado',
            name='legajo',
            field=models.CharField(default='8243', max_length=4, null=True),
        ),
    ]