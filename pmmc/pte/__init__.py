# -*- coding: utf-8 -*-

import os

CONFIG_DIR = os.path.expanduser('~') + '/.config/pmmc/pte'

#ARGPARSER_TITLE = 'opções genéricas'
ARGPARSER_TITLE = ''
ARGPARSER_DATA = (
    (False, {'args': ('-S', '--save'),
             'kwargs': {'action': 'store_true',
                        'help': 'salva as configurações passadas pela linha de comando no arquivo de configuração'}},
     {'args': ('-V', '--verbose'),
      'kwargs': {'action': 'store_true',
                 'help': 'exibe informações mais detalhadas'}}),
    (True, {'args': ('-l', '--local'),
            'kwargs': {'action': 'store_true',
                       'default': True,
                       'help': 'busca os arquivos de atividades em uma instalação local (default)'}},
           {'args': ('-r', '--remote'),
            'kwargs': {'action': 'store_false',
                       'dest': 'local',
                       'help': 'busca os arquivos de atividades em um servidor remoto'}}),
    (False, {'args': ('-s', '--server'),
             'kwargs': {'default': 'localhost',
                        'help': 'define o endereço do servidor remoto como SERVER (útil quando empregado em conjunto com a opção -r)'}})
)


def initConfigDir():
	if not os.path.exists(CONFIG_DIR):
        	os.makedirs(CONFIG_DIR)


def initConfigParser(ConfigParserClass):
	parser = ConfigParserClass({'local': 'True', 'server address': 'localhost'})
	initConfigDir()
	return parser

def populateArgParser(parser, argParserTitle, argParserData):
        group = parser.add_argument_group(argParserTitle) if argParserTitle else parser

        for grp in argParserData:
                if grp[0]:
                        xgroup = group.add_mutually_exclusive_group()

                        for arg in grp[1:]:
                                xgroup.add_argument(*arg['args'], **arg['kwargs'])
                else:
                        for arg in grp[1:]:
                                group.add_argument(*arg['args'], **arg['kwargs'])
