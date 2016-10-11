#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_cds_lojas                                                    
# Criado em: 05 de Agosto de 2016 as 16:45         
# ----------------------------------------------------------------------

from PyQt4.QtCore import QThread, pyqtSignal

from datetime import datetime

from controllers.connecta import Connecta
from models.cds_lojas import CDsLojasCabecalho, CDsLojasDados, CDsLojasRodape


class TaskCDsLojas(QThread):
    alerta = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TaskCDsLojas, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            self.cx = Connecta()
            self.cx.connectDB()
            result = self.cx.query("select p.PRPCGC, p.PRPDES, p.PRPUF, p.PRPMUN, p.PRPBAI, p.PRPCEP, 'A' as status_loja from PROPRIO p", [])

            cdsLojasCab = CDsLojasCabecalho()
            cdsLojasCab.distribuidor_cod = "11802101000100"
            cdsLojasCab.data_criacao_arquivo = datetime.now()

            arqCDsLoja = 'ACC_CADSITE_' + datetime.now().strftime('%Y%m%d') + '.txt'

            with open(arqCDsLoja, 'a') as f:
                f.write(cdsLojasCab.linha_formatada)
                f.flush()

            for registro in result[1]:
                cdslojasDados = CDsLojasDados()
                cdslojasDados.cd_loja_cod = registro[0]
                cdslojasDados.cd_loja_descricao = registro[1]
                cdslojasDados.cd_loja_uf = registro[2]
                cdslojasDados.cd_loja_cidade = registro[3]
                cdslojasDados.cd_loja_bairro = registro[4]
                cdslojasDados.cd_loja_cep = registro[5]
                cdslojasDados.cd_loja_status = registro[6]

                with open(arqCDsLoja, 'a') as f:
                    f.write(cdslojasDados.linha_formatada)
                    f.flush()

            cdslojasRodape = CDsLojasRodape()
            with open(arqCDsLoja, 'a') as f:
                f.write(cdslojasRodape.linha_formatada)
                f.flush()
        except Exception, e:
            print e