from cams.main import main


def test_main(capsys):
    main()
    assert capsys.readouterr().out == "Hola desde Cams\n"
