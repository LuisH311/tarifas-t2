from app.historial import HistorialTarjeta
from app.modelos import RespuestaTarifa


def test_instancias_no_comparten_calculos():
    a = HistorialTarjeta("A")
    b = HistorialTarjeta("B")
    respuesta = RespuestaTarifa(tarjeta="A", perfil="general", cobros=[], total=0)
    a.registrar(respuesta)
    assert a.listar() == [respuesta]
    assert b.listar() == []


def test_listar_no_expone_la_lista_interna():
    historial = HistorialTarjeta("A")
    historial.registrar(RespuestaTarifa(tarjeta="A", perfil="general", cobros=[], total=0))
    historial.listar().clear()
    assert len(historial.listar()) == 1
