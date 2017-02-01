#!/usr/bin/env python
# -*- coding: utf-8 -*-
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Autor: ronald
# Projeto: IntegradorACCERA
# Modulo: thread_principal
# Criado em: 28 de Outubro de 2016 as 11:51
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


from PyQt4.QtCore import QThread, Qt, QTime, pyqtSignal

from tasks.task_produtos import TaskProdutos
from tasks.task_cds_lojas import TaskCDsLojas
from tasks.task_clientes import TaskClientes
from tasks.task_estoque import TaskEstoque
from tasks.task_notas_fiscais_recebidas import TaskNFR
from tasks.task_vendas import TaskVendas


class TaskMain(QThread):
    gerar = pyqtSignal(object)

    def __init__(self, parent=None, mutex=None, cond=None):
        super(TaskMain, self).__init__(parent)
        self.pai = parent
        self.__parar = False
        self.mutex = mutex
        self.cond = cond

    def run(self):
        while not self.__parar:
            # print 'Esta no loop'
            if self.__parar:
                # print 'Saindo do loop'
                break
            if self.pai.dte_hora.time() == QTime.currentTime():
                # print 'Esta na hora ;)'
                self.mutex.lock()
                try:
                    self.gerar.emit(None)
                    self.cond.wait(self.mutex)
                finally:
                    self.mutex.unlock()

    def parar(self):
        self.__parar = True
