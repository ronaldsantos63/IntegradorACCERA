#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_vendas
# Criado em: 14 de Agosto de 2016 as 18:29
# ----------------------------------------------------------------------

from os import path, remove
from datetime import datetime
from PyQt4.QtCore import QThread, pyqtSignal

from models.notas_fiscais_recebidas import NFRCabecalho,NFRDados,NFRRodape

__app_titulo__ = 'IntegradorACCERA'


class TaskNFR(QThread):
    alerta = pyqtSignal(str, str, str, str)
    tray_msg = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)
    info = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TaskNFR, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            if self.pai.conectado_bd[0]:
                self.tray_msg.emit('i', __app_titulo__, u'Processando Notas Fiscais de Entrada...')
                self.info.emit(u"Processando Notas Fiscais de Entrada...")

                arqNotaFiscal = 'ACC_NFS_' + datetime.now().strftime('%Y%m%d') + '.txt'

                if path.exists(arqNotaFiscal):
                    remove(arqNotaFiscal)

                # Pegando lista de fornecedores da tabela fornecedores do sistema IntegradorACCERA
                ls_fornecedores = ",".join(
                        ["'" + str(codforn['codigo']) + "'" for codforn in self.pai.pegaDadosTabela()])

                # Falta ajustar para pegar a data do mes atual no campo e.entdat
                sql_cab = "select (select p.PRPCGC from proprio p) cod_distribuidor, min(e.entdat) data_inicial, " \
                      "max(e.entdat) data_final from ENTRADA e where e.entdat between '07/01/2016' and '07/31/2016' and " \
                      "e.forcod in ({forns}) ".format(forns=ls_fornecedores)

                # Falta ajustar para pegar a data do mes atual no campo e.entdat
                sql_dados = "select f.FORCGC, e.ENTDOC, 'E' as acao, e.ENTVLRTOT, " \
                            "(select sum(ITEM_ENTRADA.ITEQTDEMB) from item_entrada where item_entrada.entdoc = e.entdoc " \
                            "and item_entrada.ENTSER = e.ENTSER and item_entrada.FORCOD = e.forcod " \
                            "and item_entrada.ENTTNF = e.ENTTNF) quantidade, e.ENTDATEMI,e.ENTDAT from ENTRADA e " \
                            "left outer join fornecedor f on(e.forcod = f.forcod ) " \
                            "where e.entdat between '07/01/2016' and '07/31/2016' and e.forcod in ({forns})".format(
                        forns=ls_fornecedores
                )

                result_cab = self.pai.cx.query(sql_cab, [])
                result = self.pai.cx.query(sql_dados, [])

                contador = 0

                if result_cab[0] and result[0]:
                    dados_cab = result_cab[1].fetchall()
                    dados = result[1].fetchall()
                    self.progress_max.emit(len(dados_cab) + len(dados))
                else:
                    self.tray_msg.emit('c', __app_titulo__, u'Erro Interno!\nErro ao executar Script do banco de dados!')
                    if self.pai.isVisible():
                        self.alerta.emit('a', __app_titulo__, u'Erro Interno!\nErro ao executar Script do banco de dados!', "")
                    self.sleep(3)
                    self.terminate()

                for registro in dados_cab:
                    contador += 1

                    cab_nota = NFRCabecalho()
                    cab_nota.distribuidor_cod = registro[0]
                    cab_nota.data_inicial = registro[1]
                    cab_nota.data_final = registro[2]

                    with open(arqNotaFiscal,'a') as f:
                        f.write(cab_nota.linha_formatada)
                        f.flush()

                    self.progress_value.emit(contador)

                for registro in dados:
                    contador += 1

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
                    self.progress_value.emit(contador)

                rod_nota = NFRRodape()

                with open(arqNotaFiscal, 'a') as f:
                    f.write(rod_nota.linha_formatada)
                    f.flush()

                self.tray_msg.emit('i', __app_titulo__, u'Notas Fiscais de Entrada Finalizado')
                self.info.emit(u"Notas Fiscais de Entrada Finalizado!")
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__, 'Notas Fiscais de Entrada Finalizado', "")
            else:
                self.info.emit(u"Você não está conectado ao banco de dados!")
                self.tray_msg.emit('i', __app_titulo__ + " - NFe Entrada", u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__ + ' - NFe Entrada', u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!', "")
            self.sleep(3)
            self.info.emit("")
            self.progress_value.emit(0)
        except Exception, e:
            print e
            self.info.emit(u"Erro ao processar Notas Fiscais de Entrada!")
            self.progress_value.emit(0)
            self.tray_msg.emit('i', __app_titulo__, u'Erro Notas Fiscais de Entrada!\nErro: {}'.format(e))
            if self.pai.isVisible():
                self.alerta.emit('c', __app_titulo__, 'Notas Fiscais de Entrada Error', unicode(e))
            self.sleep(3)
            self.terminate()
