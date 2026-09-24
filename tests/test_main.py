from cams.main import build_parser, main


def test_scan_requires_authorization(capsys):
    # Sin --authorized debe abortar con código 2 y no escanear.
    code = main(["scan", "10.255.255.0/30"])
    assert code == 2
    assert "autoriz" in capsys.readouterr().err.lower()


def test_parser_has_scan():
    parser = build_parser()
    args = parser.parse_args(["scan", "192.168.1.0/24", "--authorized"])
    assert args.subnet == "192.168.1.0/24"
    assert args.authorized is True
