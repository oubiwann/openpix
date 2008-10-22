from zope import component

from pyparsing import Optional, Or, LineEnd

from openpix import interfaces
from openpix.grammar import common
from openpix import command
from openpix.command import usermode
from openpix.command import subcommand


shortHelpOption = common.shortHelpOption

# define common command grammars
nullCommand = common.nullCommand

class UserModeGrammar(common.Grammar):
    """
    User EXEC mode lets you see minimum security appliance settings. The
    user EXEC mode prompt appears when you first access the security
    appliance.
    """
    component.adapts(interfaces.IParser, interfaces.IUserMode)

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
            Or(subcommand.ShowSubCommands().getLegalVerbs())
            ).setResultsName('show')
        showCommand = (
            command.ShowCommand.legalVerbs + showOptions + shortHelpOption)

        shortHelpCommand = (
            command.ShortHelpCommand.legalVerbs + shortHelpOption)

        pingCommand = command.PingCommand.legalVerbs + shortHelpOption
        tracerouteCommand = (
            command.TracerouteCommand.legalVerbs + shortHelpOption)

        # set the parse action
        nullCommand.setParseAction(
            self.makeCommandParseAction(command.NullCommand))
        quitCommand.setParseAction(
            self.makeCommandParseAction(usermode.QuitCommand))
        self.helpCommand.setParseAction(
            self.makeCommandParseAction(command.HelpCommand))
        shortHelpCommand.setParseAction(
            self.makeCommandParseAction(command.ShortHelpCommand))
        enableCommand.setParseAction(
            self.makeCommandParseAction(usermode.EnableCommand))
        pingCommand.setParseAction(
            self.makeCommandParseAction(command.PingCommand))
        loginCommand.setParseAction(
            self.makeCommandParseAction(usermode.LoginCommand))
        showCommand.setParseAction(
            self.makeCommandParseAction(command.ShowCommand))
        tracerouteCommand.setParseAction(
            self.makeCommandParseAction(command.TracerouteCommand))

        # set the complete grammar
        self.grammar = Or([
            nullCommand, enableCommand, shortHelpCommand, self.helpCommand,
            quitCommand, pingCommand, loginCommand, showCommand,
            tracerouteCommand
            ]).setResultsName("command") + LineEnd()





