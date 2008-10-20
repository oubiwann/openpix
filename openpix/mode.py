import socket

from zope.interface import implements

from openpix import interfaces


basePrompt = "openpix@%s" % socket.gethostname()
defaultPrompt = "%s> " % basePrompt
rootPrompt = "%s# " % basePrompt


class Mode(object):
    """
    A simple object for creating object hierarchies.
    """
    implements(interfaces.IMode)
    commandInterface = interfaces.ICommand

    def __hash__(self):
        return hash(self.__class__.__name__)


class UserMode(Mode):
    """

    """
    implements(interfaces.IUserMode)
    name = "user"
    username = "enable_1"
    level = 1
    modes = ["P_UNPR"]
    prompt = defaultPrompt
    commandInterface = interfaces.IUserCommand


class PrivMode(Mode):
    """

    """
    implements(interfaces.IPrivMode)
    name = "priv"
    username = "enable_15"
    modes = ["P_PRIV"]
    level = 15
    prompt = rootPrompt
    commandInterface = interfaces.IPrivCommand


class ConfigMode(Mode):
    """

    """
    implements(interfaces.IConfigMode)
    name = "config"
    username = "enable_15"
    level = 15
    modes = ["P_PRIV", "P_CONF"]
    prompt = None
    commandInterface = None


usermode = UserMode()

privmode = PrivMode()

configmode = ConfigMode()

