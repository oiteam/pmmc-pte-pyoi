# -*- coding: utf-8 -*-

import os
from ConfigParser import SafeConfigParser
from argparse import ArgumentParser


class CfgParser(SafeConfigParser):
	def __init__(self, configfile):
		SafeConfigParser.__init__(self, {'local': 'True', 'server address': 'localhost', 'browser': 'firefox'})
		configdir = os.path.expanduser('~') + '/.config/pmmc/pte'

		if not os.path.exists(configdir):
			os.makedirs(configdir)

		self.read('/'.join((configdir, configfile)))


class ArgParser(ArgumentParser):
	def __init__(self, description=None):
		ArgumentParser.__init__(self, description=description)

		self.add_argument('-S', '--save',
                                  action='store_true',
                                  help='salva as configurações passadas pela linha de comando no arquivo de configuração')
		self.add_argument('-V', '--verbose',
                                  action='store_true',
                                  help='exibe informações mais detalhadas')

		#### BEGIN XGROUP
		xgroup = self.add_mutually_exclusive_group()
		xgroup.add_argument('-l', '--local',
                                    action='store_true',
                                    default=True,
                                    help='busca os arquivos de atividades em uma instalação local (default)')
		xgroup.add_argument('-r', '--remote',
                                    action='store_false',
                                    dest='local',
                                    help='busca os arquivos de atividades em um servidor remoto')
		#### END XGROUP

		self.add_argument('-s', '--server',
                                  default='localhost',
                                  help='define o endereço do servidor remoto como SERVER (útil quando empregado em conjunto com a opção -r)')

		self.add_argument('-b', '--browser',
                                  choices=('firefox', 'chromium-browser', 'google-chrome', 'opera'),
                                  help='escolhe o navegador a ser utilizado')

		# Hacks argparse's non-localizable messages
		self._action_groups[1].title = 'opções genéricas'
		self._actions[0].help = 'exibe esta mensagem de ajuda e sai'
