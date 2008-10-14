from zope import component
from zope.interface import implements

from pyparsing import ParseException, LineEnd

from openpix import mode
from openpix import interfaces


class AppParseException(ParseException):
    pass


class Parser(object):
    """

    """
    implements(interfaces.IParser)

    def __init__(self, shell):
        self.shell = shell

    def makeCommandParseAction(self, cls):
        """

        """
        def cmdParseAction(string, location, tokens):
            return cls(self, tokens=tokens)
        return cmdParseAction

    def parseCommand(self, command, mode):
        """

        """
        # switch grammars, based on the mode
        grammar = component.queryMultiAdapter(
            (self, mode), interfaces.IGrammarFactory).getGrammar()
        try:
            result = grammar.parseString(command)
            return result
        except AppParseException, e:
            print e.msg
        except ParseException, e:
            # XXX
            print e
            print "ERROR: Invalid input detected."

