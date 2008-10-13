import commands

def call(cmd):
    """
    Get shell stats and output of a command.
    """
    status, output = commands.getstatusoutput(cmd)
    # XXX do checking on status
    return output
