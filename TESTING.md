# Testing

## Backend

Los tests del backend usan `pytest`, `fastapi.testclient` y una base SQLite aislada en `back/test.db`.
Cada test recrea el schema desde cero y genera sus propios datos, por lo que no toca `data.db`.

```bash
cd back
.venv/bin/python -m pytest
```

Para correr un archivo puntual:

```bash
cd back
.venv/bin/python -m pytest tests/test_reporte_afip.py
```

## Frontend

Los tests del frontend usan el stack de `react-scripts` y Testing Library.
El smoke test principal mockea `src/api.ts`, así que no necesita backend levantado.

```bash
cd front
npm test -- --watchAll=false
```

Para compilar:

```bash
cd front
npm run build
```
