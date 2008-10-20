from zope.interface import implements

from pyparsing import Optional, empty

from openpix import interfaces
# XXX the following imported code needs to be moved from usermode into either
# commands.base or commands.common and then imported from there
from openpix.commands import base
from openpix.commands import usermode


shortHelpOption = Optional(
    base.ShortHelpCommand.legalVerbs).setResultsName('shortHelp')

nullCommand = Optional(empty)

class Grammar(object):
    """

    """
    implements(interfaces.IGrammarFactory)

    def __init__(self, parser, mode):
        self.parser = parser
        self.mode = mode
        self.grammar = None

    def makeCommandParseAction(self, klass):
        """
        A decorator that instantiates the command class that is ultimately
        responsible for carrying out the command execution (klass._doCommand).
        """
        def commandParseAction(string, location, tokens):
            return klass(self.parser, tokens=tokens)
        return commandParseAction


    def getGrammar(self):
        """

        """
        return self.grammar


