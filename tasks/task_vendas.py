#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_vendas                                                    
# Criado em: 14 de Agosto de 2016 as 18:29         
# ----------------------------------------------------------------------

from PyQt4.QtCore import QThread, pyqtSignal

from datetime import datetime

from controllers.connecta import Connecta
from models.vendas import VendasCabecalho, VendasDados, VendasRodape


class TaskVendas(QThread):
    alerta = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TaskVendas, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            self.cx = Connecta()
            self.cx.connectDB()
            result = self.cx.query(
                "select (select PROPRIO.PRPCGC from PROPRIO) as cd_loja, min(nf.NFSDATSAI) dt_inicial, max(nf.NFSDATSAI) dt_final from NOTAFISCAL nf where exists( select 1 from ITEM_NOTA_FISCAL inf where inf.NFSCTR = nf.NFSCTR and exists( select 1 from PRODUTO_FORNECEDOR pf where pf.PROCOD = inf.PROCOD and pf.FORCOD in ('0017', '0020') ) ) and nf.NFSDATSAI between '07/01/2016' and '07/31/2016'",
                [])

            arqVendas = 'ACC_SELLOUT_' + datetime.now().strftime('%Y%m%d') + '.txt'

            cab_vendas = VendasCabecalho()
            rod_vendas = VendasRodape()

            for registro in result[1]:
                cab_vendas.distribuidor_cod = registro[0]
                cab_vendas.data_inicial = registro[1]
                cab_vendas.data_final = registro[2]
                with open(arqVendas, 'a') as f:
                    f.write(cab_vendas.linha_formatada)
                    f.flush()

            result = self.cx.query(
                "select (select PROPRIO.PRPCGC from PROPRIO) as cd_loja, f.FORCGC, coalesce(pa.PROCODAUX, inf.PROCOD) as procodaux, '' lote_numero, '' lote_data, inf.INFQTDEMB, inf.INFVLRTOT, nf.NFSNUM, nf.NFSDATSAI, case when nf.NFSTIP = 'NFV' then 'V' when nf.NFSTIP = 'CAN' then 'C' end transacao_tip, nf.CFOCOD, case when char_length(nf.NFSCLICPFCGC) < 12 then '1' else '2' end pdv_tipo, nf.NFSCLICPFCGC as pdv_indentif, nf.NFSCLIDES as pdv_descricao, nf.NFSCLICEP as pdv_cep,  '' pdv_classificacao, (select PROPRIO.PRPCGC || ' - ' || PROPRIO.PRPDES from PROPRIO) vendedor, '' livre1, '' livre2  from ITEM_NOTA_FISCAL inf inner join PRODUTO_FORNECEDOR pf on (pf.PROCOD = inf.PROCOD and pf.FORCOD in ('0017', '0020') and exists( select 1 from ITEVDA itv where itv.PROCOD = pf.PROCOD and itv.TRNDAT >= '01/01/2014' )) inner join NOTAFISCAL nf on (nf.NFSCTR = inf.NFSCTR and nf.NFSTIP in ('NFV', 'CAN') and nf.NFSDATSAI between '07/01/2016' and '07/31/2016') left outer join FORNECEDOR f on (f.FORCOD = pf.FORCOD) left outer join PRODUTOAUX pa on (pa.PROCOD = pf.PROCOD)",
                [])

            if result[0]:
                print 'Vai percorrer os dados'
                for registro in result[1]:
                    dados_vendas = VendasDados()
                    print '1'
                    dados_vendas.cd_loja_cod = registro[0]
                    print '2'
                    dados_vendas.fornecedor_cod = registro[1]
                    print '3'
                    dados_vendas.produto_barras = registro[2]
                    print '4'
                    dados_vendas.lote_numero = registro[3]
                    print '5'
                    dados_vendas.lote_data_validade = registro[4]
                    print '6'
                    dados_vendas.saida_quantidade = registro[5]
                    print '7'
                    dados_vendas.valor_unitario = registro[6]
                    print '8'
                    dados_vendas.transacao_identificador = registro[7]
                    print '9'
                    dados_vendas.transacao_data = registro[8]
                    print '10'
                    dados_vendas.transacao_tipo = registro[9]
                    print '11'
                    dados_vendas.cfop = registro[10]
                    print '12'
                    dados_vendas.pdv_identificador_tipo = registro[11]
                    print '13'
                    dados_vendas.pdv_identificador = registro[12]
                    print '14'
                    dados_vendas.pdv_descricao = registro[13]
                    print '15'
                    dados_vendas.pdv_cep = registro[14]
                    print '16'
                    dados_vendas.pdv_classificacao = registro[15]
                    print '17'
                    dados_vendas.vendedor_nome = registro[16]
                    print '18'
                    dados_vendas.campo_livre1 = registro[17]
                    print '19'
                    dados_vendas.campo_livre2 = registro[18]

                    with open(arqVendas, 'a') as f:
                        f.write(dados_vendas.linha_formatada)
                        f.flush()
            else:
                print result[1]

            with open(arqVendas, 'a') as f:
                f.write(rod_vendas.linha_formatada)
                f.flush()
        except Exception, e:
            print e