#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_produtos                                                    
# Criado em: 05 de Agosto de 2016 as 11:31         
# ----------------------------------------------------------------------

from os import path, remove
from PyQt4.QtCore import QThread, pyqtSignal
from datetime import datetime

from models.produtos import ProdutosCabecalho, ProdutosDados, ProdutosRodape

__app_titulo__ = 'IntegradorACCERA'


class TaskProdutos(QThread):
    alerta = pyqtSignal(str, str, str, str)
    tray_msg = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)
    info = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TaskProdutos, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            print 'verificando se esta conectado no banco de dados'
            if self.pai.conectado_bd[0]:
                print 'Esta conectado! Iniciando processo produto'
                self.tray_msg.emit('i', __app_titulo__, u'Processando Produtos...')
                self.info.emit(u"Processando Produtos...")

                # print 'Pegando lista de fornecedores da QTable tb_fornecedores...'
                # Pegando lista de fornecedores da tabela fornecedores do sistema IntegradorACCERA
                ls_fornecedores = ",".join(
                        ["'" + str(codforn['codigo']) + "'" for codforn in self.pai.pegaDadosTabela()])

                # print 'codforn: ', ls_fornecedores

                # print 'Lista retornada com sucesso!'

                sql = "select f.FORCGC, f.FORDES, p.PROCOD, p.PRODES, coalesce(pa.PROCODAUX, " \
                      "p.PROCOD) as procodaux, p.PROUNID as unidade_venda, " \
                      "case when coalesce(p.PROITEEMBVDA, 1.0) = 0.0 then 1.0 else p.PROITEEMBVDA end qtd_item_venda, " \
                      "p.PROFORLIN, p.PRODATCADINC from produto p " \
                      "left outer join PRODUTO_FORNECEDOR pf on (pf.PROCOD = p.PROCOD and pf.FORCOD in ({forns})) " \
                      "left outer join FORNECEDOR f on (pf.FORCOD = f.FORCOD and pf.FORCOD in ({forns})) " \
                      "left outer join PRODUTOAUX pa on (pa.PROCOD = p.PROCOD) " \
                      "where exists(select 1 from ITEVDA where ITEVDA.PROCOD = p.PROCOD " \
                      "and pf.FORCOD in ({forns}) and ITEVDA.TRNDAT >= '01/01/2014')".format(forns=ls_fornecedores)

                result = self.pai.cx.query(sql, [])

                arqProd = 'ACC_CADPROD_' + datetime.now().strftime('%Y%m%d') + '.txt'

                if path.exists(arqProd):
                    remove(arqProd)

                produtoCab = ProdutosCabecalho()
                produtoRodape = ProdutosRodape()

                # print 'cod_distribuidor: ', self.pai.txt_cod_distrbuidor.text()
                # print 'Tipo: ', type(self.pai.txt_cod_distrbuidor.text())
                produtoCab.cod_distribuidor = str(self.pai.txt_cod_distrbuidor.text())
                produtoCab.data_criacao_arquivo = datetime.now()

                with open(arqProd, 'a') as f:
                    f.write(produtoCab.linha_formatada)
                    f.flush()

                if result[0]:
                    dados = result[1].fetchall()
                    self.progress_max.emit(len(dados))
                    contador = 0

                    for registro in dados:
                        contador += 1

                        produtoDados = ProdutosDados()
                        produtoDados.fornecedor_cod = registro[0]
                        # print 'codigo_fornecedor: ', registro[0]
                        produtoDados.fornecedor_descricao = registro[1]
                        produtoDados.produto_cod = registro[2]
                        # print 'codigo produto: ', registro[2]
                        produtoDados.produto_descricao = registro[3]
                        produtoDados.cod_barras = registro[4]
                        # print 'codigo de barras: ', registro[4]
                        produtoDados.tipo_embalagem_venda = registro[5]
                        produtoDados.volume_embalagem_venda = registro[6]
                        produtoDados.status_produto = registro[7]
                        produtoDados.data_cadastro = registro[8]

                        with open(arqProd, 'a') as f:
                            f.write(produtoDados.linha_formatada)
                            f.flush()

                        self.progress_value.emit(contador)

                    with open(arqProd, 'a') as f:
                        f.write(produtoRodape.linha_formatada)
                        f.flush()

                    self.info.emit(u"Processo dos Produtos finalizado!")
                    if not self.pai.isVisible():
                        self.tray_msg.emit('i', u"IntegradorACCERA", u"Processo dos Produtos finalizado!")
                    else:
                        self.alerta.emit('i', 'IntegradorACCERA', u"Processo dos PRODUTOS finalizado!", "")
                else:
                    self.info.emit(result[1])
            else:
                self.info.emit(u"Você não está conectado ao banco de dados")
                self.tray_msg.emit('i', __app_titulo__ + " - Produtos", u'Você não está conectado ao banco de dados!\n'
                                                                        u'Por favor revise suas configurações de conexão!')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__ + ' - Produtos',
                                     u'Você não está conectado ao banco de dados!\n'
                                     u'Por favor revise suas configurações de conexão!', "")
            self.sleep(3)
            self.info.emit("")
            self.progress_value.emit(0)
        except Exception, e:
            print "Erro ao processar produtos"
            print '-' * 30
            print e
            print '-' * 30
            self.info.emit(u"Erro no processso dos Produtos!")
            self.progress_value.emit(0)
            if not self.pai.isVisible():
                self.tray_msg.emit('c', u"IntegradorACCERA", u"Erro ao gerar produtos!\nErro: {}".format(e.message))
            else:
                self.alerta.emit('c', 'IntegradorACCERA', "Erro ao gerar produtos!\nErro: {}".format(e.message),
                                 unicode(e))
            self.sleep(3)
            self.terminate()
