import inspect

from zope.interface import implements

from pyparsing import MatchFirst

from openpix import interfaces
from openpix import util
from openpix.util import oneOfCaseless


commandClasses = {}
subcCommandClasses = {}


def getModules(subpackage):
    """
    Get all the modules in a given subpackage.
    """
    return [x[1] for x in inspect.getmembers(subpackage, inspect.ismodule)]


def isCommandClass(klass):
    """
    A check that filters only top-level command classes.
    """
    if inspect.isclass(klass) and issubclass(klass, BaseCommand):
        return True
    return False


def isSubCommandClass(klass):
    """
    A check that filters second-level commands.
    """
    if inspect.isclass(klass) and issubclass(klass, BaseSubCommand):
        return True
    return False


def getClasses(data, mode=None, filter=isCommandClass):
    """
    Like inspect.getmembers, returuns a list of (class name, class) tuples.

    The 'data' parameter is for caching; the mode is used to determine which
    command-level to check for commands (e.g., user-mode, priv-mode, etc.), and
    the 'filter' parameter is used to get only command classes or only
    sub-command classes, etc.
    """
    from openpix import command

    classes = data.get(mode)
    if mode and classes:
        return classes
    modules = getModules(command)
    modules.extend(getModules(command.privmode))
    commands = []
    for module in modules:
        commands.extend(
            [x for x in inspect.getmembers(module, isCommandClass)])
    if mode:
        commands = [x for x in commands
                    if mode.commandInterface.implementedBy(x[1])]
        data[mode] = commands
    return commands


def getCommandClasses(mode=None):
    """
    Like inspect.getmembers, returuns a list of (class name, class) tuples.
    
    """
    return getClasses(commandClasses, mode, isCommandClass)


def getSubCommandClasses(mode=None):
    """
    Like inspect.getmembers, returuns a list of (class name, class) tuples.
    """
    return getClasses(subCommandClasses, mode, isSubCommandClass)


def getClassesWithSubcommands(mode=None):
    """

    """
    return [(name, klass) for name, klass in getCommandClasses(mode)
            if hasattr(klass, 'subcommands')]


class BaseCommand(object):
    """
    Base class for commands.
    """
    implements(interfaces.ICommand)
    skipHelp = True
    summary = ""
    usage = ""
    syntax = ""

    def __init__(self, parser, tokens=[]):
        self.parser = parser
        self.shell = self.parser.getShell()
        self.system = self.shell.getSystem()
        self.mode = self.shell.getMode()
        self.tokens = tokens

    def __call__(self, user):
        self.doCommand(user)

    def __cmp___(self, other):
        """

        """
        x, y = (self.getCommandName(), other.getCommandName())
        if x > y:
            return 1
        elif x == y:
            return 0
        return -1

    def doCommand(self, user):
        """
        This method provides the action for each command.

        This needs to be overridden by subclasses.
        """
        raise NotImplementedError

    def getCommandName(self):
        """

        """
        return self.__class__.__name__.replace('Command', '').lower()

    def getDesc(self):
        """

        """
        return self.__doc__.strip()

    def getUsage(self):
        """

        """
        return self.usage.strip() % self.getCommandName()

    def printShortHelp(self):
        """

        """
        print "\n  %s\n\n  %s\n" % (self.getSummary(), self.getUsage())

    def getSyntax(self):
        """

        """
        return self.syntax

    def getSummary(self):
        """

        """
        return self.summary

    def getHelp(self):
        """

        """
        syntax = self.getSyntax() or ""
        if syntax:
            syntax = "SYNTAX:\n\n\t%s\n" % syntax
        return "\nUSAGE:\n\n\t%s\n\nDESCRIPTION:\n\n\t%s\n\n%s" % (
            self.getUsage(), self.getDesc(), syntax)

    def printSubCommands(self):
        """

        """
        if hasattr(self, 'subcommands'):
            self.subcommands.printSubCommands()


class BaseSubCommand(object):
    """
    
    """
    def getLegalVerbs(self):
        """
        Get all the legal verbs for all the subcommands.
        """
        def isVerb(klass):
            """
            A member checker that ensures we get verb instances as created by
            oneOfCaseless.
            """
            if isinstance(klass, MatchFirst):
                return True
            return False
        klassData = inspect.getmembers(self, isVerb)
        return [klass for klassName, klass in klassData]

    def printSubCommands(self):
        """

        """
        print
        print "  Sub-commands:"
        for verb in self.getLegalVerbs():
            print "    %s" % verb.exprs[0].returnString
        print


class BaseHelpCommand(BaseCommand):
    """

    """
    skipHelp = True
    helpTextMethod = ""



