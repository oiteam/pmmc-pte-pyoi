#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
from argparse import ArgumentParser
from pmmc.pte import pai, initConfigParser, populateArgParser, ARGPARSER_TITLE, ARGPARSER_DATA
from pmmc.pte.pai.chromium import loadConfig, saveConfig, setArgParserDefaults, launch

cfgparser = initConfigParser(SafeConfigParser)
loadConfig(cfgparser)

parser = ArgumentParser(description='PyPAI - lançador/cliente para o PAI com funcionalidades adicionais')
populateArgParser(parser, ARGPARSER_TITLE, ARGPARSER_DATA)
populateArgParser(parser, pai.ARGPARSER_TITLE, pai.ARGPARSER_DATA)
populateArgParser(parser, pai.chromium.ARGPARSER_TITLE, pai.chromium.ARGPARSER_DATA)

# Hacks argparse's non-localizable messages
parser._action_groups[1].title = 'opções genéricas'
parser._actions[0].help = 'exibe esta mensagem de ajuda e sai'

setArgParserDefaults(parser, cfgparser)
args = parser.parse_args()

if args.save:
	saveConfig(cfgparser, args)

launch(args.activity, args.page, args.kiosk, args.local, args.server, args.verbose, browser='google-chrome')
