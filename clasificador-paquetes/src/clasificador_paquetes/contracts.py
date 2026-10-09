import pandas as pd
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Entrada(BaseModel):
    # TODO
    model_config = ConfigDict(extra="forbid")
    id_paquete: str = Field()
    peso_kg: float = Field(ge=0, le=30)
    distancia_km: float = Field(ge=0, le=200)
    
    pass

#falta eliminar espacios en id_paquete y validar que no sea vacio

class Salida(BaseModel):
    # TODO
    model_config = ConfigDict(extra="forbid")
    id_paquete: str = Field(min_length=1)
    categoria: Literal["Normal", "Urgente"] 
    confianza: float = Field(ge=0, le=1)
    pass


