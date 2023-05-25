from abc import ABC, abstractmethod
from typing import List, Dict, Optional, final
from pydantic import Field, BaseModel
from .interface import Interface
# from .utils import merge_params


def validate_variable_names(func):
    def validate(cls, variable_names: List[str]):
        variable_names_invalid = [name for name in variable_names
                                  if name not in cls.variables]
        if len(variable_names_invalid):
            raise ValueError(f"Variables {variable_names_invalid} not found in environment")

        return func(cls, variable_names)

    return validate


def validate_observable_names(func):
    def validate(cls, observable_names: List[str]):
        observable_names_invalid = [name for name in observable_names
                                    if name not in cls.observables]
        if len(observable_names_invalid):
            raise ValueError(f"Observables {observable_names_invalid} not found in environment")

        return func(cls, observable_names)

    return validate


def validate_setpoints(func):
    def validate(cls, variable_inputs: Dict[str, float]):
        _bounds = cls._get_bounds(list(variable_inputs.keys()))
        for name, value in variable_inputs.items():

            lower = _bounds[name][0]
            upper = _bounds[name][1]

            if value > upper or value < lower:
                raise ValueError(f"Input point for {name} is outside its bounds {_bounds[name]}")

        return func(cls, variable_inputs)

    return validate


class Environment(BaseModel, ABC):

    name: str
    variables: List[str]
    observables: List[str]
    interface: Optional[Interface] = None
    params: Optional[Dict] = Field({}, description='Environment parameters')

    # Cache of variable bounds
    _bounds: Optional[Dict[str, List[float]]] = None

    class Config:
        validate_assignment = True
        use_enum_values = True
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    ############################################################
    # Must-inherit methods
    ############################################################

    @abstractmethod
    def get_variables(self, variable_names: List[str]) -> Dict:
        pass

    @abstractmethod
    def set_variables(self, variable_inputs: Dict[str, float]):
        pass

    @abstractmethod
    def get_observables(self, observable_names: List[str]) -> Dict:
        pass

    @abstractmethod
    def get_bounds(self, variable_names: List[str]) -> Dict[str, List[float]]:
        pass

    ############################################################
    # Optional methods to inherit
    ############################################################

    # Actions to preform after changing vars and before reading vars/obj
    def variables_changed(self, variables_input: Dict[str, float]):
        pass

    # Get current system states
    # If return is not None, the states would be saved at the start of each run
    # Should return a dict if not None
    def get_system_states(self) -> Optional[Dict]:
        return None

    ############################################################
    # Should never be overridden
    ############################################################

    # Optimizer will only call this method to get variable values
    @final
    def _get_variables(self, variable_names: List[str]) -> Dict:
        # Deal with variables defined in env
        variable_names_def = [v for v in variable_names if v in self.variables]
        variable_outputs_def = self.get_variables(variable_names_def)

        # Deal with tmp variables
        # Usually should be able to read from the interface
        variable_names_tmp = [v for v in variable_names
                              if v not in self.variables]

        # If no undefined variables
        if not len(variable_names_tmp):
            return variable_outputs_def

        # If no interface
        if self.interface is None:
            raise Exception(f'Variables {variable_names_tmp} do not exist in the environment!')

        # Try reading variable values from the interface
        try:
            variable_outputs_tmp = self.interface.get_values(variable_names_tmp)
        except Exception:  # TODO: specify what exceptions could occur
            raise Exception(f'Error reading variables {variable_names_tmp} from the interface!')

        return {**variable_outputs_def, **variable_outputs_tmp}

    # The reason for this method is we cannot know the bounds of a variable
    # that exists in interface but not defined in environment.
    # So we can only validate the setpoints for the defined variables
    @final
    @validate_setpoints
    def _set_variables_def(self, variable_inputs: Dict[str, float]):
        self.set_variables(variable_inputs)

    # Optimizer will only call this method to set variable values
    @final
    def _set_variables(self, variable_inputs: Dict[str, float]):
        # Deal with variables defined in env
        variable_inputs_def = dict([v for v in variable_inputs.items()
                                    if v[0] in self.variables])
        self._set_variables_def(variable_inputs_def)

        # Deal with tmp variables
        # Usually should be able to directly set to the interface
        variable_inputs_tmp = dict([v for v in variable_inputs.items()
                                    if v[0] not in self.variables])
        variable_names_tmp = list(variable_inputs_tmp.keys())

        # If no undefined variables
        if not len(variable_inputs_tmp):
            return

        # If no interface
        if self.interface is None:
            raise Exception(f'Variables {variable_names_tmp} do not exist in the environment!')

        # Try setting variable values directly through the interface
        try:
            self.interface.set_values(variable_inputs_tmp)
        except Exception:  # TODO: specify what exceptions could occur
            raise Exception(f'Error setting variables {variable_names_tmp} through the interface!')

    # Optimizer will only call this method to get observable values
    @final
    @validate_observable_names
    def _get_observables(self, observable_names: List[str]) -> Dict:
        return self.get_variables(observable_names)

    # Optimizer will only call this method to get variable bounds
    # Lazy loading -- read the bounds only when they are needed
    # TODO: considering cache validation (is it needed?)
    @final
    @validate_variable_names
    def _get_bounds(self, variable_names: Optional[List[str]] = None) -> Dict[str, List[float]]:
        if variable_names is None:
            variable_names = self.variables

        if self._bounds is None:
            self._bounds = self.get_bounds(variable_names)
        else:
            variable_names_new = [v for v in variable_names
                                  if v not in self._bounds.keys()]
            if len(variable_names_new):
                self._bounds.update(self.get_bounds(variable_names_new))

        return {k: self._bounds[k] for k in variable_names}
