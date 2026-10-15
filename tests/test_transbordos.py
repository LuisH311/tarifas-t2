import json
from pathlib import Path

import pytest

from app.modelos import Perfil, SolicitudTarifa
from app.tarifas import aplicar_descuento, calcular_tarifa


def calcular(fechas, perfil="general"):
    return calcular_tarifa(SolicitudTarifa(
        tarjeta="T-1", perfil=perfil,
        validaciones=[
            {"id": str(i), "estacion": "E01", "fecha_hora": fecha}
            for i, fecha in enumerate(fechas)
        ],
    ))


@pytest.mark.parametrize("perfil,base,transbordo", [
    (Perfil.GENERAL, 3200, 500),
    (Perfil.ESTUDIANTE, 2100, 350),
    (Perfil.ADULTO_MAYOR, 1450, 250),
])
def test_descuentos_exactos_y_empates(perfil, base, transbordo):
    assert aplicar_descuento(3200, perfil) == base
    assert aplicar_descuento(500, perfil) == transbordo
    assert aplicar_descuento(0, perfil) == 0


@pytest.mark.parametrize("ultima,esperado", [
    ("08:29:59", 500), ("08:30:00", 500),
    ("08:30:00.000001", 3200),
])
def test_limite_90_minutos(ultima, esperado):
    respuesta = calcular(["2025-03-10T07:00:00-05:00", f"2025-03-10T{ultima}-05:00"])
    assert respuesta.cobros[1].valor == esperado


def test_ventana_no_se_reinicia_con_transbordo():
    respuesta = calcular([f"2025-03-10T{hora}-05:00" for hora in ["07:00:00", "08:00:00", "08:31:00"]])
    assert [c.valor for c in respuesta.cobros] == [3200, 500, 3200]


def test_maximo_dos_transbordos_y_nueva_ventana():
    respuesta = calcular([f"2025-03-10T{hora}-05:00" for hora in ["07:00:00", "07:10:00", "07:20:00", "07:30:00", "09:00:00"]])
    assert [c.tipo for c in respuesta.cobros] == ["tarifa", "transbordo", "transbordo_gratis", "tarifa", "transbordo"]
    assert respuesta.total == 7400


def test_cruce_medianoche():
    respuesta = calcular(["2025-03-10T23:34:00-05:00", "2025-03-11T00:21:15-05:00"], "adulto_mayor")
    assert [c.valor for c in respuesta.cobros] == [1450, 250]


def test_desorden_offsets_y_no_mutacion():
    solicitud = SolicitudTarifa(tarjeta="T", validaciones=[
        {"id": "tarde", "estacion": "E01", "fecha_hora": "2025-03-10T08:00:00-05:00"},
        {"id": "temprano", "estacion": "E02", "fecha_hora": "2025-03-10T12:00:00Z"},
    ])
    respuesta = calcular_tarifa(solicitud)
    assert [c.validacion_id for c in respuesta.cobros] == ["temprano", "tarde"]
    assert respuesta.total == 3700
    assert solicitud.validaciones[0].id == "tarde"


def test_empates_conservan_orden_de_entrada():
    respuesta = calcular(["2025-03-10T12:00:00Z"] * 4)
    assert [c.validacion_id for c in respuesta.cobros] == ["0", "1", "2", "3"]
    assert [c.valor for c in respuesta.cobros] == [3200, 500, 0, 3200]


def test_lista_vacia():
    respuesta = calcular([])
    assert respuesta.cobros == []
    assert respuesta.total == 0


def test_muestra_real():
    ruta = Path(__file__).resolve().parents[1] / "datos_ejemplo/validaciones_2025-03-10.json"
    resultados = [calcular_tarifa(SolicitudTarifa.model_validate(s)) for s in json.loads(ruta.read_text())]
    assert [r.total for r in resultados] == [7400, 4900, 1700]
    assert [c.validacion_id for c in resultados[1].cobros] == ["b7c0", "b7c1", "b7c2", "b7c3"]
