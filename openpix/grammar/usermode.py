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
            Or(base.ShowSubCommands().getLegalVerbs())
            ).setResultsName('show')
        showCommand = (
            base.ShowCommand.legalVerbs + showOptions + shortHelpOption)

        shortHelpCommand = (
            base.ShortHelpCommand.legalVerbs + shortHelpOption)
        helpCommand = base.HelpCommand.legalVerbs + shortHelpOption

        pingCommand = base.PingCommand.legalVerbs + shortHelpOption
        tracerouteCommand = (
            base.TracerouteCommand.legalVerbs + shortHelpOption)

        # set the parse action
        nullCommand.setParseAction(
            self.makeCommandParseAction(base.NullCommand))
        quitCommand.setParseAction(
            self.makeCommandParseAction(usermode.QuitCommand))
        helpCommand.setParseAction(
            self.makeCommandParseAction(base.HelpCommand))
        shortHelpCommand.setParseAction(
            self.makeCommandParseAction(base.ShortHelpCommand))
        enableCommand.setParseAction(
            self.makeCommandParseAction(usermode.EnableCommand))
        pingCommand.setParseAction(
            self.makeCommandParseAction(base.PingCommand))
        loginCommand.setParseAction(
            self.makeCommandParseAction(usermode.LoginCommand))
        showCommand.setParseAction(
            self.makeCommandParseAction(base.ShowCommand))
        tracerouteCommand.setParseAction(
            self.makeCommandParseAction(base.TracerouteCommand))

        # set the complete grammar
        self.grammar = Or([
            nullCommand, enableCommand, shortHelpCommand, helpCommand,
            quitCommand, pingCommand, loginCommand, showCommand,
            tracerouteCommand
            ]).setResultsName("command") + LineEnd()

    def getGrammar(self):
        """
        User EXEC mode lets you see minimum security appliance settings. The
        user EXEC mode prompt appears when you first access the security
        appliance.
        """
        return self.grammar


