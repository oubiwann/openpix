from openpix.commands import base
from openpix.util import oneOfCaseless


class InterfaceCommand(base.BaseCommand):
    """

    """
    summary = ""
    usage = ""
    skipHelp = False
    legalVerbs = oneOfCaseless("interface interf inter int i")

    def _doCommand(self, user):
        print self.system.getInterface()


class QuitCommand(base.BaseCommand):
    """
    Disable privileged commands, end configuration mode, or logout
    """
    summary = "Exit from the EXEC"
    usage = "%s"
    skipHelp = False
    legalVerbs = oneOfCaseless("quit q exit ex logout logou logo")

    def _doCommand(self, user):
        print "\nLogoff\n"


class ExitCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__


class LogoffCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__



