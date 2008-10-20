from zope import component

from pyparsing import Optional, Or, LineEnd

from openpix import interfaces
from openpix.grammar import common
from openpix.commands import base
from openpix.commands.privmode import system


shortHelpOption = common.shortHelpOption

# define common command grammars
nullCommand = common.nullCommand

class PrivModeGrammar(common.Grammar):
    """
    Priv EXEC mode lets you see all appliance settings as well as enter
    into configuration mode where these settings may be changed.
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
        quitCommand = (
            system.QuitCommand.legalVerbs + shortHelpOption
            ).setResultsName("exit")

        # set the parse action for the common grammars
        nullCommand.setParseAction(
            self.makeCommandParseAction(base.NullCommand))

        # set the parse action
        interfaceCommand.setParseAction(
            self.makeCommandParseAction(system.InterfaceCommand))
        quitCommand.setParseAction(
            self.makeCommandParseAction(system.QuitCommand))

        # set the complete grammar
        self.grammar = Or([
            nullCommand, quitCommand, interfaceCommand
        ]).setResultsName("command") + LineEnd()



