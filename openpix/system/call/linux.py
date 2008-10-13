from openpix.system.call import call


class System(object):
    uname = "Linux"
    longName = call("uname -a")
    call = classmethod(call)

