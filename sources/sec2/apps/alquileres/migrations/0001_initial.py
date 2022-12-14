# Generated by Django 4.1.1 on 2022-11-28 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0001_initial'),
        ('afiliados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_alquiler', models.DateTimeField(auto_now_add=True, null=True)),
                ('afiliado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alquileres', to='afiliados.afiliado')),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('capacidad', models.PositiveIntegerField(help_text='capacidad maxima del salon')),
                ('precio', models.DecimalField(decimal_places=2, help_text='costo del alquiler', max_digits=10)),
                ('fecha_baja', models.DateTimeField(auto_now_add=True, null=True)),
                ('encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salon', to='personas.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Pago_alquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateTimeField(auto_now_add=True, null=True)),
                ('alquiler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='alquileres.alquiler')),
            ],
        ),
        migrations.AddField(
            model_name='alquiler',
            name='salon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alquileres', to='alquileres.salon'),
        ),
    ]
