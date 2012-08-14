# -*- coding: utf-8 -*-

from subprocess import call
from pmmc.pte.pai import CONFIG_FILE, getURL

ARGPARSER_TITLE = 'opções específicas para o Firefox'
ARGPARSER_DATA = (
    (False, {'args': ('-P', '--profile'),
             'kwargs': {'default': 'default',
                        'help': 'utiliza o perfil do Firefox PROFILE para navegar no PAI'}}),
)


def setArgParserDefaults(parser, cfgparser):
	parser.set_defaults(local=cfgparser.getboolean('Firefox', 'local'),
                            server=cfgparser.get('Firefox', 'server address'),
                            profile=cfgparser.get('Firefox', 'profile'))


def loadConfig(parser):
	parser.read(CONFIG_FILE)

	if not parser.has_section('Firefox'):
        	parser.add_section('Firefox')
        	parser.set('Firefox', 'profile', 'default')


def saveConfig(parser, args):
	parser.set('DEFAULT', 'local', str(args.local))
        parser.set('DEFAULT', 'server address', args.server)
        parser.set('Firefox', 'profile', args.profile)

        with open(CONFIG_FILE, 'wb') as inifile:
                parser.write(inifile)


def launch(activity, page, profile, local, server, verbose):
        url = getURL(activity.upper(), page, local, server, verbose)
        call(('firefox', '-P', profile, url))
