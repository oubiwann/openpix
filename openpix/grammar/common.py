from zope.interface import implements

from pyparsing import Optional, empty, oneOf

from openpix import interfaces
# XXX the following imported code needs to be moved from usermode into either
# commands.base or commands.common and then imported from there
from openpix.command import base
from openpix.command import usermode

shortHelpOption = Optional(
    base.ShortHelpCommand.legalVerbs).setResultsName('shortHelp')
nullCommand = Optional(empty)


class Grammar(object):
    """

    """
    implements(interfaces.IGrammarFactory)

    def __init__(self, parser, mode):
        self.parser = parser
        self.shell = parser.getShell()
        self.mode = mode
        self.grammar = None
        self.buildHelpers()
        self.buildGrammar()

    def makeCommandParseAction(self, klass):
        """
        A decorator that instantiates the command class that is ultimately
        responsible for carrying out the command execution (klass.doCommand).
        """
        def commandParseAction(string, location, tokens):
            return klass(self.parser, tokens=tokens)
        return commandParseAction

    def buildHelpers(self):
        """
        This method sets up helper grammars that are useful to more than one
        subclass but depend upon the grammar class or one or more of its
        attribtues in order to be created.
        """
        # note that allCommandNames is intended to be used with help, in the
        # second position; this is the position of "subcommand", thus the
        # result name
        self.allCommandNames = oneOf(
            self.shell.getCommandNames()).setResultsName("subCommand")
        self.helpCommand = (
            base.HelpCommand.legalVerbs +
            self.allCommandNames +
            shortHelpOption)

    def buildGrammar(self):
        """

        """
        raise NotImplementedError

    def getGrammar(self):
        """

        """
        return self.grammar


