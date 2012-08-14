# -*- coding: utf-8 -*-

from subprocess import call
from pmmc.pte.pai import CONFIG_FILE, getURL

ARGPARSER_TITLE = 'opções específicas para o Chromium/Google Chrome'
ARGPARSER_DATA = (
    (True, {'args': ('-k', '--kiosk'),
            'kwargs': {'action': 'store_true',
                       'help': 'inicia o navegador em modo kiosk (tela cheia)'}},
           {'args': ('-A', '--app'),
            'kwargs': {'action': 'store_false',
                       'dest': 'kiosk',
                       'help': 'inicia o navegador em modo aplicativo'}}),
)


def setArgParserDefaults(parser, cfgparser):
	parser.set_defaults(local=cfgparser.getboolean('Chromium', 'local'),
                            server=cfgparser.get('Chromium', 'server address'),
                            kiosk=cfgparser.getboolean('Chromium', 'kiosk mode'))


def loadConfig(parser):
	parser.read(CONFIG_FILE)

	if not parser.has_section('Chromium'):
        	parser.add_section('Chromium')
        	parser.set('Chromium', 'kiosk mode', 'False')


def saveConfig(parser, args):
	parser.set('DEFAULT', 'local', str(args.local))
        parser.set('DEFAULT', 'server address', args.server)
        parser.set('Chromium', 'kiosk mode', str(args.kiosk))

        with open(CONFIG_FILE, 'wb') as inifile:
                parser.write(inifile)


def launch(activity, page, kioskmode, local, server, verbose, browser='chromium-browser'):
	cmd = [browser, '--incognito']

        if local:
		cmd.append('--allow-file-access-from-files')

	if kioskmode:
		cmd.extend(('--kiosk', getURL(activity.upper(), page, local, server, verbose)))
	else:
		cmd.append('--app=%s' % getURL(activity.upper(), page, local, server, verbose))

	call(cmd)
