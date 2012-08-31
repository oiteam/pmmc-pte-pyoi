# -*- coding: utf-8 -*-

import pyoi
from xml.dom.minidom import parse as domparse
from urllib2 import urlopen


def _getPath(suffix, local, server):
        if local:
                prefix = 'file:///opt/pmmc/pte/pai'
        else:
                prefix = '/'.join(('http:/', server, 'pai'))

        return '/'.join((prefix, suffix))


def _parseXML(activity, local, server):
        def nodeText(node):
                text = ''

                for child in node.childNodes:
                        if child.nodeType is child.TEXT_NODE:
                                text += child.data

                if text == '1':
                        return True
                elif text == '0':
                        return False
                elif text.startswith(u'Nível'):
                        return int(text.split(' ')[-1])
                else:
                        return text

        url = _getPath('xml/pai.xml', local, server)
        paiXML = domparse(urlopen(url))
        nodes = paiXML.documentElement
        OITiposPAI = [node for node in nodes.childNodes if node.nodeType == paiXML.ELEMENT_NODE]

        for tipo in OITiposPAI:
                elements = [node for node in tipo.childNodes if node.nodeType == paiXML.ELEMENT_NODE]
                d = dict((str(x.nodeName), nodeText(x)) for x in elements)
                codPAI = d.pop('cod_pai')

                if codPAI == activity:
                        d.pop('arquivo')
                        d['quantidade'] = int(d['quantidade'])

                        return d

        raise Exception('Atividade %s não encontrada no arquivo pai.xml.' % activity.upper())


def _showSummary(activity, local, server, summary=None):
        if not summary:
                summary = _parseXML(activity, local, server)

        print 'Sumário da atividade %s:' % activity
        print '>>> Diretório:         %s' % summary['atividade']
        print '>>> Título:            %s' % summary['titulo']
        print '>>> Descrição:         %s' % summary['descricao']
        print '>>> Disciplina:        %s' % summary['disciplina']
        print '>>> Nível:             %s' % summary['nivel']
        print '>>> Tipo de atividade: %s' % summary['tipo']
        print '>>> Número de páginas: %s' % summary['quantidade']
        print '>>> Proposta por:      %s' % summary['professor']
        print '>>> Desenvolvida por:  %s' % summary['orientador']
        print '>>>     Na escola:     %s' % summary['escola']


def getURL(activity, page=1, local=True, server='localhost', verbose=False):
        if activity == 'MENU':
                return _getPath('pai.html', local, server)
        else:
                summary = _parseXML(activity, local, server)

                if page not in range(1, summary['quantidade'] + 1):
                        raise IndexError('Página %d fora do intervalo de páginas disponíveis para a atividade %s (1 a %d).' % (page, activity, summary['quantidade']))

                if verbose:
                        _showSummary(activity, local, server, summary=summary)

                suffix = '/'.join(('atividades', summary['atividade'], '%s%02d.htm' % (summary['atividade'], page)))
                return _getPath(suffix, local, server)


class CfgParser(pyoi.CfgParser):
	def __init__(self, configfile='pai.conf'):
		pyoi.CfgParser.__init__(self, configfile)

		if not self.has_section('Firefox'):
			self.add_section('Firefox')
			self.set('Firefox', 'profile', 'default')

		if not self.has_section('Chromium'):
			self.add_section('Chromium')
			self.set('Chromium', 'kiosk mode', 'False')


class ArgParser(pyoi.ArgParser):
	def __init__(self):
		pyoi.ArgParser.__init__(self, description='PyPAI - lançador/cliente para o PAI com funcionalidades adicionais')

		########## PAI SPECIFIC OPTIONS ##########
		group = self.add_argument_group('opções específicas para o PAI')
		group.add_argument('-a', '--activity',
                                   default='menu',
                                   help='abre o PAI diretamente na atividade ACTIVITY (exemplo: menu, 3m012 ou 3M012; default: menu)')
                group.add_argument('-p', '--page',
                                   type=int,
                                   default=1,
                                   help='abre a atividade do PAI diretamente na página PAGE; funciona somente em conjunto com a opção -a (default: 1)')

		########## FIREFOX SPECIFIC OPTIONS ##########
		group = self.add_argument_group('opções específicas para o Firefox')
		group.add_argument('-P', '--profile',
                                   default='default',
                                   help='utiliza o perfil do Firefox PROFILE para navegar no PAI')

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
