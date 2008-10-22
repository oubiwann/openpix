from zope.interface import implements

from pyparsing import Optional, empty, oneOf

from openpix import command


shortHelpOption = Optional(
    command.ShortHelpCommand.legalVerbs).setResultsName('shortHelp')
nullCommand = Optional(empty)


