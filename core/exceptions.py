class InstanceNotExistError(Exception):
    def __init__(self, message="Instance does not exists", *args):
        super().__init__(message, *args)
