from pyparsing import ParseException, LineEnd

from openpix.grammar.usermode import getUserEXECModeGrammar


class AppParseException(ParseException):
    pass


class Parser(object):
    def __init__(self):
        self.bnf = self.makeBNF()

    def makeCommandParseAction(self, cls):
        def cmdParseAction(string, location, tokens):
            return cls(tokens=tokens)
        return cmdParseAction

    def makeBNF(self):
        grammar = getUserEXECModeGrammar(self)
        return grammar.setResultsName("command") + LineEnd()

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

