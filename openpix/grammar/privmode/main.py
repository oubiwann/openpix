from zope import component

from pyparsing import Optional, Or, LineEnd

from openpix import interfaces
from openpix import grammar
from openpix.grammar import base
from openpix import command
from openpix.command import subcommand
from openpix.command.privmode import system


shortHelpOption = grammar.shortHelpOption

# define common, non-class command grammars
nullCommand = grammar.nullCommand

class PrivModeGrammar(base.Grammar):
    """
    Priv EXEC mode lets you see all appliance settings as well as enter
    into configuration mode where these settings may be changed.
    """
    component.adapts(interfaces.IParser, interfaces.IPrivMode)

    def buildGrammar(self):
        """

        """
        # define the common grammars
        quitCommand = (
            system.QuitCommand.legalVerbs + shortHelpOption
            ).setResultsName("exit")

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

        nullCommand.setParseAction(
            self.makeCommandParseAction(command.NullCommand))

        # privmode grammar: system
        interfaceCommand = (
            system.InterfaceCommand.legalVerbs + shortHelpOption)

        # set the common parse actions
        quitCommand.setParseAction(
            self.makeCommandParseAction(system.QuitCommand))
        showCommand.setParseAction(
            self.makeCommandParseAction(command.ShowCommand))
        shortHelpCommand.setParseAction(
            self.makeCommandParseAction(command.ShortHelpCommand))

        self.helpCommand.setParseAction(
            self.makeCommandParseAction(command.HelpCommand))

        pingCommand.setParseAction(
            self.makeCommandParseAction(command.PingCommand))
        tracerouteCommand.setParseAction(
            self.makeCommandParseAction(command.TracerouteCommand))

        # privmode parse action: system
        interfaceCommand.setParseAction(
            self.makeCommandParseAction(system.InterfaceCommand))

        # set the complete grammar
        self.grammar = Or([
            nullCommand, quitCommand, interfaceCommand, showCommand,
            self.helpCommand, shortHelpCommand, pingCommand, tracerouteCommand,
        ]).setResultsName("command") + LineEnd()



