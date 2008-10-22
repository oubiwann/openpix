import readline

from openpix import util
from openpix import mode
from openpix import components
from openpix.system import backend
from openpix.system import call as system
from openpix.grammar.parser import Parser
from openpix.command.base import getCommandClasses, getClassesWithSubcommands


class Completer(object):
    """
    A class for OpenPIX shell command completion.

    Completer's are a bit tricky because there doesn't seem to be too much
    clear and detailed documentation on them.

    XXX - add notes about state and text
    XXX - add notes about the completer methods in this class
    XXX - add notes about the subcommand method
    XXX - add notes about helper methods in this class
    """
    def __init__(self, shell):
        self.shell = shell
        self.matches = []

    def getGlobalMatches(self, text):
        """

        """
        matches = []
        for commandName in self.shell.getCommandNames():
            if commandName[:len(text)] == text:
                matches.append(commandName)
        return matches

    def getSubCommandMatches(self, commandName, text):
        """

        """
        matches = []
        subCommandNames = []
        command = self.shell.getCommand(commandName)
        for subCommandVerb in [x[0] for x in command.subcommands.getLegalVerbs()]:
            subCommandName = subCommandVerb.returnString
            if subCommandName[:len(text)] == text:
                matches.append(subCommandName)
        return matches

    def complete(self, text, state):
        """
        Return the next possible completion for 'text'.

        Note that subcommands take the following form, and are parsed as such:
            prompt> command [subcommand]

        And that help commands take this form:
            prompt> help command
        """
        subCheck = readline.get_line_buffer().split(" ")
        if state == 0:
            if len(subCheck) > 1:
                commandName = subCheck[0]
                subCommandName = subCheck[1]
                # completer for help
                if commandName == "help":
                    self.matches = self.getGlobalMatches(text)
                # completer for subcommands
                elif commandName in self.shell.getCommandNamesWithSubCommands():
                    self.matches = self.getSubCommandMatches(commandName, text)
            else:
                # general completer
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
        self._command_cache = []
        self._listing_ignore = ["shorthelp"]

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
        readline.parse_and_bind("tab: complete")

    def getMode(self):
        """

        """
        return self.mode

    def getCommands(self):
        """

        """
        if self._command_cache:
            return self._command_cache
        commandData  = getCommandClasses(self.mode)
        commands = [klass(self.parser)
                    for name, klass in commandData]
        commands.sort()
        self._command_cache = [x for x in commands
                         if x.getCommandName() not in self._listing_ignore]
        return self._command_cache

    def getCommandNames(self):
        """

        """
        return [x.getCommandName() for x in self.getCommands()]

    def getCommandNamesWithSubCommands(self):
        """
        Get the list of commands (in openpix.command) that have subcommands.
        """
        return [x.getCommandName() for x in self.getCommands()
                if hasattr(x, "subcommands")]

    def getCommand(self, name):
        """

        """
        for command in self.getCommands():
            if command.getCommandName() == name:
                return command

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
        #import pdb;pdb.set_trace()

    def run(self):
        while not self.user.logout:
            commandString = raw_input(self.getMode().prompt)
            self.processResults(
                self.parser.parseCommand(commandString, self.getMode()))

