"""Descubrimiento de cámaras en una red PROPIA o autorizada.

USO RESPONSABLE: ejecuta esto únicamente contra redes de tu propiedad o
sobre las que tengas autorización explícita por escrito para auditar.
Escanear o acceder a equipos ajenos sin permiso es acceso no autorizado y
constituye delito en la mayoría de jurisdicciones, con independencia de la
intención. Estar conectado a la misma red que otra persona no otorga ese
permiso.
"""

from __future__ import annotations

import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

# Puertos habitualmente expuestos por cámaras IP, DVR/NVR y sus interfaces web.
CAMERA_PORTS: dict[int, str] = {
    80: "http",       # interfaz web
    81: "http-alt",
    443: "https",
    554: "rtsp",      # streaming RTSP
    8000: "http-alt",
    8080: "http-alt",
    8443: "https-alt",
    8554: "rtsp-alt",
    8899: "onvif",
    37777: "dahua",   # protocolo Dahua
    34567: "dvr",     # DVR/NVR chino común
}

DEFAULT_PORTS: tuple[int, ...] = tuple(CAMERA_PORTS)


@dataclass
class HostResult:
    """Resultado del escaneo de un host."""

    ip: str
    open_ports: list[int] = field(default_factory=list)

    @property
    def services(self) -> list[str]:
        return [CAMERA_PORTS.get(p, str(p)) for p in self.open_ports]

    @property
    def likely_camera(self) -> bool:
        """Heurística: hay señales de cámara si hay un puerto de streaming
        (RTSP/ONVIF/Dahua) o una interfaz web en un puerto no estándar."""
        streaming = {554, 8554, 8899, 37777, 34567}
        return bool(set(self.open_ports) & streaming) or any(
            p in self.open_ports for p in (81, 8000, 8080)
        )


def hosts_in(cidr: str) -> list[str]:
    """Expande un CIDR (p.ej. '192.168.1.0/24') a las IP de host utilizables."""
    net = ipaddress.ip_network(cidr, strict=False)
    if net.num_addresses <= 2:  # /31, /32
        return [str(h) for h in net]
    return [str(h) for h in net.hosts()]


def scan_host(
    ip: str,
    ports: tuple[int, ...] = DEFAULT_PORTS,
    timeout: float = 0.5,
) -> HostResult:
    """Escaneo TCP connect de un host. No autentica ni accede al servicio;
    solo comprueba qué puertos aceptan conexión."""
    result = HostResult(ip=ip)
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((ip, port)) == 0:
                result.open_ports.append(port)
    return result


def scan_subnet(
    cidr: str,
    ports: tuple[int, ...] = DEFAULT_PORTS,
    timeout: float = 0.5,
    workers: int = 100,
) -> list[HostResult]:
    """Escanea una subred y devuelve los hosts con al menos un puerto abierto."""
    targets = hosts_in(cidr)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = pool.map(lambda ip: scan_host(ip, ports, timeout), targets)
    return [r for r in results if r.open_ports]


class AuthorizationError(PermissionError):
    """Se intentó escanear sin confirmar autorización sobre la red."""


def require_authorization(authorized: bool) -> None:
    """Barrera de seguridad: obliga a confirmar de forma explícita que se
    tiene autorización sobre la red antes de escanear."""
    if not authorized:
        raise AuthorizationError(
            "Debes confirmar que la red es de tu propiedad o que cuentas con "
            "autorización explícita para auditarla (authorized=True)."
        )
