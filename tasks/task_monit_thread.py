#!/usr/bin/env python
# encoding utf-8
# ----------------------------------------------------------------------
# Modulo: task_monit_thread
# Descricao: Este modulo sera o responsavel por monitar as threads de irao gerar os arquivos
# Autor: ronald
# Criado em: 08 de dez de 2016
# ----------------------------------------------------------------------

from PyQt4.QtCore import QThread, pyqtSignal


class TaskMonitThread(QThread):
    def __init__(self, parent=None, pool_thread=[]):
        super(TaskMonitThread, self).__init__(parent)
        self.pai = parent
        self.pool_thread = pool_thread
        self.__parar = False

    def run(self):
        while not self.__parar and not self.pool_thread:
            for idx, thread in enumerate(self.pool_thread):
                if thread.isFinished():
                    self.pool_thread.pop(idx)
