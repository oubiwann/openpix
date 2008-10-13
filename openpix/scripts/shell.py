from openpix.shell import Shell, User

# XXX do something more meaningful with user... like os.getlogin
user = User("Bob")

def run():
    shell = Shell()
    shell.login(user)
    shell.run()
