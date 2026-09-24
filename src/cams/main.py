"""CLI de Cams: descubrimiento de cámaras en redes propias o autorizadas."""

from __future__ import annotations

import argparse
import sys

from cams.discovery import (
    DEFAULT_PORTS,
    AuthorizationError,
    require_authorization,
    scan_subnet,
)

_AVISO = (
    "AVISO: ejecuta el escaneo SOLO en redes de tu propiedad o con "
    "autorización explícita por escrito. Escanear o acceder a equipos "
    "ajenos sin permiso es delito, aunque la intención sea avisar."
)


def _cmd_scan(args: argparse.Namespace) -> int:
    try:
        require_authorization(args.authorized)
    except AuthorizationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        print(_AVISO, file=sys.stderr)
        print("Vuelve a ejecutar con --authorized si es tu red.", file=sys.stderr)
        return 2

    print(f"Escaneando {args.subnet} ...", file=sys.stderr)
    results = scan_subnet(args.subnet, timeout=args.timeout)
    if not results:
        print("No se encontraron hosts con puertos de cámara abiertos.")
        return 0

    for r in sorted(results, key=lambda h: tuple(int(x) for x in h.ip.split("."))):
        flag = "  <- posible cámara" if r.likely_camera else ""
        servicios = ", ".join(f"{p}/{s}" for p, s in zip(r.open_ports, r.services))
        print(f"{r.ip:<16} {servicios}{flag}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cams", description=_AVISO)
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Descubrir cámaras en una subred.")
    scan.add_argument("subnet", help="Subred en formato CIDR, p.ej. 192.168.1.0/24")
    scan.add_argument(
        "--authorized",
        action="store_true",
        help="Confirma que la red es tuya o tienes autorización para auditarla.",
    )
    scan.add_argument(
        "--timeout", type=float, default=0.5, help="Timeout por puerto (segundos)."
    )
    scan.set_defaults(func=_cmd_scan, ports=DEFAULT_PORTS)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
