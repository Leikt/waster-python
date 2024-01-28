import pytest

from waster.core.services.memory_waster import create_memory_waster


def test_create_memory_waster___default():
    ms = create_memory_waster()
    assert ms.target_kb == 0
    assert ms.current_kb == 0
    assert ms.need_refresh is False


def test_create_memory_waster___initial_value():
    ms = create_memory_waster(10)
    assert ms.target_kb == 10
    assert ms.current_kb == 0
    assert ms.need_refresh is True


def test_ms_set():
    ms = create_memory_waster(0)
    assert ms.need_refresh is False

    ms.set(10)
    assert ms.target_kb == 10
    assert ms.need_refresh is True

    with pytest.raises(ValueError):
        ms.set(-1)


def test_ms_increase():
    ms = create_memory_waster(0)
    ms.increase(10)
    assert ms.target_kb == 10
    assert ms.need_refresh is True

    ms.increase(105)
    assert ms.target_kb == 115
    assert ms.need_refresh is True

    with pytest.raises(ValueError):
        ms.increase(-1)


def test_ms_decrease():
    ms = create_memory_waster(200)
    ms.decrease(10)
    assert ms.target_kb == 190
    assert ms.need_refresh is True

    ms.decrease(105)
    assert ms.target_kb == 85
    assert ms.need_refresh is True

    with pytest.raises(ValueError):
        ms.decrease(-1)


def test_ms_clear():
    ms = create_memory_waster(150)
    ms.refresh()
    ms.clear()
    assert ms.target_kb == 0
    assert ms.need_refresh is True


def test_ms_refresh():
    ms = create_memory_waster(10)
    assert ms.need_refresh is True

    ms.refresh()
    assert ms.need_refresh is False

    ms.set(100)
    assert ms.need_refresh is True
    ms.refresh()
    assert ms.need_refresh is False

    ms.decrease(50)
    assert ms.need_refresh is True
    ms.refresh()
    assert ms.need_refresh is False
