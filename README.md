# Cams

Herramienta de auditoría para descubrir cámaras IP en **tu propia red** (o
en una red sobre la que tengas autorización explícita para auditar) y
detectar las que están expuestas sin la configuración de seguridad adecuada.

## ⚠️ Uso responsable

Ejecuta esta herramienta **únicamente** contra redes de tu propiedad o con
**autorización explícita por escrito** del responsable de la red. Escanear o
acceder a equipos ajenos sin permiso es acceso no autorizado y constituye
delito en la mayoría de jurisdicciones, **con independencia de la intención**.
Estar conectado a la misma red que otra persona no otorga ese permiso.

Si detectas una cámara de un tercero expuesta y quieres que se corrija, el
canal correcto es reportarlo al **CERT/CSIRT** de tu país, al **ISP** o al
**fabricante** del dispositivo — no acceder tú al equipo.

## Requisitos

- Python 3.10+

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Uso

Descubrir cámaras en tu subred (la bandera `--authorized` es obligatoria y
confirma que tienes permiso sobre esa red):

```bash
cams scan 192.168.1.0/24 --authorized
```

## Tests

```bash
pytest
```

## Estado / hoja de ruta

- [x] Carga de la lista de cámaras desde YAML (`cams.sources`)
- [x] Descubrimiento por escaneo de puertos con barrera de autorización (`cams.discovery`)
- [ ] Comprobación de streams RTSP/HLS y captura de fotograma (OpenCV)
- [ ] Detección de acceso sin autenticación (hallazgos de seguridad)
- [ ] Visor web de los feeds
