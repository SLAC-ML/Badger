import subprocess
from importlib import metadata


def capture(command):
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    return out, err, proc.returncode


def test_cli_main():
    command = ['badger']
    out, err, exitcode = capture(command)

    assert exitcode == 0

    # Check output lines
    outlines = out.split('\n')
    assert len(outlines) == 8

    # Check name
    assert outlines[0] == 'name: Badger the optimizer'

    # Check version
    version = metadata.version('badger-opt')
    assert outlines[1] == f'version: {version}'


# def test_cli_run(mock_config_root):
#     command = ['badger', 'run', '-a', 'upper_confidence_bound', '-ap',
#                '{max_evaluations: 10}',  '-e', 'silly', '-c',
#                os.path.join(mock_config_root, 'test.yaml'), '-y']
#     out, err, exitcode = capture(command)

#     assert exitcode == 0

#     # Check output lines
#     outlines = out.split('\n')
#     assert len(outlines) == 15

#     # Check table header
#     assert outlines[1] == '|    iter    |     l2     ' \
#         + '|     q1     |     q2     |'
