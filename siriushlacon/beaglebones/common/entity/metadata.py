class SingletonInstanceError(Exception):
    """
    A simple wrapper for singleton errors
    """
    pass


class Singleton(type):
    """
    Singleton metadata class. It allows only one instance per class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def get_instance(cls):
        """
        Returns the saved instance.
        :raise SingletonInstanceError: class has not been created before this call.
        :return: The single copy of the object instance. A new object is created if it has not been instantiated yet.
        """
        if cls in cls._instances.keys():
            return cls._instances[cls]

        raise SingletonInstanceError("{} class hasn't been created yet".format(cls))
