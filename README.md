# tarifas-t2

Servicio que calcula el cobro de una tarjeta por sus validaciones en la Línea T2, incluyendo reglas de transbordos y descuentos según el perfil del usuario.

## Correr local

```
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentación interactiva en http://localhost:8000/docs

## Tests

```
pytest
python -m pytest -v  ---> Prueba completa
```

## Docker

```
docker compose up --build
docker compose down         ----> Detener
```
