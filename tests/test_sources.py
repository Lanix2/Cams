from pathlib import Path

import pytest

from cams.sources import Camera, enabled_cameras, load_cameras


def _write(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "cameras.yaml"
    p.write_text(text, encoding="utf-8")
    return p


def test_load_cameras_ok(tmp_path):
    p = _write(
        tmp_path,
        """
cameras:
  - id: a
    name: Cámara A
    url: "rtsp://host/stream"
  - id: b
    url: 0
    enabled: false
""",
    )
    cams = load_cameras(p)
    assert cams == [
        Camera(id="a", name="Cámara A", url="rtsp://host/stream", enabled=True),
        Camera(id="b", name="b", url=0, enabled=False),
    ]
    assert enabled_cameras(cams) == [cams[0]]


def test_load_cameras_duplicate_id(tmp_path):
    p = _write(
        tmp_path,
        """
cameras:
  - id: a
    url: 0
  - id: a
    url: 1
""",
    )
    with pytest.raises(ValueError, match="duplicado"):
        load_cameras(p)


def test_load_cameras_missing_field(tmp_path):
    p = _write(tmp_path, "cameras:\n  - name: sin id\n    url: 0\n")
    with pytest.raises(ValueError, match="Falta el campo"):
        load_cameras(p)


def test_load_cameras_bad_root(tmp_path):
    p = _write(tmp_path, "otra_cosa: 1\n")
    with pytest.raises(ValueError, match="lista bajo la clave"):
        load_cameras(p)
