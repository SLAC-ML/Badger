# Badger: The Ocelot Optimizer Rebirth

## Installation

### Install the Badger core

Using `pip`: `pip install badger-opt`

Or using `conda`: `conda install -c conda-forge badger-opt`

### Get the Badger plugins

Clone the [badger plugins repo](https://github.com/SLAC-ML/Badger-Plugins) to some directory on your computer.

### Set up Badger

Once `badger-opt` is installed and you have the badger plugins cloned, run the following command:

```bash
badger
```

Follow the instructions and configure several paths that are needed by Badger.

## Usage

For all the implemented and planned CLI usage, please refer to [these slides](https://docs.google.com/presentation/d/1APlLgaRik2VPGL7FuxEUmwHvx6egTeIRaxBKGS1TnsE/edit#slide=id.ge68b2a5657_0_5). We'll highlight several common CLI use cases of Badger in the following sections.

### Get help

```bash
badger -h
```

Or [shoot me an email](mailto:zhezhang@slac.stanford.edu)!

### Show metadata of Badger

To show the version number and some other metadata such as plugin directory:

```bash
badger
```

### Get information of the algorithms

List all the available algorithms:

```bash
badger algo
```

Get the configs of a specific algorithm:

```bash
badger algo ALGO_NAME
```

You'll get something like:

```yaml
name: silly
version: '0.1'
dependencies:
  - numpy
params:
  dimension: 1
  max_iter: 42
```

Note that in order to use this plugin, you'll need to install the dependencies listed in the command output. This dependency installation will be handled automatically if the plugin was installed through the `badger install` command, but that command is not available yet (it is coming soon).

The `params` part shows all the intrinsic parameters that can be tuned when doing optimization with this algorithm.

### Get information of the environments

List all the available environments:

```bash
badger env
```

Get the configs of a specific environment:

```bash
badger env ENV_NAME
```

The command will print out something like:

```yaml
name: dumb
version: '0.1'
dependencies:
  - numpy
  - badger-opt
interface:
  - silly
environments:
  - silly
  - naive
params: null
variables:
  - q1: 0 -> 1
  - q2: 0 -> 1
  - q3: 0 -> 1
  - q4: 0 -> 1
  - s1: 0 -> 1
  - s2: 0 -> 1
observations:
  - l2
  - mean
  - l2_x_mean
```

There are several important properties here:

- `variables`: The tunable variables provided by this environment. You could choose a subset of the variables as the desicion variables for the optimization in the routine config. The allowed ranges (in this case, 0 to 1) are shown behind the corresponding variable names
- `observations`: The measurements provided by this environment. You could choose some observations as the objectives, and some other observations as the constraints in the routine config

### Run an optimization

```bash
badger run [-h] -a ALGO_NAME [-ap ALGO_PARAMS] -e ENV_NAME [-ep ENV_PARAMS] -c ROUTINE_CONFIG
```

The `-ap` and `-ep` optional arguments, and the `-c` argument accept either a `.yaml` file path or a yaml string. The configs set to `-ap` and `-ep` optional arguments should be treated as "patch" on the default algorithm and environment parameters, respectively, which means that you only need to specify the paramters that you'd like to change on top of the default configs, rather than pass in a full config. The content of the `ROUTINE_CONFIG` (aka routine configs) should look like this:

```yaml
variables:
  - x1: [-1, 0.5]
  - x2
objectives:
  - c1
  - y2: MINIMIZE
constraints:
  - y1:
      - GREATER_THAN
      - 0
  - c2:
      - LESS_THAN
      - 0.5
```

The `variables` and `objectives` properties are required, while the `constraints` property is optional. Just omit the `constraints` property if there are no constraints for your optimization problem. The names listed in `variables` should come from `variables` of the env specified by the `-e` argument, while the names listed in `objectives` and `constraints` should come from `observations` of that env.

Several example routine configs can be found in the `examples` folder.

Below are some example `badger run` commands. They were run from the Badger project root only because of a simpler relative path of the routine config:) You could run them from any directory, just remember to change the routine config path accordingly.

```bash
badger run -a silly -e TNK -c examples/silly_tnk.yaml
```

```bash
badger run -a silly -ap "dimension: 4" -e dumb -c examples/silly_dumb.yaml
```

```bash
badger run -a silly -ap "{dimension: 4, max_iter: 10}" -e dumb -c examples/silly_dumb.yaml
```

In order to run the following commands, you'll need to [set up xopt](https://github.com/ChristopherMayes/Xopt#installing-xopt) on your computer (since the algorithms are provided by xopt).

```bash
badger run -a cnsga -ap "max_generations: 10" -e TNK -c examples/cnsga_tnk.yaml
```

## Development

### Install the Badger core in editable mode

Clone this repo and `cd` to the project root, then install badger in dev mode:

```bash
pip install -e .
```

#### Uninstall Badger

To uninstall badger, run the following command under the project root:

```bash
python setup.py develop -u
```

### Develop algorithm plugins for Badger

Algorithm in Badger is just a function has the following signature:

```
result = optimize(evaluate, params)
```

Where `evaluate` is an evaluation function for the problem to be optimized, with the signature below:

```
Y, I, E = evaluate(X)
```

Here `X`, `Y` are the decision vectors and the objectives, respectively. `I` is the inequality constraints, `E` the equality constraints. `X` and `Y` are 2D arrays, and `I` and `E` are either 2D arrays or `None`, depends on whether the optimization problem has the corresponding constraints or not.

To see an example of a Badger algorithm plugin, please have a look at the algorithms in the [official Badger algo registry](https://github.com/SLAC-ML/Badger-Plugins/tree/master/algorithms).

For now, you could simply create a folder named after your algorithm under the `$BADGER_PLUGIN_ROOT/algorithms` directory, where `$BADGER_PLUGIN_ROOT` is the value for key `BADGER_PLUGIN_ROOT` when you run `badger config`, and put the `__init__.py`, `configs.yaml`, and an optional `README.md` into your algorithm folder.

You can then `badger algo` to see if your algorithm is there.

### Develop environment plugins for Badger

Before developing new environments for Badger, please have a look at the [available environments](https://github.com/SLAC-ML/Badger-Plugins/tree/master/environments) in the official Badger plugins repo.

The existing envs could boost up your new env development process since Badger supports **nested environments**, which means that you could use environments in other environment, to reuse the observations/variables in the existing environments. To see an example of a nested environment, please check out the code of `silly`, `naive`, and `dumb` envs in the official Badger env registry. Note `dumb = silly + naive`.

For now, you could simply create a folder named after your env under the `$BADGER_PLUGIN_ROOT/environments` directory, where `$BADGER_PLUGIN_ROOT` is the value for key `BADGER_PLUGIN_ROOT` when you run `badger config`, and put the `__init__.py`, `configs.yaml`, and an optional `README.md` into your env folder.

You can then `badger env` to see if your environment is there.
