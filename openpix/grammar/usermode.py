from pyparsing import Optional, Or, LineEnd

from openpix.commands import usermode


shortHelpOption = Optional(
    usermode.ShortHelpCommand.legalVerbs
    ).setResultsName('shortHelp')


class Grammar(object):
    """

    """
    def __init__(self, parser):
        self.parser = parser

    def getGrammar(self):
        """
        User EXEC mode lets you see minimum security appliance settings. The
        user EXEC mode prompt appears when you first access the security
        appliance.
        """
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

        quitCommand.setParseAction(
            parser.makeCommandParseAction(usermode.QuitCommand))
        helpCommand.setParseAction(
            parser.makeCommandParseAction(usermode.HelpCommand))
        shortHelpCommand.setParseAction(
            parser.makeCommandParseAction(usermode.ShortHelpCommand))
        enableCommand.setParseAction(
            parser.makeCommandParseAction(usermode.EnableCommand))
        pingCommand.setParseAction(
            parser.makeCommandParseAction(usermode.PingCommand))
        loginCommand.setParseAction(
            parser.makeCommandParseAction(usermode.LoginCommand))
        showCommand.setParseAction(
            parser.makeCommandParseAction(usermode.ShowCommand))
        tracerouteCommand.setParseAction(
            parser.makeCommandParseAction(usermode.TracerouteCommand))

        return Or([
            enableCommand, shortHelpCommand, helpCommand, quitCommand,
            pingCommand, loginCommand, showCommand, tracerouteCommand
            ]).setResultsName("command") + LineEnd()


