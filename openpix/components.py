from zope import component

from openpix.grammar import usermode
from openpix.grammar.privmode import main as privmode

def register():
    """

    """
    component.provideAdapter(usermode.UserModeGrammar)
    component.provideAdapter(privmode.PrivModeGrammar)
    
