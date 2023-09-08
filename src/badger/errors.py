class BadgerConfigError(Exception):
    pass


class VariableRangeError(Exception):
    pass


class BadgerNotImplementedError(Exception):
    pass


class BadgerRunTerminatedError(Exception):

    def __init__(self, message="Optimization run has been terminated!"):
        super().__init__(message)


class BadgerDBError(Exception):
    pass


class BadgerEnvVarError(Exception):
    pass


class BadgerIntfChannelError(Exception):
    pass


class BadgerInvalidPluginError(Exception):
    pass


class BadgerPluginNotFoundError(Exception):
    pass


class BadgerInvalidDocsError(Exception):
    pass


class BadgerLogbookError(Exception):
    pass


class BadgerLoadConfigError(Exception):
    pass


class BadgerRoutineError(Exception):
    pass
