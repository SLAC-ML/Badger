import time
import pandas as pd
from PyQt5.QtCore import Qt

from xopt import VOCS
from xopt.generators import RandomGenerator


def test_run_monitor(qtbot):
    from badger.routine import Routine
    from badger.gui.default.components.run_monitor import BadgerOptMonitor

    monitor = BadgerOptMonitor()
    monitor.show()
    qtbot.addWidget(monitor)

    # Create the sample routine
    test_routine = {
        "name": "routine-for-core-test",
        "algo": "upper_confidence_bound",
        "env": "test",
        "algo_params": {
            "model": None,
            "turbo_controller": None,
            "use_cuda": False,
            "gp_constructor": {
                "name": "standard",
                "use_low_noise_prior": True,
                "covar_modules": {},
                "mean_modules": {},
                "trainable_mean_keys": [],
            },
            "numerical_optimizer": {
                "name": "LBFGS",
                "n_restarts": 20,
                "max_iter": 2000,
            },
            "max_travel_distances": None,
            "fixed_features": None,
            "n_candidates": 1,
            "n_monte_carlo_samples": 128,
            "beta": 2.0,
            "start_from_current": True,
        },
        "env_params": {},
        "config": {
            "variables": {
                "x0": [-1, 1],
                "x1": [-1, 1],
                "x2": [-1, 1],
                "x3": [-1, 1]
            },
            "objectives": {"f": "MAXIMIZE"},
            "constraints": None,
            "states": None,
            "domain_scaling": None,
            "tags": None,
            "init_points": {
                "x0": [0.5],
                "x1": [0.5],
                "x2": [0.5],
                "x3": [0.5],
            },
        },
    }

    # Create the vocs
    vocs = VOCS(
        variables=test_routine["config"]["variables"],
        objectives=test_routine["config"]["objectives"],
    )

    # Create the generator
    generator = RandomGenerator(vocs=vocs)

    # Finally create the routine
    routine = Routine(
        name="test",
        vocs=vocs,
        generator=generator,
        environment={"name": test_routine["env"]},
        initial_points=pd.DataFrame(test_routine["config"]["init_points"])
    )

    # Feed in the sample routine
    monitor.routine = routine
    assert monitor.btn_stop.text() == 'Run'

    qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)
    time.sleep(3)
    qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)
    assert monitor.var_names == ['x0', 'x1', 'x2', 'x3']
