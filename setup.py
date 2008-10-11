import openpix
from openpix import util


util.setup(
    name=openpix.name,
    version=openpix.version,
    description=openpix.description,
    author="Duncan McGreggor, Anthony Baxter",
    author_email="oubiwann@divmod.com",
    url=openpix.projectURL,
    packages=util.find_packages(),
    #scripts=['bin/pfShell.tac'],
    long_description=util.catReST(
        'README',
        'DEPENDENCIES',
         out=False),
    license='MIT',
    classifiers=[
       'Intended Audience :: System Administrators',
       'Intended Audience :: Developers',
       'Topic :: Internet',
       'Topic :: System :: Networking',
    ]

)
