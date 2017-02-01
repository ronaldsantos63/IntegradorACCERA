#!/usr/bin/env python
# encoding: utf-8
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Autor: ronald
# Projeto: IntegradorACCERA
# Modulo: tray
# Criado em: 20 de Outubro de 2016 as 18:10
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt4 import QtGui, QtCore


class AnimatedSystemTrayIcon(QtGui.QSystemTrayIcon):
    def UpdateIcon(self):
        icon = QtGui.QIcon()
        icon.addPixmap(self.iconMovie.currentPixmap())
        self.setIcon(icon)

    def __init__(self, movie, parent=None):
        super(AnimatedSystemTrayIcon, self).__init__(parent)
        self.pai = parent

        self.iconDefault = QtGui.QIcon(":/logo/images/logo/logo.jpg")

        self.setIcon(self.iconDefault)

        menu = QtGui.QMenu(parent)
        self.AbrirFormPrinAction = menu.addAction(QtGui.QIcon(":/logo/images/logo/logo.jpg"), "Abrir")
        # self.IniciarMonitAction = menu.addAction(QtGui.QIcon(":/png/images/png/play.png"), "Iniciar Monitoramento")
        # self.PararMonitAction = menu.addAction(QtGui.QIcon(":/png/images/png/Stop.png"), "Parar Monitoramento")
        # self.PararMonitAction.setEnabled(False)
        # self.ExportarAction = menu.addAction(QtGui.QIcon(":/png/images/png/Download.png"), u"Exportar Alterações")
        # self.configAction = menu.addAction(QtGui.QIcon(":/png/images/png/configure.png"), u"Configuração")
        exitAction = menu.addAction(QtGui.QIcon(":/png/images/png/Exit.png"), "Sair")
        self.setContextMenu(menu)

        self.iconMovie = movie

        # Conexoes
        self.connect(self.AbrirFormPrinAction, QtCore.SIGNAL("triggered()"), self.abrirFormPrinc)
        # self.connect(self.IniciarMonitAction, QtCore.SIGNAL("triggered()"), self.pai.iniciar_processo)
        # self.connect(self.PararMonitAction, QtCore.SIGNAL("triggered()"), self.pai.iniciar_processo)
        # self.connect(self.ExportarAction, QtCore.SIGNAL("triggered()"), self.pai.iniciar_processo)
        # self.connect(self.configAction, QtCore.SIGNAL("triggered()"), self.pai.show_configuracao)
        self.connect(exitAction, QtCore.SIGNAL("triggered()"), self.pai.close)
        self.iconMovie.frameChanged.connect(self.UpdateIcon)

    def abrirFormPrinc(self):
        if self.pai.isVisible:
            self.pai.showNormal()
            self.pai.activateWindow()
            # self.hide()
        else:
            self.pai.show()

    def processando(self):
        self.iconMovie.start()

    def processo_finalizado(self):
        self.iconMovie.stop()
        self.setIcon(self.iconDefault)
