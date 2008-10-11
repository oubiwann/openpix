from openpix import meta
from openpix import util


util.setup(
    name=meta.name,
    version=meta.version,
    description=meta.description,
    author="Duncan McGreggor, Anthony Baxter",
    author_email="oubiwann@divmod.com",
    url=meta.projectURL,
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
