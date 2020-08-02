from main import break_down_time


def test_break_down_time():
    assert break_down_time(0) == (0, 0, 0, 0)
    assert break_down_time(15) == (0, 0, 0, 15)
    assert break_down_time(120) == (0, 0, 2, 0)
    assert break_down_time(3600) == (0, 1, 0, 0)
    assert break_down_time(86400) == (1, 0, 0, 0)
    assert break_down_time(90061) == (1, 1, 1, 1)
    assert break_down_time(100989) == (1, 4, 3, 9)
