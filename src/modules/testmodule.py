#!/usr/bin/env python3
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014, Teo Mrnjavac <teo@kde.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import sys

import yaml

try:
    import libcalamares
except ImportError:
    print( "Failed to import libcalamares. Make sure then PYTHONPATH environment variable includes the dir where libcalamares.so is installed." )
    print()
    raise


class Job:
    def __init__( self, workingPath, doc ):
        self.prettyName = "Testing job " + doc[ "name" ]
        self.workingPath = workingPath
        self.configuration = doc[ "configuration" ]

    def setprogress( self, progress ):
        print ( "Job set progress to {}%.".format( progress * 100 ) )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( "moduledir",
                         help = "Dir containing the Python module" )
    parser.add_argument( "globalstorage_yaml", nargs = "?",
                         help = "A yaml file to initialize GlobalStorage" )
    args = parser.parse_args()

    print( "Testing module in: " + args.moduledir )

    confpath = os.path.join( args.moduledir, "module.conf" )
    with open( confpath ) as f:
        doc = yaml.load( f )

    if doc[ "type" ] != "job" or doc[ "interface" ] != "python":
        print( "Only Python jobs can be tested." )
        return 1

    libcalamares.job = Job( args.moduledir, doc )
    libcalamares.global_storage = libcalamares.GlobalStorage()

    # if a file for simulating global_storage contents is provided, load it
    if args.globalstorage_yaml:
        with open( args.globalstorage_yaml ) as f:
            doc = yaml.load( f )
        for key, value in doc.items():
            libcalamares.global_storage.insert( key, value )

    scriptpath = os.path.abspath( args.moduledir )
    sys.path.append( scriptpath )
    import main

    print( "Output from module:" )
    print( main.calamares_main() )

    return 0


if __name__ == "__main__":
    sys.exit( main() )