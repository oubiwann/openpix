from pyparsing import ParseException, oneOf, replaceWith, LineEnd, empty

from openpix import command


class AppParseException(ParseException):
    pass


class Parser(object):
    def __init__(self):
        self.bnf = self.makeBNF()

    def makeCommandParseAction( self, cls ):
        def cmdParseAction(s,l,tokens):
            return cls(tokens)
        return cmdParseAction

    def makeBNF(self):
        moveVerb = oneOf("MOVE GO", caseless=True) | empty
        quitVerb = oneOf("QUIT Q", caseless=True)
        helpVerb = oneOf("H HELP ?",caseless=True)

        nDir = oneOf("N NORTH",caseless=True).setParseAction(replaceWith("N"))
        sDir = oneOf("S SOUTH",caseless=True).setParseAction(replaceWith("S"))
        eDir = oneOf("E EAST",caseless=True).setParseAction(replaceWith("E"))
        wDir = oneOf("W WEST",caseless=True).setParseAction(replaceWith("W"))
        moveDirection = nDir | sDir | eDir | wDir

        moveCommand = moveVerb + moveDirection.setResultsName("direction")
        quitCommand = quitVerb
        helpCommand = helpVerb

        moveCommand.setParseAction(
            self.makeCommandParseAction( command.MoveCommand ) )
        quitCommand.setParseAction(
            self.makeCommandParseAction( command.QuitCommand ) )
        helpCommand.setParseAction(
            self.makeCommandParseAction( command.HelpCommand ) )

        return (
                  moveCommand |
                  helpCommand |
                  quitCommand ).setResultsName("command") + LineEnd()

    def parseCmd(self, cmdstr):
        try:
            ret = self.bnf.parseString(cmdstr)
            return ret
        except AppParseException, pe:
            print pe.msg
        except ParseException, pe:
            print "ERROR: Invalid input detected."

