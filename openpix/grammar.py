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
        quitVerb = oneOf("quit q exit ex logout", caseless=True)
        helpVerb = oneOf("help h", caseless=True)
        shortHelpVerb = Literal("?")
        enableVerb = oneOf("enable en", caseless=True)

        quitCommand = quitVerb
        helpCommand = helpVerb
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

        return (
            enableCommand | shortHelpCommand | helpCommand | quitCommand
            ).setResultsName("command") + LineEnd()

    def parseCommand(self, command):
        try:
            ret = self.bnf.parseString(command)
            return ret
        except AppParseException, e:
            print e.msg
        except ParseException, e:
            # XXX
            print e
            print "ERROR: Invalid input detected."

