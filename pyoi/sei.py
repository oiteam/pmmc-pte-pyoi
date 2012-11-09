# -*- coding: utf-8 -*-

import pyoi
from urllib2 import urlopen


def _getPath(suffix, local, server):
	if local:
		prefix = 'file:///opt/pmmc/pte/sei'
	else:
		prefix = '/'.join(('http:/', server, 'sei'))

	return '/'.join((prefix, suffix))


def getURL(local=True, server='localhost', verbose=False):
	return _getPath('sei.html', local, server)


class CfgParser(pyoi.CfgParser):
	def __init__(self, configfile='sei.conf'):
		pyoi.CfgParser.__init__(self, configfile)

		if not self.has_section('Firefox'):
			self.add_section('Firefox')
			self.set('Firefox', 'profile', 'default')

		if not self.has_section('Chromium'):
			self.add_section('Chromium')
			self.set('Chromium', 'kiosk mode', 'False')


class ArgParser(pyoi.ArgParser):
	def __init__(self):
		pyoi.ArgParser.__init__(self, description='PySEI - lançador/cliente para o SEI com funcionalidades adicionais')

		########## SEI SPECIFIC OPTIONS ##########
		## none at moment

		########## FIREFOX SPECIFIC OPTIONS ##########
		group = self.add_argument_group('opções específicas para o Firefox')
		group.add_argument('-P', '--profile',
                                   default='default',
                                   help='utiliza o perfil do Firefox PROFILE para navegar no SEI')

		########## CHROMIUM/GOOGLE CHROME/OPERA SPECIFIC OPTIONS ##########
		group = self.add_argument_group('opções específicas para o Chromium/Google Chrome/Opera')

		### BEGIN XGROUP
		xgroup = group.add_mutually_exclusive_group()

		xgroup.add_argument('-k', '--kiosk',
                                    action='store_true',
                                    help='inicia o navegador em modo kiosk (tela cheia)')
		xgroup.add_argument('-w', '--windowed',
                                    action='store_false',
                                    dest='kiosk',
                                    help='inicia o navegador em modo janela')
		### END XGROUP
