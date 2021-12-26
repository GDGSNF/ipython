from IPython.utils import decorators

def test_flag_calls():
    @decorators.flag_calls
    def f():
        pass
    
    assert not f.called
    f()
    assert f.called


def test_flag_calls_raise():
    @decorators.flag_calls
    def f():
        1 / 0

    assert not f.called
    try:
        f()
    except Exception:
        pass
    assert not f.called
