"""Cálculo de lo que se le cobra a una tarjeta por sus validaciones."""

from datetime import timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP

from app.config import (
    DESCUENTOS,
    MULTIPLO_REDONDEO,
    TARIFA_BASE,
    VALOR_TRANSBORDO,
    VENTANA_TRANSBORDO_MIN,
)
from app.modelos import Cobro, Perfil, RespuestaTarifa, SolicitudTarifa


def aplicar_descuento(valor: int, perfil: Perfil) -> int:
    """Descuenta y redondea cada cobro; los empates siempre suben."""
    valor_descontado = Decimal(valor) * (100 - DESCUENTOS[perfil.value]) / 100
    unidades = (valor_descontado / MULTIPLO_REDONDEO).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return int(unidades) * MULTIPLO_REDONDEO


def calcular_tarifa(solicitud: SolicitudTarifa) -> RespuestaTarifa:
    # UTC compara instantes reales, aunque lleguen con offsets distintos.
    validaciones = sorted(
        solicitud.validaciones,
        key=lambda validacion: validacion.fecha_hora.astimezone(timezone.utc),
    )
    cobros = []
    inicio_viaje = None
    transbordos = 0
    ventana = timedelta(minutes=VENTANA_TRANSBORDO_MIN)

    for validacion in validaciones:
        instante = validacion.fecha_hora.astimezone(timezone.utc)
        if (
            inicio_viaje is None
            or instante - inicio_viaje > ventana
            or transbordos == 2
        ):
            inicio_viaje = instante
            transbordos = 0
            tipo = "tarifa"
            valor = TARIFA_BASE
        else:
            transbordos += 1
            tipo = "transbordo" if transbordos == 1 else "transbordo_gratis"
            valor = VALOR_TRANSBORDO if transbordos == 1 else 0

        cobros.append(
            Cobro(
                validacion_id=validacion.id,
                fecha_hora=validacion.fecha_hora,
                tipo=tipo,
                valor=aplicar_descuento(valor, solicitud.perfil),
            )
        )

    return RespuestaTarifa(
        tarjeta=solicitud.tarjeta,
        perfil=solicitud.perfil,
        cobros=cobros,
        total=sum(cobro.valor for cobro in cobros),
    )
