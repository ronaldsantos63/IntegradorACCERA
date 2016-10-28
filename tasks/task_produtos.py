#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_produtos                                                    
# Criado em: 05 de Agosto de 2016 as 11:31         
# ----------------------------------------------------------------------

from PyQt4.QtCore import QThread, pyqtSignal

from datetime import datetime

from controllers.connecta import Connecta
from models.produtos import ProdutosCabecalho, ProdutosDados, ProdutosRodape


class TaskProdutos(QThread):
    alerta = pyqtSignal(str, str, str, str)
    tray_msg = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TaskProdutos, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            self.cx = Connecta()
            self.cx.connectDB()
            result = self.cx.query("select f.FORCGC, f.FORDES, pf.PRFREFFOR, p.PRODES, coalesce(pa.PROCODAUX, pf.PRFREFFOR) as procodaux, p.PROUNID as unidade_venda, case when coalesce(p.PROITEEMBVDA, 1.0) = 0.0 then 1.0 else p.PROITEEMBVDA end qtd_item_venda, p.PROFORLIN, p.PRODATCADINC from produto p left outer join PRODUTO_FORNECEDOR pf on (pf.PROCOD = p.PROCOD and pf.FORCOD in ('0017', '0020')) left outer join FORNECEDOR f on (pf.FORCOD = f.FORCOD and pf.FORCOD in ('0017', '0020')) left outer join PRODUTOAUX pa on (pa.PROCOD = p.PROCOD) where exists(select 1 from ITEVDA where ITEVDA.PROCOD = p.PROCOD and pf.FORCOD in ('0017', '0020') and ITEVDA.TRNDAT >= '01/01/2014')", [])

            arqProd = 'ACC_CADPROD_' + datetime.now().strftime('%Y%m%d') + '.txt'

            produtoCab = ProdutosCabecalho()
            produtoRodape = ProdutosRodape()

            produtoCab.cod_distribuidor = '11802101000100'
            produtoCab.data_criacao_arquivo = datetime.now()

            with open(arqProd, 'a') as f:
                f.write(produtoCab.linha_formatada)
                f.flush()

            for registro in result[1]:
                produtoDados = ProdutosDados()
                produtoDados.fornecedor_cod = registro[0]
                produtoDados.fornecedor_descricao = registro[1]
                produtoDados.produto_cod = registro[2]
                produtoDados.produto_descricao = registro[3]
                produtoDados.cod_barras = registro[4]
                produtoDados.tipo_embalagem_venda = registro[5]
                produtoDados.volume_embalagem_venda = registro[6]
                produtoDados.status_produto = registro[7]
                produtoDados.data_cadastro = registro[8]

                with open(arqProd, 'a') as f:
                    f.write(produtoDados.linha_formatada)
                    f.flush()

            with open(arqProd, 'a') as f:
                f.write(produtoRodape.linha_formatada)
                f.flush()

            if not self.pai.isVisible():
                self.tray_msg.emit('i', u"IntegradorACCERA", u"Processo dos <strong>Produtos</strong> finalizado!")
            else:
                self.alerta.emit('c', 'IntegradorACCERA', u"Processo dos PRODUTOS finalizado!")
        except Exception, e:
            print "Erro ao processar produtos"
            print '-' * 30
            print e
            print '-' * 30
            if not self.pai.isVisible():
                self.tray_msg.emit('c', u"IntegradorACCERA", u"Erro ao gerar produtos!\nErro: {}".format(e.message))
            else:
                self.alerta.emit('c', 'IntegradorACCERA', "Erro ao gerar produtos!\nErro: {}".format(e.message), unicode(e))
            self.terminate()