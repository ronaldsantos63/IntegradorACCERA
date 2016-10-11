#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_vendas
# Criado em: 14 de Agosto de 2016 as 18:29
# ----------------------------------------------------------------------
from datetime import datetime
from PyQt4.QtCore import QThread, pyqtSignal

from controllers.connecta import Connecta
from models.notas_fiscais_recebidas import NFRCabecalho,NFRDados,NFRRodape


class TaskNFR(QThread):
    alerta = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TaskNFR, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            self.cx = Connecta()
            self.cx.connectDB()

            arqNotaFiscal = 'ACC_NFS_' + datetime.now().strftime('%Y%m%d') + '.txt'

            result = self.cx.query("select (select p.PRPCGC from proprio p) cod_distribuidor, min(e.entdat) data_inicial, max(e.entdat) data_final from ENTRADA e where e.entdat between '07/01/2016' and '07/31/2016' and e.forcod in ('0017','0020') ", [])

            if result[0]:
                cab_nota = NFRCabecalho()
                for registro in result[1]:
                    cab_nota.distribuidor_cod = registro[0]
                    cab_nota.data_inicial = registro[1]
                    cab_nota.data_final = registro[2]

                    with open(arqNotaFiscal,'a') as f:
                        f.write(cab_nota.linha_formatada)
                        f.flush()
            else:
                print result[1]
                self.terminate()

            result = self.cx.query("select f.FORCGC, e.ENTDOC, 'E' as acao, e.ENTVLRTOT, (select sum(ITEM_ENTRADA.ITEQTDEMB) from item_entrada where item_entrada.entdoc = e.entdoc and item_entrada.ENTSER = e.ENTSER and item_entrada.FORCOD = e.forcod and item_entrada.ENTTNF = e.ENTTNF) quantidade, e.ENTDATEMI,e.ENTDAT from ENTRADA e left outer join fornecedor f on(e.forcod = f.forcod ) where e.entdat between '07/01/2016' and '07/31/2016' and e.forcod in ('0017','0020') ",[])
            if result[0]:
                for registro in result[1]:
                    dados_nota = NFRDados()
                    dados_nota.fornecedor_cod = registro[0]
                    dados_nota.nf_numero = registro[1]
                    dados_nota.nf_acao = registro[2]
                    dados_nota.nf_valor = registro[3]
                    dados_nota.nf_quantidade = registro[4]
                    dados_nota.nf_acao_data = registro[5]
                    dados_nota.nf_data_entrada = registro[6]

                    with open(arqNotaFiscal,'a') as f:
                        f.write(dados_nota.linha_formatada)
                        f.flush()

            else:
                print result[1]

            rod_nota = NFRRodape()

            with open(arqNotaFiscal,'a') as f:
                f.write(rod_nota.linha_formatada)
                f.flush()
        except Exception, e:
            print e