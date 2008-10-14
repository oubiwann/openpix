from zope import component

from pyparsing import Optional, Or, LineEnd

from openpix import interfaces
from openpix.grammar import common
from openpix.commands import base
from openpix.commands import usermode


shortHelpOption = common.shortHelpOption

# define common command grammars
nullCommand = common.nullCommand

class UserModeGrammar(common.Grammar):
    """

    """
    component.adapts(interfaces.IParser, interfaces.IUserMode)

    def __init__(self, parser, mode):
        self.parser = parser
        self.mode = mode
        self.grammar = None
        self.buildGrammar()

    def buildGrammar(self):
        """

        """
        # define the commdands' grammars
        enableCommand = (
            usermode.EnableCommand.legalVerbs + shortHelpOption
            ).setResultsName('privMode')
        loginCommand = usermode.LoginCommand.legalVerbs + shortHelpOption
        quitCommand = usermode.QuitCommand.legalVerbs + shortHelpOption

        showOptions = Optional(
            Or(usermode.ShowSubCommands().getLegalVerbs())
            ).setResultsName('show')
        showCommand = (
            usermode.ShowCommand.legalVerbs + showOptions + shortHelpOption)

        shortHelpCommand = (
            usermode.ShortHelpCommand.legalVerbs + shortHelpOption)
        helpCommand = usermode.HelpCommand.legalVerbs + shortHelpOption

        pingCommand = usermode.PingCommand.legalVerbs + shortHelpOption
        tracerouteCommand = (
            usermode.TracerouteCommand.legalVerbs + shortHelpOption)

        # set the parse action
        nullCommand.setParseAction(
            self.makeCommandParseAction(base.NullCommand))
        quitCommand.setParseAction(
            self.makeCommandParseAction(usermode.QuitCommand))
        helpCommand.setParseAction(
            self.makeCommandParseAction(usermode.HelpCommand))
        shortHelpCommand.setParseAction(
            self.makeCommandParseAction(usermode.ShortHelpCommand))
        enableCommand.setParseAction(
            self.makeCommandParseAction(usermode.EnableCommand))
        pingCommand.setParseAction(
            self.makeCommandParseAction(usermode.PingCommand))
        loginCommand.setParseAction(
            self.makeCommandParseAction(usermode.LoginCommand))
        showCommand.setParseAction(
            self.makeCommandParseAction(usermode.ShowCommand))
        tracerouteCommand.setParseAction(
            self.makeCommandParseAction(usermode.TracerouteCommand))

        # set the complete grammar
        self.grammar = Or([
            nullCommand, enableCommand, shortHelpCommand, helpCommand, quitCommand,
            pingCommand, loginCommand, showCommand, tracerouteCommand
            ]).setResultsName("command") + LineEnd()

    def getGrammar(self):
        """
        User EXEC mode lets you see minimum security appliance settings. The
        user EXEC mode prompt appears when you first access the security
        appliance.
        """
        return self.grammar



