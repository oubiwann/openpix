from openpix.commands import base
from openpix.util import oneOfCaseless
# XXX instead of this, let's use the component registry and adapt and ISystem
# to an ICaller or some such
from openpix.system import call as system


class InterfaceCommand(base.BaseCommand):
    """

    """
    summary = ""
    usage = ""
    skipHelp = False
    legalVerbs = oneOfCaseless("interface interf inter int i")

    def _doCommand(self, user):
        print system.call("ifconfig")
