# Network Service Monitor

Proyecto educativo de **redes / infraestructura TI** escrito en Python, sin dependencias externas. Comprueba si un servicio **TCP** expresamente indicado acepta conexiones y genera un reporte local JSON.

> **Alcance:** comprueba conectividad TCP, **no** garantiza que la aplicación web funcione correctamente. Usar solo con servicios propios o con autorización; no realiza descubrimiento automático ni barridos de puertos.

## Requisitos

Python 3.10+.

## Primer uso (Windows / PowerShell)

Abre PowerShell en la carpeta que contiene `src` y `samples`:

```powershell
py -m unittest discover -s tests -v
py src/monitor.py samples/targets.json --timeout 1
py src/monitor.py samples/targets.json --json report.json
```

El archivo de ejemplo usa `127.0.0.1` (tu propio equipo). Un puerto sin servidor escuchando aparecerá como `unreachable`: **es esperable**.

Para obtener un resultado `reachable`, abre otra terminal y ejecuta:

```powershell
py -m http.server 8000 --bind 127.0.0.1
```

Deja ese servidor funcionando y repite la consulta en la primera terminal. Después, detén el servidor con **Ctrl+C**.

## Archivo de destinos

```json
[
  {"name": "Web local", "host": "127.0.0.1", "port": 8000},
  {"name": "Servicio local de ejemplo", "host": "127.0.0.1", "port": 9999}
]
```

El programa prueba únicamente los destinos indicados, con un máximo de 30 entradas y timeout máximo de 10 segundos por destino.

## Qué aprenderás

- Conectividad TCP y diferencia entre *puerto accesible* y *aplicación saludable*.
- Manejo de excepciones de sockets en Python.
- Validación de JSON y parámetros CLI.
- Pruebas unitarias con `unittest` y `unittest.mock`.

## Estructura

```text
src/monitor.py           # Lógica y CLI
tests/test_monitor.py    # Siete pruebas automáticas sin tráfico real
samples/targets.json    # Destinos locales ficticios
```

## Limitaciones y mejoras futuras

- Ejecuta comprobaciones secuenciales y puntuales; no programa monitoreo periódico.
- No realiza HTTP GET ni verifica certificados TLS.
- Los tiempos de conexión no representan el rendimiento total de un servicio.
- Mejora propuesta: historial CSV para ver cambios de estado y gráfico de disponibilidad.

## Seguridad y privacidad

No subas IP privadas de una organización, contraseñas ni capturas de redes internas sin permiso. El código no requiere privilegios de administrador ni credenciales.

## Autoría y aprendizaje

Proyecto de portafolio educativo preparado con asistencia de IA. Se recomienda ejecutarlo, entenderlo y documentar las mejoras personales antes de presentarlo en entrevistas.
