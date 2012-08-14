# -*- coding: utf-8 -*-

from subprocess import call
from pmmc.pte.pai import CONFIG_FILE, getURL

ARGPARSER_TITLE = 'opções específicas para o Opera'
ARGPARSER_DATA = (
    (True, {'args': ('-k', '--kiosk'),
            'kwargs': {'action': 'store_true',
                       'help': 'inicia o navegador em modo kiosk (tela cheia)'}},
           {'args': ('-n', '--normal'),
            'kwargs': {'action': 'store_false',
                       'dest': 'kiosk',
                       'help': 'inicia o navegador em modo normal (janela)'}}),
)


def setArgParserDefaults(parser, cfgparser):
	parser.set_defaults(local=cfgparser.getboolean('Opera', 'local'),
                            server=cfgparser.get('Opera', 'server address'),
                            kiosk=cfgparser.getboolean('Opera', 'kiosk mode'))


def loadConfig(parser):
	parser.read(CONFIG_FILE)

	if not parser.has_section('Opera'):
        	parser.add_section('Opera')
        	parser.set('Opera', 'kiosk mode', 'False')


def saveConfig(parser, args):
	parser.set('DEFAULT', 'local', str(args.local))
        parser.set('DEFAULT', 'server address', args.server)
        parser.set('Opera', 'kiosk mode', str(args.kiosk))

        with open(CONFIG_FILE, 'wb') as inifile:
                parser.write(inifile)


def launch(activity, page, kioskmode, local, server, verbose):
	cmd = ['opera', '-nosession', '-nomail', '-nomaillinks', '-nomenu', '-noprint', '-nosave']

	if kioskmode:
		cmd.extend(('-kioskmode', '-resetonexit'))

	cmd.append(getURL(activity.upper(), page, local, server, verbose=verbose))
	call(cmd)
