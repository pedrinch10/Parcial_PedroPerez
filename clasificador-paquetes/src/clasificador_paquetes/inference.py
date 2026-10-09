import csv
import pandas as pd
import os
from pathlib import Path
import joblib
from .contracts import Entrada, Salida
from pydantic import ValidationError


def leer_csv(ruta: Path) -> list[Entrada]:
    entradas = []
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            entradas.append(Entrada(**fila))

    if not entradas:
        raise ValueError("El CSV no tiene filas de datos")

    return entradas
    # TODO



def preprocesar(entrada: Entrada) -> list[float]:
    # TODO
    return [round(entrada.peso_kg, 1), entrada.distancia_km]


def cargar_modelo(ruta: Path):
    # TODO
    return joblib.load(ruta)
    


def predecir(entrada, modelo):
    # TODO
    matriz = [preprocesar(entrada)]

    categoria = modelo.predict(matriz)[0]
    probabilidades = modelo.predict_proba(matriz)[0]

    return Salida(
        id_paquete=entrada.id_paquete,
        categoria=str(categoria),
        confianza=float(max(probabilidades)),
    )


def guardar_csv(resultados, ruta):
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["id_paquete", "categoria", "confianza"])
        escritor.writeheader()
        for resultado in resultados:
            escritor.writerow(resultado.model_dump())


def ejecutar(entrada, modelo, salida):
    entradas = leer_csv(entrada)
    modelo_cargado = cargar_modelo(modelo)
    resultados = [predecir(e, modelo_cargado) for e in entradas]
    guardar_csv(resultados, salida)
    return resultados