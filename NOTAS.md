# Notas técnicas

## Hallazgos del código heredado

Además del problema de aislamiento del historial, encontré aspectos importantes en el manejo de las validaciones y del cálculo de tarifas. El historial se almacenaba en una lista compartida a nivel de clase, lo que podía mezclar cálculos de tarjetas distintas. Lo corregí para que cada instancia mantenga su propio historial y añadí una prueba de regresión.

También reforcé las validaciones de entrada y el tratamiento de fechas para evitar datos ambiguos y registros duplicados.

## Casos borde y soluciones

- **Transbordos:** contemplé el límite de 90 minutos, incluyendo la hora exacta del límite, y la regla de máximo dos transbordos antes de iniciar un nuevo cobro.
- **Fechas y zonas horarias:** ordené las validaciones por instante UTC y rechacé fechas sin zona horaria.
- **Descuentos y redondeo:** utilicé `Decimal` con redondeo `ROUND_HALF_UP` para evitar imprecisiones propias de los números de punto flotante.
- **Identificadores duplicados:** agregué una validación para rechazar validaciones repetidas.
- **Aislamiento y consistencia:** probé el historial por tarjeta, las solicitudes inválidas, las listas vacías y que el cálculo no modifique las validaciones originales.

## Supuestos

Interpreté que el límite de 90 minutos es inclusivo; que el tiempo del transbordo se calcula respecto de la validación que inicia el período y no se reinicia con cada transbordo; y que las fechas deben incluir zona horaria. Apliqué las reglas de perfiles, descuentos y transbordos según el comportamiento definido para el ejercicio.

## Pendiente para producción

- **Base de datos:** almacenar los historiales de forma persistente para no perderlos al reiniciar el servicio.
- **Seguridad:** implementar autenticación y validar los permisos de acceso a la API.
- **Pruebas:** ampliar las pruebas de integración y rendimiento para verificar el comportamiento con múltiples solicitudes.
- **Monitoreo:** incorporar registros y alertas para detectar fallos y dar seguimiento al funcionamiento del servicio.
- **Configuración:** separar las configuraciones de desarrollo y producción para facilitar el despliegue y mantenimiento.

