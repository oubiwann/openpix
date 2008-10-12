from pyparsing import (
    ParseException, oneOf, replaceWith, LineEnd, empty, Literal)

from openpix import command


class AppParseException(ParseException):
    pass


class Parser(object):
    def __init__(self):
        self.bnf = self.makeBNF()

    def makeCommandParseAction(self, cls):
        def cmdParseAction(s,l,tokens):
            return cls()
        return cmdParseAction

    def makeBNF(self):
        quitVerb = oneOf("quit q exit ex logout logou logo", caseless=True)
        helpVerb = oneOf("help h", caseless=True)
        pingVerb = oneOf("ping pi", caseless=True)
        loginVerb = oneOf("login logi", caseless=True)
        showVerb = oneOf("show sho sh", caseless=True)
        tracerouteVerb = oneOf("traceroute tracert trace trac tra tr",
                               caseless=True)
        shortHelpVerb = Literal("?")
        enableVerb = oneOf("enable enab en", caseless=True)

        quitCommand = quitVerb
        helpCommand = helpVerb
        pingCommand = pingVerb
        loginCommand = loginVerb
        showCommand = showVerb
        tracerouteCommand = tracerouteVerb
        enableCommand = enableVerb
        shortHelpCommand = shortHelpVerb

        quitCommand.setParseAction(
            self.makeCommandParseAction(command.QuitCommand))
        helpCommand.setParseAction(
            self.makeCommandParseAction(command.HelpCommand))
        shortHelpCommand.setParseAction(
            self.makeCommandParseAction(command.ShortHelpCommand))
        enableCommand.setParseAction(
            self.makeCommandParseAction(command.EnableCommand))
        pingCommand.setParseAction(
            self.makeCommandParseAction(command.PingCommand))
        loginCommand.setParseAction(
            self.makeCommandParseAction(command.LoginCommand))
        showCommand.setParseAction(
            self.makeCommandParseAction(command.ShowCommand))
        tracerouteCommand.setParseAction(
            self.makeCommandParseAction(command.TracerouteCommand))

        return (
            enableCommand | shortHelpCommand | helpCommand | quitCommand |
            pingCommand | loginCommand | showCommand | tracerouteCommand
            ).setResultsName("command") + LineEnd()

    def parseCommand(self, command):
        try:
            ret = self.bnf.parseString(command)
            return ret
        except AppParseException, e:
            print e.msg
        except ParseException, e:
            # XXX
            #print e
            print "ERROR: Invalid input detected."

