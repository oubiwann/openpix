from zope.interface import implements

from openpix import util
from openpix.command import base
from openpix.util import oneOfCaseless
from openpix.interfaces import IUserCommand


class EnableCommand(base.BaseCommand):
    """
    Turn on privileged commands
    """
    implements(IUserCommand)
    summary = "Turn on privileged commands"
    usage = "%s [<priv_level>]"
    skipHelp = False
    legalVerbs = oneOfCaseless("enable enab en")

    def doCommand(self, user):
        # XXX add support for changing the password
        pass


class LoginCommand(base.BaseCommand):
    """
    Log in as a particular user
    """
    implements(IUserCommand)
    summary = "Log in as a particular user"
    usage = "%s"
    skipHelp = False
    legalVerbs = oneOfCaseless("login logi")

    def doCommand(self, user):
        print "not implemented"


class QuitCommand(base.BaseCommand):
    """
    Disable privileged commands, end configuration mode, or logout
    """
    implements(IUserCommand)
    summary = "Exit from the EXEC"
    usage = "%s"
    skipHelp = False
    legalVerbs = oneOfCaseless("quit q exit ex logout logou logo")

    def doCommand(self, user):
        print "\nLogoff\n"
        user.logout = True


class ExitCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__


class LogoffCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__



