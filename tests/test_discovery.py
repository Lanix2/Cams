import pytest

from cams.discovery import (
    AuthorizationError,
    HostResult,
    hosts_in,
    require_authorization,
)


def test_hosts_in_24():
    hosts = hosts_in("192.168.1.0/24")
    assert len(hosts) == 254
    assert hosts[0] == "192.168.1.1"
    assert hosts[-1] == "192.168.1.254"


def test_hosts_in_single():
    assert hosts_in("10.0.0.5/32") == ["10.0.0.5"]


def test_services_and_camera_detection():
    r = HostResult(ip="192.168.1.10", open_ports=[80, 554])
    assert "rtsp" in r.services
    assert r.likely_camera is True


def test_web_only_not_flagged_as_camera():
    # Un puerto 80/443 estándar por sí solo no basta (podría ser cualquier web).
    r = HostResult(ip="192.168.1.11", open_ports=[80, 443])
    assert r.likely_camera is False


def test_nonstandard_web_flagged():
    r = HostResult(ip="192.168.1.12", open_ports=[8080])
    assert r.likely_camera is True


def test_require_authorization():
    with pytest.raises(AuthorizationError):
        require_authorization(False)
    # No levanta con autorización.
    require_authorization(True)
