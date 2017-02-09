#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_vendas                                                    
# Criado em: 14 de Agosto de 2016 as 18:29         
# ----------------------------------------------------------------------

from os import path, remove, sep
from PyQt4.QtCore import QThread, pyqtSignal, QDate
from datetime import datetime

from models.vendas import VendasCabecalho, VendasDados, VendasRodape

__app_titulo__ = 'IntegradorACCERA'


class TaskVendas(QThread):
    alerta = pyqtSignal(str, str, str, str)
    tray_msg = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)
    info = pyqtSignal(str)

    def __init__(self, parent=None, data=None):
        super(TaskVendas, self).__init__(parent)
        self.pai = parent
        self.pasta = unicode(self.pai.txt_local_gravar_arquivos.text())
        self.data = data if data is not None else datetime.now()

    def run(self):
        try:
            if self.pai.conectado_bd[0]:
                self.tray_msg.emit('i', __app_titulo__, u'Processando Vendas...')
                self.info.emit(u"Processando Vendas...")

                # Pegando lista de fornecedores da tabela fornecedores do sistema IntegradorACCERA
                ls_fornecedores = ",".join(
                        ["'" + str(codforn['codigo']) + "'" for codforn in self.pai.pegaDadosTabela()])

                dtInicial = QDate(self.data)
                dtInicial = dtInicial.addDays(-(dtInicial.day() - 1))
                dtFinal = QDate(self.data)
                dtFinal = dtFinal.addDays((dtFinal.daysInMonth() - dtFinal.day()))


                # Falta ajustar para pegar a data do mes atual do campo nf.nfsdatsai
                sql_cab = "select (select PROPRIO.PRPCGC from PROPRIO) as cd_loja, min(nf.NFSDATSAI) dt_inicial, " \
                      "max(nf.NFSDATSAI) dt_final from NOTAFISCAL nf " \
                      "where exists( select 1 from ITEM_NOTA_FISCAL inf where inf.NFSCTR = nf.NFSCTR " \
                      "and exists( select 1 from PRODUTO_FORNECEDOR pf where pf.PROCOD = inf.PROCOD " \
                      "and pf.FORCOD in ({forns}) ) ) and nf.NFSDATSAI between '{dtInicial:%m/%d/%Y}' and '{dtFinal:%m/%d/%Y}'".format(
                    forns=ls_fornecedores, dtInicial=dtInicial.toPyDate(), dtFinal=dtFinal.toPyDate()
                )

                # Falta ajustar para pegar a data do mes atual do campo nf.nfsdatsai
                sql_dados = "select (select PROPRIO.PRPCGC from PROPRIO) as cd_loja, f.FORCGC," \
                            "coalesce(pa.PROCODAUX, inf.PROCOD) as procodaux, '' lote_numero, '' lote_data," \
                            "inf.INFQTDEMB, inf.INFVLRTOT, nf.NFSNUM, nf.NFSDATSAI, " \
                            "case when nf.NFSTIP = 'NFV' and nf.CFOCOD in ('51020', '61020') then 'V' when nf.NFSTIP = 'NFV' and nf.CFOCOD in ('59100', '69100') then 'B' when nf.NFSTIP = 'CAN' then 'C' end transacao_tip, " \
                            "nf.CFOCOD, case when char_length(nf.NFSCLICPFCGC) < 12 then '1' else '2' end pdv_tipo, " \
                            "nf.NFSCLICPFCGC as pdv_indentif, nf.NFSCLIDES as pdv_descricao, nf.NFSCLICEP as pdv_cep, " \
                            "'' pdv_classificacao, (select PROPRIO.PRPCGC || ' - ' || PROPRIO.PRPDES from PROPRIO) vendedor, " \
                             "'' livre1, '' livre2  from ITEM_NOTA_FISCAL inf " \
                            "inner join PRODUTO_FORNECEDOR pf on (pf.PROCOD = inf.PROCOD and pf.FORCOD in ({forns}) " \
                             "and exists( select 1 from ITEVDA itv where itv.PROCOD = pf.PROCOD " \
                            "and itv.TRNDAT >= '01/01/2014' )) " \
                            "inner join NOTAFISCAL nf on (nf.NFSCTR = inf.NFSCTR and nf.NFSTIP in ('NFV', 'CAN') " \
                            "and nf.NFSDATSAI between '{dtInicial:%m/%d/%Y}' and '{dtFinal:%m/%d/%Y}') " \
                            "left outer join FORNECEDOR f on (f.FORCOD = pf.FORCOD) " \
                            "left outer join PRODUTOAUX pa on (pa.PROCOD = pf.PROCOD)".format(
                        forns=ls_fornecedores, dtInicial=dtInicial.toPyDate(), dtFinal=dtFinal.toPyDate()
                )

                result_cab = self.pai.cx.query(sql_cab, [])
                result = self.pai.cx.query(sql_dados, [])

                if result_cab[0] and result[0]:
                    dados_cab = result_cab[1].fetchall()
                    dados = result[1].fetchall()

                    self.progress_max.emit(len(dados_cab) + len(dados))
                    contador = 0
                else:
                    print 'SQL: ', result[1]
                    print result_cab[1]
                    self.info.emit(u"Erro interno!\nErro ao executar Script SQL de Vendas!")
                    self.tray_msg.emit('i', __app_titulo__, u'Erro ao executar Script SQL de Vendas!')
                    if self.pai.isVisible():
                        self.alerta.emit('i', __app_titulo__, 'Erro ao execurar Script SQL de Vendas', "")
                    self.sleep(3)
                    self.terminate()

                if len(dados) > 0:

                    arqVendas = self.pasta + sep + u'ACC_SELLOUT_' + self.data.strftime('%Y%m%d') + u'.txt'

                    if path.exists(arqVendas):
                        remove(arqVendas)

                    cab_vendas = VendasCabecalho()
                    rod_vendas = VendasRodape()

                    for registro in dados_cab:
                        contador += 1

                        print registro

                        print "Distribuidor: ", registro[0]
                        cab_vendas.distribuidor_cod = registro[0]
                        print "Data Inicial: ", registro[1]
                        cab_vendas.data_inicial = registro[1]
                        print "Data Final: ", registro[2]
                        cab_vendas.data_final = registro[2]
                        with open(arqVendas, 'a') as f:
                            f.write(cab_vendas.linha_formatada)
                            f.flush()

                        self.progress_value.emit(contador)

                    # print 'Vai percorrer os dados'
                    for registro in dados:
                        contador += 1

                        if registro[9] in ('B', 'C'):

                            # Escrevendo Origem do cancelamento ou bonificacao
                            orig_registro = []
                            orig_registro.extend(registro)
                            orig_registro[9] = u'V'
                            orig_modelo = self.popula_modelo(orig_registro)
                            self.escreve(arqVendas, orig_modelo)

                            # Escrevendo Cancelamento ou bonificacao
                            modelo = self.popula_modelo(registro)
                            self.escreve(arqVendas, modelo)
                        else:
                            modelo = self.popula_modelo(registro)
                            self.escreve(arqVendas, modelo)
                        self.progress_value.emit(contador)

                    with open(arqVendas, 'a') as f:
                        f.write(rod_vendas.linha_formatada)
                        f.flush()

                    self.info.emit(u"Vendas finalizado!")
                    self.tray_msg.emit('i', __app_titulo__, u'Vendas Finalizado')
                    if self.pai.isVisible():
                        self.alerta.emit('i', __app_titulo__, 'Vendas Finalizado', "")
                else:
                    self.alerta.emit('i', 'IntegradorACCERA', 'Sem vendas no periodo!', '')
            else:
                self.info.emit(u"Você não está conectado ao banco de dados!")
                self.tray_msg.emit('i', __app_titulo__ + " - Vendas", u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__ + ' - Vendas', u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!', "")

            self.sleep(3)
            self.info.emit("")
            self.progress_value.emit(0)
        except Exception, e:
            print e
            self.info.emit(u"Erro no processo das Vendas!")
            self.progress_value.emit(0)
            self.tray_msg.emit('i', __app_titulo__, u'Erro Vendas!\nErro: {}'.format(e))
            if self.pai.isVisible():
                self.alerta.emit('c', __app_titulo__, 'Vendas Error', unicode(e))
            self.sleep(3)
            self.terminate()

    def popula_modelo(self, registro):
        dados_vendas = VendasDados()
        # print '1'
        dados_vendas.cd_loja_cod = registro[0]
        # print '2'
        dados_vendas.fornecedor_cod = registro[1]
        # print '3'
        dados_vendas.produto_barras = registro[2]
        # print '4'
        dados_vendas.lote_numero = registro[3]
        # print '5'
        dados_vendas.lote_data_validade = registro[4]
        # print '6'
        dados_vendas.saida_quantidade = registro[5]
        # print '7'
        dados_vendas.valor_unitario = registro[6]
        # print '8'
        dados_vendas.transacao_identificador = registro[7]
        # print '9'
        dados_vendas.transacao_data = registro[8]
        # print '10'
        dados_vendas.transacao_tipo = registro[9]
        # print '11'
        dados_vendas.cfop = registro[10]
        # print '12'
        dados_vendas.pdv_identificador_tipo = registro[11]
        # print '13'
        dados_vendas.pdv_identificador = registro[12]
        # print '14'
        dados_vendas.pdv_descricao = registro[13]
        # print '15'
        dados_vendas.pdv_cep = registro[14]
        # print '16'
        dados_vendas.pdv_classificacao = registro[15]
        # print '17'
        dados_vendas.vendedor_nome = registro[16]
        # print '18'
        dados_vendas.campo_livre1 = registro[17]
        # print '19'
        dados_vendas.campo_livre2 = registro[18]

        return dados_vendas

    def escreve(self, arqVendas, dados_vendas):
        with open(arqVendas, 'a') as f:
            f.write(dados_vendas.linha_formatada)
            f.flush()
