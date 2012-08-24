#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pai
from subprocess import call

CONFIG_DIR = os.path.expanduser('~') + '/.config/pmmc/pte'
CONFIG_FILE = CONFIG_DIR + '/pai.conf'

if not os.path.exists(CONFIG_DIR):
	os.makedirs(CONFIG_DIR)

cfgparser = pai.CfgParser(CONFIG_FILE)
parser = pai.ArgParser()
parser.set_defaults(local=cfgparser.getboolean('DEFAULT', 'local'),
                    server=cfgparser.get('DEFAULT', 'server address'),
                    browser=cfgparser.get('DEFAULT', 'browser'),
                    profile=cfgparser.get('Firefox', 'profile'),
                    kiosk=cfgparser.getboolean('Chromium', 'kiosk mode'))
args = parser.parse_args()

if args.save:
	cfgparser.set('DEFAULT', 'local', str(args.local))
	cfgparser.set('DEFAULT', 'server address', args.server)
	cfgparser.set('DEFAULT', 'browser', args.browser)
	cfgparser.set('Firefox', 'profile', args.profile)
	cfgparser.set('Chromium', 'kiosk mode', str(args.kiosk))

	with open(CONFIG_FILE, 'wb') as inifile:
		cfgparser.write(inifile)

url = pai.getURL(args.activity.upper(), args.page, args.local, args.server, args.verbose)
cmdline = [args.browser]
	
if args.browser == 'firefox':
	cmdline.extend(('-P', args.profile, url))
elif args.browser in ('chromium-browser', 'google-chrome'):
	cmdline.append('--incognito')

	if args.local:
		cmdline.append('--allow-file-access-from-files')

	if args.kiosk:
		cmdline.extend(('--kiosk', url))
	else:
		cmdline.append('--app=%s' % url)
elif args.browser == 'opera':
	cmdline.extend(('-nosession', '-nomail', '-nomaillinks', '-nomenu', '-noprint', '-nosave'))

	if args.kiosk:
		cmdline.extend(('-kioskmode', '-resetonexit'))

	cmdline.append(url)
else:
	cmdline.append(url)

call(cmdline)
