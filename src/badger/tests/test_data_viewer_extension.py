from badger.gui.default.components.analysis_extensions import DataViewer
from PyQt5.QtCore import Qt

def test_data_viewer_simple(qtbot):
    from badger.tests.utils import create_routine

    routine = create_routine()
    routine.evaluate_data(routine.initial_points)

    data_viewer = DataViewer()
    data_viewer.update_window(routine)
