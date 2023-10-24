import os


class TestDB:
    def test_save_routine(self):
        from badger.db import BADGER_DB_ROOT
        from badger.db import save_routine, remove_routine
        from badger.tests.utils import create_routine

        os.makedirs(BADGER_DB_ROOT, exist_ok=True)

        routine = create_routine()
        save_routine(routine)

        remove_routine("test")

    def test_load_routine(self):
        from badger.db import BADGER_DB_ROOT
        from badger.db import save_routine, load_routine, remove_routine
        from badger.tests.utils import create_routine

        os.makedirs(BADGER_DB_ROOT, exist_ok=True)

        routine = create_routine()
        save_routine(routine)

        new_routine, _ = load_routine("test")
        assert new_routine.generator == routine.generator
        assert new_routine.vocs == routine.vocs

        remove_routine("test")
