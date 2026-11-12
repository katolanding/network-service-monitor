# Network Service Monitor

[![Python Tests](https://github.com/katolanding/network-service-monitor/actions/workflows/python-tests.yml/badge.svg)](https://github.com/katolanding/network-service-monitor/actions/workflows/python-tests.yml)

Herramienta educativa de **redes e infraestructura TI**, escrita en Python y sin dependencias externas. Comprueba si servicios TCP explícitamente configurados aceptan una conexión y permite guardar un informe JSON.

> **Alcance:** una conexión TCP exitosa no garantiza que la aplicación responda correctamente. Úsala solo con servicios propios o con autorización; no descubre hosts ni barre puertos.

## Demostración local

Requiere Python 3.10 o superior. Desde la carpeta del repositorio, abre PowerShell y ejecuta:

```powershell
py src/monitor.py samples/targets.json
```

El archivo `samples/targets.json` configura dos destinos **en tu propio equipo** (`127.0.0.1`), en los puertos `8000` y `9999`. Si no hay servicios escuchando, es normal que ambos aparezcan como `unreachable`.

### Probar un servicio realmente accesible

En una **segunda terminal**, inicia un servidor HTTP de prueba en tu equipo:

```powershell
py -m http.server 8000 --bind 127.0.0.1
```

En la primera terminal, ejecuta nuevamente:

```powershell
py src/monitor.py samples/targets.json --timeout 1
```

**Ejemplo ilustrativo de salida con el servidor local activo:**

```text
Services: 2 | Reachable: 1 | Unreachable: 1
  Web local (127.0.0.1:8000): reachable [<latencia variable> ms]
  Servicio local de ejemplo (127.0.0.1:9999): unreachable [<latencia variable> ms]
```

La latencia y el resultado del puerto `9999` dependen de los servicios que tengas abiertos. Para detener el servidor del puerto 8000, presiona **Ctrl+C** en la segunda terminal.

### Exportar JSON

```powershell
py src/monitor.py samples/targets.json --json report.json
```

El programa permite hasta 30 destinos declarados y un tiempo máximo de espera de 10 segundos por destino.

## Pruebas automatizadas

```powershell
py -m unittest discover -s tests -v
```

Incluye **siete pruebas unitarias** con conexiones simuladas (`unittest.mock`), por lo que el flujo de pruebas no requiere contactar servidores externos. La ejecución consultada el **12 de noviembre de 2026** terminó correctamente; la insignia indica el estado más reciente.

## Archivo de ejemplo

```json
[
  {"name": "Web local", "host": "127.0.0.1", "port": 8000},
  {"name": "Servicio local de ejemplo", "host": "127.0.0.1", "port": 9999}
]
```

## Estructura

```text
src/monitor.py             Comprobación TCP, validación y CLI
tests/test_monitor.py      Siete pruebas automatizadas
samples/targets.json       Destinos locales de ejemplo
.github/workflows/         Integración continua
```

## Limitaciones y futuras mejoras

- Comprueba destinos de forma secuencial, no hace monitoreo continuo.
- No ejecuta peticiones HTTP ni valida certificados TLS.
- El tiempo de conexión no representa el rendimiento completo del servicio.
- Posible ampliación: historial local CSV y gráfico de disponibilidad.

## Seguridad y autoría
Proyecto de portafolio educativo con foco en aprendizaje de redes.
