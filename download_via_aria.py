#! /usr/bin/env python
################################################################################
#                                                                              #
#     download_via_aria.py                                                     #
#     Copyright (C) 2016  Md Safiyat Reza <reza.safiyat@acm.org>               #
#                                                                              #
#     This program is free software; you can redistribute it and/or modify     #
#     it under the terms of the GNU General Public License 2.0 as published by #
#     the Free Software Foundation.                                            #
#                                                                              #
#     This program is distributed in the hope that it will be useful,          #
#     but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#     GNU General Public License for more details.                             #
#                                                                              #
#     You should have received a copy of the GNU General Public License along  #
#     with this program; if not, write to the Free Software Foundation, Inc.,  #
#     51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.              #
#                                                                              #
################################################################################

import json
import os
import sys
import urllib2


def read_conf():
    """Read the default aria2 config file."""
    conf_path = os.path.join(os.environ['HOME'], '.aria2/aria2.conf')
    with open(conf_path) as fp:
        conf_text = fp.read()
    conf = dict()
    for line in conf_text.splitlines():
        splits = line.split('=', 1)
        if len(splits) == 2:
            conf[splits[0].strip()] = splits[1].strip()
        else:
            conf[splits[0]] = None
    return conf


def get_options():
    """Get the dict of supported options and their values from conf."""
    applicable_conf = ['rpc-secret', 'rpc-user', 'rpc-passwd', 'dir']
    conf_in_file = read_conf()
    conf = dict()
    for option in applicable_conf:
        if option in conf_in_file:
            conf[option] = conf_in_file[option]
    if ('rpc-user' in conf) ^ ('rpc-passwd' in conf):
        raise KeyError("Both the keys 'rpc-user' and 'rpc-passwd' should be "
                       "present in the configuration file.")
    return conf


def main():
    """The main method."""
    sys.stdout.write('Received args: %s\n' % (':-:'.join(sys.argv)))
    if os.path.isfile(os.path.join(os.environ['HOME'], '.aria2/aria2.conf')):
        conf = get_options()
    else:
        conf = None
    json_req = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                           'method': 'aria2.addUri',
                           'params': ['token:%s' % conf['rpc-secret'],
                                      [sys.argv[1]]]})
    c = urllib2.urlopen('http://localhost:6800/jsonrpc', json_req)
    c.read()

if __name__ == '__main__':
    sys.exit(main())
