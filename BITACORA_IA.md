# Bitácora de uso de IA

## 1. Herramientas utilizadas

Utilicé ChatGPT como asistente para revisar el código Python heredado, analizar casos borde, proponer mejoras en la lógica de tarifas, estructurar pruebas automatizadas y revisar la configuración de Docker y Git. Las sugerencias se contrastaron con el código del proyecto y con la ejecución local.

## 2. Tres prompts representativos

**Prompt 1 — Revisión del historial**

“Revisa el código de `historial.py`, `modelos.py` y `tarifas.py`. Identifica el problema de aislamiento de los historiales por tarjeta, explica su causa y plantea una corrección acompañada de una prueba de regresión.”

**Prompt 2 — Transbordos y descuentos**

“Revisa la lógica de cálculo de tarifas e implementa las reglas de transbordos y descuentos por perfil. Ten en cuenta el límite de tiempo, el máximo de transbordos, el redondeo monetario y los casos borde. Propón pruebas automatizadas para validar el comportamiento.”

**Prompt 3 — Pruebas y Docker**

“Revisa la cobertura de pruebas de la API y la configuración de Docker. Identifica validaciones o casos borde que falten, comprueba que las pruebas no deshabiliten las advertencias y optimiza la construcción de la imagen sin incluir archivos innecesarios.”


## 3. Verificación y criterio propio

No di por correctas las propuestas únicamente porque la IA las generara. Revisé los cambios, ejecuté la suite con `python -m pytest -v` y comprobé que las pruebas pasaran, manteniendo las advertencias como errores. También construí y levanté la aplicación con Docker.

Durante la validación inicial de Docker apareció un error de conexión con el motor de Docker Desktop. Identifiqué que el problema estaba relacionado con la disponibilidad del motor, no necesariamente con el código de la API. Tras resolverlo, repetí la construcción y confirmé que el servicio arrancara.

## 4. Mi aporte

Mi aporte fue dirigir el análisis según los requisitos de la prueba, decidir qué comportamientos debían validarse, revisar las soluciones propuestas y comprobarlas en el entorno local. También organicé los cambios en commits separados, preparé las pruebas de regresión, revisé la configuración del repositorio y publiqué la rama `feature/transbordos` en GitHub.

La IA fue una herramienta de apoyo; la selección de cambios, la verificación de resultados y la preparación de la entrega formaron parte de mi trabajo.

