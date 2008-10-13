from zope.interface import Interface


class IMode(Interface):
    """
    An object representing an execution mode, with associated attributes.
    """


class ICommand(Interface):
    """
    
    """


class IUserCommand(ICommand):
    """

    """


class IPriveCommand(ICommand):
    """

    """


class IConfigCommand(ICommand):
    """

    """


