from zope import component

from pyparsing import Optional, Or, LineEnd

from openpix import interfaces
from openpix.grammar import common
from openpix.commands.privmode import system


shortHelpOption = common.shortHelpOption


class PrivModeGrammar(common.Grammar):
    """

    """
    component.adapts(interfaces.IParser, interfaces.IPrivMode)

    def __init__(self, parser, mode):
        self.parser = parser
        self.mode = mode
        self.buildGrammar()

    def buildGrammar(self):
        """

        """
        # define the commdands' grammars
        interfaceCommand = (
            system.InterfaceCommand.legalVerbs + shortHelpOption)

        # set the parse action
        interfaceCommand.setParseAction(
            self.parser.makeCommandParseAction(system.InterfaceCommand))

        # set the complete grammar
        self.grammar = Or([interfaceCommand]
        ).setResultsName("command") + LineEnd()

    def getGrammar(self):
        """
        Priv EXEC mode lets you see all appliance settings as well as enter
        into configuration mode where these settings may be changed.
        """
        return self.grammar


