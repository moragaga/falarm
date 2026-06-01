"""
Default identities for fallback configuration.

This module defines a constant `IDENTITIES_FALLBACK` containing a tuple of
default `Identity` instances. Each `Identity` represents a system user with
predefined attributes such as id, name, email, profile, and activation status.
The fallback identities are typically used as a predefined configuration
fallback for environments where no other user configurations are available.

Attributes
----------
IDENTITIES_FALLBACK : tuple of Identity
    A tuple containing default `Identity` instances. Each `Identity` includes
    attributes like id (generated using `uuid4`), name, email, profile (from
    `Profile.ADMINISTRADOR`), and an active status.
"""

from __future__ import annotations

from uuid import uuid4

from src.features.configuration.models import Profile

from ..models.identity import Identity

IDENTITIES_FALLBACK: tuple[Identity, ...] = (
    Identity(
        id=uuid4().__str__(),
        name='Gerardo Moraga Gajardo',
        email='gmoraga.glo@aminerals.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Josefa Andrea Parra Videla',
        email='jparravi@pelambres.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Maria Jesus Campos Andrade',
        email='mcamposa@pelambres.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Sofía Andrea Barrientos Rebolledo',
        email='sbarrientos.glo@aminerals.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Carlos Alejandro Loyola Pino',
        email='glocloyola@eeccmlp.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Fernanda Macarena Quinteros Beltran',
        email='fquinteros@pelambres.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Carolina Espinoza',
        email='cespinoza.acc@aminerals.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
)
