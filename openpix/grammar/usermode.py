from pyparsing import ParseException, replaceWith, empty, Literal, Optional

from openpix import command
from openpix.util import oneOfCaseless


shortHelp = Literal("?")

enableVerb = oneOfCaseless("enable enab en")
loginVerb = oneOfCaseless("login logi")
quitVerb = oneOfCaseless("quit q exit ex logout logou logo")

showVerb = oneOfCaseless("show sho sh")
shortHelpVerb = shortHelp
helpVerb = oneOfCaseless("help h")

pingVerb = oneOfCaseless("ping pi")
tracerouteVerb = oneOfCaseless("traceroute tracert trace trac tra tr")

shortHelpOption = Optional(shortHelp).setResultsName('shortHelp')

# show sub parts
"""
PIX:

  checksum  Display configuration information cryptochecksum
  curpriv   Display current privilege level
  flash:    Display information about flash: file system
  history   Display the session command history
  rip       IP RIP show commands
  sla       Service Level Agreement (SLA)
  track     Tracking information
  version   Display system software version

"""
versionVerb = oneOfCaseless("version ver")
licenseVerb = oneOfCaseless("license lisence lis lic li")
splashVerb = oneOfCaseless("splash splas spla spl")
bannerVerb = oneOfCaseless("banner ban")
copyrightVerb = oneOfCaseless("copyright copyr copy cop")
historyVerb = oneOfCaseless("history hist his")


def getUserEXECModeGrammar(parser):
    """
    User EXEC mode lets you see minimum security appliance settings. The user
    EXEC mode prompt appears when you first access the security appliance.
    """
    enableCommand = enableVerb + shortHelpOption
    loginCommand = loginVerb + shortHelpOption
    quitCommand = quitVerb + shortHelpOption

    showOptions = Optional(
        versionVerb |
        licenseVerb |
        splashVerb |
        bannerVerb |
        copyrightVerb |
        historyVerb
        ).setResultsName('show')
    showCommand = showVerb + showOptions + shortHelpOption

    shortHelpCommand = shortHelpVerb + shortHelpOption
    helpCommand = helpVerb + shortHelpOption

    pingCommand = pingVerb + shortHelpOption
    tracerouteCommand = tracerouteVerb + shortHelpOption

    quitCommand.setParseAction(
        parser.makeCommandParseAction(command.QuitCommand))
    helpCommand.setParseAction(
        parser.makeCommandParseAction(command.HelpCommand))
    shortHelpCommand.setParseAction(
        parser.makeCommandParseAction(command.ShortHelpCommand))
    enableCommand.setParseAction(
        parser.makeCommandParseAction(command.EnableCommand))
    pingCommand.setParseAction(
        parser.makeCommandParseAction(command.PingCommand))
    loginCommand.setParseAction(
        parser.makeCommandParseAction(command.LoginCommand))
    showCommand.setParseAction(
        parser.makeCommandParseAction(command.ShowCommand))
    tracerouteCommand.setParseAction(
        parser.makeCommandParseAction(command.TracerouteCommand))

    return (
        enableCommand | shortHelpCommand | helpCommand | quitCommand |
        pingCommand | loginCommand | showCommand | tracerouteCommand
        )
