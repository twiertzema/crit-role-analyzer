from fetch_episodes import parse_time


def test_parse_time():
    assert parse_time("0:0") == 0
    assert parse_time("0:0:0") == 0

    assert parse_time("0:15") == 15
    assert parse_time("0:0:15") == 15

    assert parse_time("2:0") == 120
    assert parse_time("0:2:0") == 120

    assert parse_time("1:15") == 75
    assert parse_time("0:1:15") == 75

    assert parse_time("2:0:15") == 7215
    assert parse_time("2:1:15") == 7275
