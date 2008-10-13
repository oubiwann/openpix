import socket

from zope.interface import implements

from openpix.interfaces import IMode


class Mode(object):
    """
    A simple object for creating object hierarchies.
    """
    implements(IMode)

    def __hash__(self):
        return hash(self.__dict__)


basePrompt = "openpix@%s" % socket.gethostname()
defaultPrompt = "%s> " % basePrompt
rootPrompt = "%s# " % basePrompt

usermode = Mode()
usermode.name = "user"
usermode.username = "enable_1"
usermode.level = 1
usermode.modes = ["P_UNPR"]
usermode.prompt = defaultPrompt

privmode = Mode()
privmode.name = "priv"
privmode.username = "enable_15"
privmode.level = 15
privmode.modes = ["P_PRIV"]
privmode.prompt = rootPrompt

configmode = Mode()
configmode.name = "config"
configmode.username = "enable_15"
configmode.level = 15
configmode.modes = ["P_PRIV", "P_CONF"]

