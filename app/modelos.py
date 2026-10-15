from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import AwareDatetime, BaseModel, field_validator


class Perfil(str, Enum):
    GENERAL = "general"
    ESTUDIANTE = "estudiante"
    ADULTO_MAYOR = "adulto_mayor"


class Validacion(BaseModel):
    id: str
    estacion: str
    fecha_hora: AwareDatetime


class SolicitudTarifa(BaseModel):
    tarjeta: str
    perfil: Perfil = Perfil.GENERAL
    validaciones: list[Validacion]

    @field_validator("validaciones")
    @classmethod
    def ids_unicos(cls, validaciones: list[Validacion]) -> list[Validacion]:
        ids = [validacion.id for validacion in validaciones]
        if len(ids) != len(set(ids)):
            raise ValueError("No puede haber dos validaciones con el mismo id")
        return validaciones


class Cobro(BaseModel):
    validacion_id: str
    fecha_hora: datetime
    tipo: Literal["tarifa", "transbordo", "transbordo_gratis"]
    valor: int


class RespuestaTarifa(BaseModel):
    tarjeta: str
    perfil: Perfil
    cobros: list[Cobro]
    total: int
