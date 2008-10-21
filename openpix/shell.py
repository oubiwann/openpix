import readline

from openpix import util
from openpix import mode
from openpix import components
from openpix.system import backend
from openpix.system import call as system
from openpix.grammar.parser import Parser
from openpix.commands.base import getCommandClasses, getClassesWithSubcommands


class Completer(object):
    """
    A class for OpenPIX shell command completion.
    """
    def __init__(self, shell):
        self.shell = shell
        self.commands = []
        self.matches = []
        self.ignore = ['shorthelp']

    def getCommands(self):
        """

        """
        if self.commands:
            return self.commands
        commandData  = getCommandClasses(self.shell.mode)
        commands = [klass(self.shell.parser)
                    for name, klass in commandData]
        commands.sort()
        self.commands = [x for x in commands
                         if x.getCommandName() not in self.ignore]
        return self.commands

    def getCommandNames(self):
        """

        """
        return [x.getCommandName() for x in self.getCommands()]

    def getCommandNamesWithSubCommands(self):
        """

        """
        return [x.getCommandName() for x in self.getCommands()
                if hasattr(x, 'subcommands')]

    def getCommand(self, name):
        for command in self.getCommands():
            if command.getCommandName() == name:
                return command

    def getGlobalMatches(self, text):
        """

        """
        matches = []
        for commandName in self.getCommandNames():
            if commandName[:len(text)] == text:
                matches.append(commandName)
        return matches

    def getSubCommandMatches(self, commandName, text):
        """

        """
        matches = []
        subCommandNames = []
        command = self.getCommand(commandName)
        for subCommandVerb in [x[0] for x in command.subcommands.getLegalVerbs()]:
            subCommandName = subCommandVerb.returnString
            if subCommandName[:len(text)] == text:
                matches.append(subCommandName)
        return matches

    def tryComplete(self, data, error=IndexError):
        try:
            return data
        except error:
            return None

    def complete(self, text, state):
        """
        Return the next possible completion for 'text'.
        """
        buffer = readline.get_line_buffer()
        subCheck = buffer.split(" ")
        if state == 0:
            if len(subCheck) > 1:
                commandName = subCheck[0]
                subCommandName = subCheck[1]
                if commandName in self.getCommandNamesWithSubCommands():
                    self.matches = self.getSubCommandMatches(commandName, text)
            else:
                self.matches = self.getGlobalMatches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None


class User(object):
    """

    """
    def __init__(self, name):
        self.name = name
        self.logout = False


class Shell(object):
    """

    """
    def __init__(self):
        self.system = None
        self.mode = None
        self.backend = None
        self.user = None
        self.privUser = None
        self.parser = None
        self.prompt = ''
        self.setMode(mode.usermode)
        self.setSystem()
        self.registerComponents()

    def registerComponents(self):
        """

        """
        components.register()

    def setSystem(self):
        """
        Identify the type of system that the software is running on, import the
        appropriate module, instantiate the System object, and set it on the
        shell.
        """
        name = system.call("uname")
        if name == system.linux.System.uname:
            self.system = system.linux.System()
        elif name == system.openbsd.System.uname:
            self.system = system.openbsd.System()
        elif name == system.darwin.System.uname:
            self.system = system.darwin.System()

    def getSystem(self):
        """

        """
        return self.system

    def setBackend(self, name="pf"):
        """

        """
        if name == backend.pf.shortName:
            self.backend = backend.pf
        elif name == backend.iptables.shortName:
            self.backend = backend.iptables
        elif name == backend.ipf.shortName:
            self.backend = backend.ipf
        elif name == backend.ipfw.shortName:
            self.backend = backend.ipfw
        elif name == backend.ipchains.shortName:
            self.backend = backend.ipchains

    def getBackend(self):
        """

        """
        return self.backend

    def setUser(self, user):
        """

        """
        self.user = user

    def setMode(self, mode):
        """
        Mode is an object that has attributes which define the mode name and
        the mode prompt.
        """
        self.mode = mode

    def setUpCompletion(self):
        # XXX get max lines from config
        maxHistoryLines = 500
        readline.set_history_length(maxHistoryLines)
        readline.set_completer(Completer(self).complete)
        readline.parse_and_bind('tab: complete')

    def getMode(self):
        """

        """
        return self.mode

    def processResults(self, parseResults):
        """
        This function performs simple decision-making tasks based on the
        obtained results.
        """
        if parseResults is not None:
            cmd = parseResults.command
            # XXX
            # not sure if this switching logic should happen here or in the
            # command classes during __init__ and __call__
            if cmd.tokens.shortHelp:
                cmd.printShortHelp()
            elif cmd.tokens.privMode:
                # do authentication checks
                # XXX
                auth = True
                if auth:
                    self.setMode(mode.privmode)
                    cmd(self.user)
            elif self.mode == mode.privmode and cmd.tokens.exit:
                self.setMode(mode.usermode)
            else:
                cmd(self.user)

    def login(self, user):
        """
        This function does everything necessary to start a shell and parse
        commands as they are entered.
        """
        self.setUser(user)
        util.printBanner()
        self.setUpCompletion()
        # create parser
        self.parser = Parser(self)

    def run(self):
        while not self.user.logout:
            commandString = raw_input(self.getMode().prompt)
            self.processResults(
                self.parser.parseCommand(commandString, self.getMode()))

