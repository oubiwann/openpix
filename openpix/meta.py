name = "OpenPIX"
shortName = "OpenPIX"
summary = "Security Appliance Shell"
description = "A PIX-like CLI for Open Source Firewalls"
version = "0.0.1"
longVersion = "%s: %s, Version %s" % (name, description, version)
projectURL = "https://launchpad.net/openpix"

copyright = """
Copyright (c) 2006-2008 Duncan McGreggor
Copyright (c) 2008 Duncan McGreggor, Canonical Ltd
"""

licenseType = "LGPL"
licenseVersion = "2.1"
licenseURL = "http://www.opensource.org/licenses/lgpl-2.1.php"

licenseReference = """
This application is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation; either version 2.1 of the License, or (at your
option) any later version.

This software is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this software; if not, write to the Free Software Foundation, Inc., 59
Temple Place, Suite 330, Boston, MA 02111-1307 USA.
"""
licenseNotice = "%s %s, %s\n%s%s" % (
    name, summary, description, copyright, licenseReference)
