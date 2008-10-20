from zope.component.registry import Components

from openpix.grammar import usermode
from openpix.grammar.privmode import main as privmode


registry = Components("openpix")

def register():
    """

    """
    registry.registerAdapter(usermode.UserModeGrammar)
    registry.registerAdapter(privmode.PrivModeGrammar)
    
