import pytest 
import unittest
from apps.personas.models import Persona


@pytest.mark.django_db
def test_persona_creation():
    persona_prueba = Persona.objects.create(
        dni = "12345678",
        cuil = "12345678912",
        nombre = "nombre1",
        apellido = "apellido1",
        fecha_nacimiento = "1991-01-01",
        estado_civil = 1
    )
    assert persona_prueba.dni == "12345678"

@pytest.mark.django_db
def test_persona_creation_fail():
    persona_prueba = Persona.objects.create(
        cuil = "12345678912",
        nombre = "nombre1",
        apellido = "apellido1",
        fecha_nacimiento = "1991-1-1",
        estado_civil = 1
    )

@pytest.mark.django_db
def test_persona_instancia():
    persona_prueba = Persona.objects.create(
        dni = "12345678",
        cuil = "12345678912",
        nombre = "nombre1",
        apellido = "apellido1",
        fecha_nacimiento = "1991-1-1",
        estado_civil = 1
    )
    assert isinstance(persona_prueba, Persona)
