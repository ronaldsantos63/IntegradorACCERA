#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_estoque                                                    
# Criado em: 07 de Agosto de 2016 as 18:49         
# ----------------------------------------------------------------------

from os import path, remove, sep
from PyQt4.QtCore import QThread, pyqtSignal
from datetime import datetime

from models.estoque import EstoqueCabecalho, EstoqueDados, EstoqueRodape

__app_titulo__ = 'IntegradorACCERA'


class TaskEstoque(QThread):
    alerta = pyqtSignal(str, str, str, str)
    tray_msg = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)
    info = pyqtSignal(str)

    def __init__(self, parent=None, data=None):
        super(TaskEstoque, self).__init__(parent)
        self.pai = parent
        self.pasta = unicode(self.pai.txt_local_gravar_arquivos.text())
        self.data = data if data is not None else datetime.now()

    def run(self):
        try:
            if self.pai.conectado_bd[0]:
                self.tray_msg.emit('i', __app_titulo__, u'Processando Estoque...')
                self.info.emit(u"Processando Estoque...")

                # Pegando lista de fornecedores da tabela fornecedores do sistema IntegradorACCERA
                ls_fornecedores = ",".join(
                        ["'" + str(codforn['codigo']) + "'" for codforn in self.pai.pegaDadosTabela()])

                sql = "select (select PROPRIO.PRPCGC from PROPRIO) as cd_loja, f.FORCGC, " \
                      "coalesce(pa.PROCODAUX, e.procod) as barras, '' numero_lote, '' data_validade_lote, " \
                      "case when coalesce(e.ESTATUSDO, 0) < 0 then 0 else e.ESTATUSDO end as quantidade_estoque, " \
                      "case when coalesce(e.ESTATUSDO, 0) <= 0 then 'H' else 'H' end as tipo_estoque, " \
                      "(select current_timestamp from RDB$DATABASE) as data_estoque from estoque e " \
                      "left outer join produto_fornecedor pf on (pf.PROCOD = e.PROCOD and pf.FORCOD in ({forns})) " \
                      "left outer join FORNECEDOR f on (f.FORCOD = pf.FORCOD and f.FORCOD in ({forns})) " \
                      "left outer join PRODUTOAUX pa on (pa.PROCOD = e.PROCOD) where e.DATULTSAI >= '01/01/2014' and " \
                      "exists ( select 1 from PRODUTO_FORNECEDOR where e.PROCOD = PRODUTO_FORNECEDOR.PROCOD and " \
                      "PRODUTO_FORNECEDOR.FORCOD in ({forns}) )".format(forns=ls_fornecedores)

                result = self.pai.cx.query(sql, [])

                cab_estoque = EstoqueCabecalho()
                cab_estoque.distribuidor_cod = str(self.pai.txt_cod_distrbuidor.text())
                cab_estoque.data_inicial = self.data
                cab_estoque.data_final = self.data

                arq_estoque = self.pasta + sep + u'ACC_POSESTQ_' + self.data.strftime('%Y%m%d') + u'.txt'

                if path.exists(arq_estoque):
                    remove(arq_estoque)

                with open(arq_estoque, 'a') as f:
                    f.write(cab_estoque.linha_formatada)
                    f.flush()

                if result[0]:
                    dados = result[1].fetchall()
                    self.progress_max.emit(len(dados))
                    contador = 0

                    for registro in dados:
                        contador += 1

                        dados_estoque = EstoqueDados()
                        dados_estoque.cd_loja_cod = registro[0]
                        dados_estoque.fornecedor_cod = registro[1]
                        dados_estoque.produto_barras = registro[2]
                        dados_estoque.lote_numero = registro[3]
                        dados_estoque.lote_data_validade = registro[4]
                        dados_estoque.estoque_quantidade = registro[5]
                        dados_estoque.estoque_tipo = registro[6]
                        dados_estoque.estoque_data = registro[7]

                        with open(arq_estoque, 'a') as f:
                            f.write(dados_estoque.linha_formatada)
                            f.flush()

                        self.progress_value.emit(contador)

                    rodape_estoque = EstoqueRodape()
                    with open(arq_estoque, 'a') as f:
                        f.write(rodape_estoque.linha_formatada)
                        f.flush()

                    self.tray_msg.emit('i', __app_titulo__, u'Estoque Finalizado')
                    self.info.emit(u"Estoque Finalizado!")
                    if self.pai.isVisible():
                        self.alerta.emit('i', __app_titulo__, 'Estoque Finalizado', "")
                else:
                    self.info.emit(u"Erro ao executar script para retornar o Estoque!")
            else:
                self.info.emit(u"Você não está conectado ao banco de dados")
                self.tray_msg.emit('i', __app_titulo__ + " - Estoque", u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__ + ' - Estoque', u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!', "")
            self.sleep(3)
            self.info.emit("")
            self.progress_value.emit(0)
        except Exception, e:
            print e
            self.info.emit(u"Erro no processo Estoque!")
            self.progress_value.emit(0)
            self.tray_msg.emit('i', __app_titulo__, u'Erro Estoque!\nErro: {}'.format(e))
            if self.pai.isVisible():
                self.alerta.emit('c', __app_titulo__, 'Estoque Error', unicode(e))
            self.sleep(3)
            self.terminate()
