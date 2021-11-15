import os
from pkg_resources import get_distribution


pytest_plugins = ['pytester']


def test_cli_main(testdir):
    args = ['badger']
    result = testdir.run(*args)

    assert result.ret == 0

    # Check output lines
    outlines = result.outlines
    assert len(outlines) == 6

    # Check name
    assert outlines[0] == 'name: Badger the optimizer'

    # Check version
    version = get_distribution('badger-opt').version
    assert outlines[1] == f'version: {version}'


def test_cli_run(testdir, mock_config_root):
    args = ['badger', 'run', '-a', 'silly', '-ap',
            '{dimension: 2, max_iter: 10}',  '-e', 'silly', '-c',
            os.path.join(mock_config_root, 'test.yaml'), '-y']
    result = testdir.run(*args)

    assert result.ret == 0

    # Check output lines
    outlines = result.outlines
    assert len(outlines) == 14

    # Check table header
    assert outlines[1] == '|    iter    |     l2     |     q1     |     q2     |'
