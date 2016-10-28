#!/usr/bin/env python
# -*- coding: utf-8 -*-
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Autor: ronald
# Projeto: IntegradorACCERA
# Modulo: thread_principal
# Criado em: 28 de Outubro de 2016 as 11:51
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


from PyQt4.QtCore import QThread, Qt, QTime


class TaskMain(QThread):
    def __init__(self, parent=None):
        super(TaskMain, self).__init__(parent)
        self.pai = parent

    def run(self):
        while True:
            if self.pai.dte_hora.time().toString(Qt.TextDate) == QTime.currentTime().toString():
                pass
