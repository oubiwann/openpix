from zope import component

from pyparsing import Optional, Or, LineEnd

from openpix import interfaces
from openpix.grammar import common
from openpix.commands import usermode


shortHelpOption = common.shortHelpOption


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
        quitCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.QuitCommand))
        helpCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.HelpCommand))
        shortHelpCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.ShortHelpCommand))
        enableCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.EnableCommand))
        pingCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.PingCommand))
        loginCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.LoginCommand))
        showCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.ShowCommand))
        tracerouteCommand.setParseAction(
            self.parser.makeCommandParseAction(usermode.TracerouteCommand))

        # set the complete grammar
        self.grammar = Or([
            enableCommand, shortHelpCommand, helpCommand, quitCommand,
            pingCommand, loginCommand, showCommand, tracerouteCommand
            ]).setResultsName("command") + LineEnd()

    def getGrammar(self):
        """
        User EXEC mode lets you see minimum security appliance settings. The
        user EXEC mode prompt appears when you first access the security
        appliance.
        """
        return self.grammar



