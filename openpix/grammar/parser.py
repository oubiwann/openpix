from pyparsing import ParseException, LineEnd

from openpix import constants
from openpix.grammar.usermode import getUserEXECModeGrammar
from openpix.grammar.configmode import getConfigModeGrammar
from openpix.grammar.privmode.main import getPrivEXECModeGrammar


class AppParseException(ParseException):
    pass


class Parser(object):
    def __init__(self, shell):
        self.shell = shell
        self.bnfs = self.makeBNFs()

    def makeCommandParseAction(self, cls):
        """

        """
        def cmdParseAction(string, location, tokens):
            return cls(self, tokens=tokens)
        return cmdParseAction

    def makeBNFs(self):
        """

        """
        return {
            constants.usermode.name: getUserEXECModeGrammar(self),
            constants.privmode.name: getPrivEXECModeGrammar(self),
            constants.configmode.name: getConfigModeGrammar(self),
            }

    def getGrammar(self, mode):
        """

        """
        return self.bnfs[mode.name]

    def parseCommand(self, command, mode):
        """

        """
        # switch grammars, based on the mode
        grammar = self.getGrammar(mode)
        try:
            ret = grammar.parseString(command)
            return ret
        except AppParseException, e:
            print e.msg
        except ParseException, e:
            # XXX
            print e
            print "ERROR: Invalid input detected."

