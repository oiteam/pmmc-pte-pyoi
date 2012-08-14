# -*- coding: utf-8 -*-

from xml.dom.minidom import parse as domparse
from urllib2 import urlopen
from pmmc.pte import CONFIG_DIR

CONFIG_FILE = CONFIG_DIR + '/pai.conf'
ARGPARSER_TITLE = 'opções específicas para o PAI'
ARGPARSER_DATA = (
    (False, {'args': ('-a', '--activity'),
             'kwargs': {'default': 'menu',
                        'help': 'abre o PAI diretamente na atividade ACTIVITY (exemplo: menu, 3m012 ou 3M012; default: menu)'}},
            {'args': ('-p', '--page'),
             'kwargs': {'type': int,
                        'default': 1,
                        'help': 'abre a atividade do PAI diretamente na página PAGE; funciona somente em conjunto com a opção -a (default: 1)'}}),
)


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

        print 'Sumário da atividade', activity, ':'
        print '>>> Diretório:        ', summary['atividade']
        print '>>> Título:           ', summary['titulo']
        print '>>> Descrição:        ', summary['descricao']
        print '>>> Disciplina:       ', summary['disciplina']
        print '>>> Nível:            ', summary['nivel']
        print '>>> Tipo de atividade:', summary['tipo']
        print '>>> Número de páginas:', summary['quantidade']
        print '>>> Proposta por:     ', summary['professor']
        print '>>> Desenvolvida por: ', summary['orientador']
        print '>>>     Na escola:    ', summary['escola']


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
