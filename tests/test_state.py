
from checkers_sem.state import state

def test_state():
    for attr_name in dir(state):
        if attr_name.startswith('__'):
            continue
        attr = getattr(state, attr_name)
        assert attr is not None

    assert len(state.get_genetic_settings()) == 5
