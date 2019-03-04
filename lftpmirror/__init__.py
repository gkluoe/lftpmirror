# Copyright 2018 Geoff Lee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The lftpmirror tool"""
#!/usr/bin/python

import subprocess 
import sys
import argparse

DESCRIPTION = 'Back up some sources to a target'
VERSION = '0.0.2'

def main():
    args = process_args()

    server = args.server
    port = args.port
    user = args.user

    sources = args.sources.split(',') 

    target = args.target 

    if args.erase:
        cmd='rm -r {}/\n'.format(target)
    else:
        cmd=''

    for source in sources:
        cmd += 'mirror -e --verbose=5 --reverse {} {}\n'.format(source, target+source)

    ftp = subprocess.Popen(['lftp', '-u', user, 'sftp://{}:{}'.format(server, port)], stdin=subprocess.PIPE)

    ftp.communicate(cmd)


def process_args(argv=None):
    """Process any commandline arguments"""
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     version=VERSION)


    parser.add_argument("-e", "--erase", help="Erase everything in the target directory before starting: DESTRUCTIVE!",
                    action="store_true")

    parser.add_argument("-d", "--dest-host", help="Server where target directory lives",
                    dest="server", required=True)

    parser.add_argument("-p", "--port", help="Port to use to connect to target server",
		    required=True)
    
    parser.add_argument("-u", "--user", help="Username,password (use 'username, for no password)",
                    required=True)

    parser.add_argument("-s", "--sources", help="Comma-separated list of source directories",
                    required=True)

    parser.add_argument("target", help="Target directory on the remote server",
                    )

    args = parser.parse_args(argv)
    return args


if __name__ == "__main__":
    main()
