"""Carga y validación de la lista de cámaras."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Camera:
    """Una fuente de vídeo. `url` puede ser una URL (RTSP/HLS/MJPEG) o un
    índice de dispositivo (int) para una webcam local."""

    id: str
    name: str
    url: str | int
    enabled: bool = True


def load_cameras(path: str | Path) -> list[Camera]:
    """Lee un archivo YAML con la lista de cámaras.

    Levanta FileNotFoundError si no existe y ValueError si el formato es
    inválido o hay ids duplicados.
    """
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    raw = data.get("cameras")
    if not isinstance(raw, list):
        raise ValueError("El YAML debe tener una lista bajo la clave 'cameras'.")

    cameras: list[Camera] = []
    seen: set[str] = set()
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"La cámara en la posición {i} no es un mapa.")
        try:
            cam = Camera(
                id=str(item["id"]),
                name=str(item.get("name", item["id"])),
                url=item["url"],
                enabled=bool(item.get("enabled", True)),
            )
        except KeyError as exc:
            raise ValueError(
                f"Falta el campo {exc} en la cámara en la posición {i}."
            ) from exc

        if cam.id in seen:
            raise ValueError(f"Id de cámara duplicado: {cam.id!r}.")
        seen.add(cam.id)
        cameras.append(cam)

    return cameras


def enabled_cameras(cameras: list[Camera]) -> list[Camera]:
    """Devuelve solo las cámaras habilitadas."""
    return [c for c in cameras if c.enabled]
