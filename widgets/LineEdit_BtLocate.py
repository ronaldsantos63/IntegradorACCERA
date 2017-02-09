#!/usr/bin/env python
#encoding: utf-8
__author__ = 'ronald'


from PyQt4.QtGui import QLineEdit, QToolButton, QIcon, QHBoxLayout, QFileDialog, QApplication, QMessageBox
from PyQt4.QtCore import Qt, QDir, QFile

import resources_rc


class LineEditBtLocate(QLineEdit):
    '''
    Classe Personalizada do QLineEdit com botao para localizar pastas e ou arquivos
    '''
    def __init__(self, parent=None, so_pasta=False, filtro=None):
        '''
        Contrutor da classe personalizada
        @param parent: Classe Principal
        @param so_pasta: True - Se sera exibido somente pastas | False - se for exibidos arquivos e pastas
        @param filtro: Filtro usado quando o @so_pasta for verdadeiro\nEx: "All(*);;Imagem (*.jpeg;*.png);;Audio (*.wav)"
        '''
        QLineEdit.__init__(self, parent)

        self.so_pasta = so_pasta
        self.filtro = filtro

        self.btLocate = QToolButton(self)
        self.btLocate.setCursor(Qt.PointingHandCursor)
        self.btLocate.setFocusPolicy(Qt.NoFocus)
        if self.so_pasta:
            self.btLocate.setIcon(QIcon(":/images/ico_widgets/folder.ico"))
        else:
            self.btLocate.setIcon(QIcon(":/images/ico_widgets/view.ico"))
        self.btLocate.setStyleSheet("background: transparent; border: none;")

        layout = QHBoxLayout(self)
        layout.addWidget(self.btLocate, 0, Qt.AlignRight)

        layout.setSpacing(0)
        layout.setMargin(5)

        self.btLocate.setToolTip(QApplication.translate("None", "Localizar", None, QApplication.UnicodeUTF8))
        self.btLocate.clicked.connect(self.abrir_arquivo)

    def setFiltro(self, filtro):
        self.filtro = filtro

    def setSoPasta(self, value):
        self.so_pasta = value
        if self.so_pasta:
            self.btLocate.setIcon(QIcon(":/images/ico_widgets/folder.ico"))
        else:
            self.btLocate.setIcon(QIcon(":/images/ico_widgets/view.ico"))

    def showButtonLocate(self, bool=True):
        self.btLocate.setVisible(bool)

    def abrir_arquivo(self):
        if self.so_pasta:
            pasta = QFileDialog.getExistingDirectory(self, "Localizar", ".")
            #print("arquivo: {0}".format(pasta))
            #print("Tipo: {0}".format(type(pasta)))
            if QDir(pasta).exists():
                self.setText(pasta)
            else:
                QMessageBox.critical(self, "Alerta", u"O arquivo selecionado não é valido!")
        else:
            arquivo = QFileDialog.getOpenFileName(self, "Localizar", ".", self.filtro if self.filtro else "")
            if QFile(arquivo).exists():
                self.setText(arquivo)
            else:
                QMessageBox.critical(self, "Alerta", u"O arquivo selecionado não é valido!")