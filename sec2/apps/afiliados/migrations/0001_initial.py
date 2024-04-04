import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.funciones


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '__first__'),
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Afiliado',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.rol')),
                ('estado', models.PositiveSmallIntegerField(choices=[(1, 'Pendiente'), (2, 'Activo'), (3, 'Inactivo')], default=1)),
                ('razon_social', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='invalid_text', message='Sin caracteres especiales.', regex='^[A-Za-z0-9\\sñÑ]+$')])),
                ('categoria_laboral', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(code='invalid_text', message='Sin caracteres especiales.', regex='^[A-Za-z0-9\\sñÑ]+$')])),
                ('rama', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_text', message='Sin caracteres especiales.', regex='^[A-Za-z0-9\\sñÑ]+$')])),
                ('sueldo', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'El sueldo debe ser un valor positivo.')])),
                ('horaJornada', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cuit_empleador', models.CharField(help_text='Cuit sin puntos y guiones. Ej: 01234567899', max_length=11, validators=[django.core.validators.RegexValidator(code='invalid_numeric', message='Debe contener solo dígitos numéricos.', regex='^\\d+$')])),
                ('domicilio_empresa', models.CharField(help_text='Calle y numero', max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_text', message='Sin caracteres especiales.', regex='^[A-Za-z0-9\\sñÑ]+$')])),
                ('fechaAfiliacion', models.DateField(null=True, validators=[utils.funciones.validate_no_mayor_actual])),
                ('fechaIngresoTrabajo', models.DateField(validators=[utils.funciones.validate_no_mayor_actual])),
                ('localidad_empresa', models.CharField(choices=[('RAWSON', 'Rawson'), ('PUERTO MADRYN', 'Puerto Madryn'), ('GAIMAN', 'Gaiman'), ('TRELEW', 'Trelew')], default='TRELEW', max_length=30)),
                ('dictados', models.ManyToManyField(blank=True, related_name='afiliados', to='cursos.dictado')),
            ],
            bases=('personas.rol',),
        ),
        migrations.CreateModel(
            name='Familiar',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.rol')),
                ('activo', models.BooleanField(default=False)),
                ('dictados', models.ManyToManyField(blank=True, related_name='familiares', to='cursos.dictado')),
                ('lista_espera', models.ManyToManyField(blank=True, related_name='familiares_en_espera', to='cursos.dictado')),
            ],
            bases=('personas.rol',),
        ),
        migrations.CreateModel(
            name='RelacionFamiliar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_relacion', models.PositiveSmallIntegerField(choices=[(1, 'Conyugue'), (2, 'Hijo/a')])),
                ('afiliado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afiliados.afiliado')),
                ('familiar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afiliados.familiar')),
            ],
        ),
        migrations.AddField(
            model_name='afiliado',
            name='familia',
            field=models.ManyToManyField(blank=True, through='afiliados.RelacionFamiliar', to='afiliados.familiar'),
        ),
        migrations.AddField(
            model_name='afiliado',
            name='lista_espera',
            field=models.ManyToManyField(blank=True, related_name='afiliados_en_espera', to='cursos.dictado'),
        ),
    ]
