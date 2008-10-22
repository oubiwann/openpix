from openpix.command import base
from openpix.util import oneOfCaseless


class ShowSubCommands(base.BaseSubCommand):
    """
    The subcommands for the show command.

    PIX:
        checksum  Display configuration information cryptochecksum
        curpriv   Display current privilege level
        flash:    Display information about flash: file system
        history   Display the session command history
        rip       IP RIP show commands
        sla       Service Level Agreement (SLA)
        track     Tracking information
        version   Display system software version
    """
    version = oneOfCaseless("version ver")
    license = oneOfCaseless("license lisence lis lic li")
    splash = oneOfCaseless("splash splas spla spl")
    banner = oneOfCaseless("banner ban")
    copyright = oneOfCaseless("copyright copyr copy cop")
    history = oneOfCaseless("history hist his")
    backend = oneOfCaseless("backend back")
    system = oneOfCaseless("system syst sys")
