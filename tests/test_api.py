import pytest
from fastapi.testclient import TestClient

from app.config import TARIFA_BASE
from app.main import app

cliente = TestClient(app)


def test_salud():
    r = cliente.get("/salud")
    assert r.status_code == 200
    assert r.json() == {"estado": "ok"}


def test_una_validacion_paga_tarifa_completa():
    r = cliente.post(
        "/tarifas/calcular",
        json={
            "tarjeta": "T-TEST-001",
            "perfil": "general",
            "validaciones": [
                {"id": "v1", "estacion": "E01", "fecha_hora": "2025-03-10T07:12:00-05:00"}
            ],
        },
    )
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["total"] == TARIFA_BASE
    assert cuerpo["cobros"][0]["tipo"] == "tarifa"


def test_historial_registra_el_calculo():
    cliente.post(
        "/tarifas/calcular",
        json={
            "tarjeta": "T-TEST-002",
            "validaciones": [
                {"id": "v1", "estacion": "E04", "fecha_hora": "2025-03-10T09:00:00-05:00"}
            ],
        },
    )
    r = cliente.get("/tarjetas/T-TEST-002/historial")
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_historial_separa_tarjetas_y_acumula_solo_la_propia():
    for tarjeta in ["A", "B", "A"]:
        r = cliente.post("/tarifas/calcular", json={"tarjeta": tarjeta, "validaciones": []})
        assert r.status_code == 200
    a = cliente.get("/tarjetas/A/historial").json()
    b = cliente.get("/tarjetas/B/historial").json()
    assert len(a) == 2 and all(c["tarjeta"] == "A" for c in a)
    assert len(b) == 1 and b[0]["tarjeta"] == "B"
    assert cliente.get("/tarjetas/NUEVA/historial").json() == []


def test_contrato_completo_y_perfil_por_defecto():
    r = cliente.post("/tarifas/calcular", json={
        "tarjeta": "C", "validaciones": [
            {"id": "v2", "estacion": "E07", "fecha_hora": "2025-03-10T07:31:44-05:00"},
            {"id": "v1", "estacion": "E01", "fecha_hora": "2025-03-10T06:52:10-05:00"},
        ],
    })
    assert r.status_code == 200
    assert r.json() == {
        "tarjeta": "C", "perfil": "general", "total": 3700,
        "cobros": [
            {"validacion_id": "v1", "fecha_hora": "2025-03-10T06:52:10-05:00", "tipo": "tarifa", "valor": 3200},
            {"validacion_id": "v2", "fecha_hora": "2025-03-10T07:31:44-05:00", "tipo": "transbordo", "valor": 500},
        ],
    }


def test_vacio_devuelve_200():
    r = cliente.post("/tarifas/calcular", json={"tarjeta": "C", "validaciones": []})
    assert r.status_code == 200
    assert r.json() == {"tarjeta": "C", "perfil": "general", "cobros": [], "total": 0}


@pytest.mark.parametrize("cambio", ["perfil", "sin_zona", "duplicado", "fecha_invalida"])
def test_solicitudes_invalidas_422_sin_registrar_historial(cambio):
    validacion = {"id": "v1", "estacion": "E01", "fecha_hora": "2025-03-10T07:00:00-05:00"}
    datos = {"tarjeta": "INVALIDA", "validaciones": [validacion]}
    if cambio == "perfil":
        datos["perfil"] = "desconocido"
    elif cambio == "sin_zona":
        validacion["fecha_hora"] = "2025-03-10T07:00:00"
    elif cambio == "fecha_invalida":
        validacion["fecha_hora"] = "no-es-fecha"
    else:
        datos["validaciones"].append(dict(validacion))
    assert cliente.post("/tarifas/calcular", json=datos).status_code == 422
    assert cliente.get("/tarjetas/INVALIDA/historial").json() == []
