#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    IntegradorACCERA                                                    
# Criado em: 04 de Agosto de 2016 as 13:49         
# ----------------------------------------------------------------------

import sys

from PyQt4.QtGui import QApplication
from datetime import datetime

from controllers.connecta import Connecta
from models.estoque import EstoqueCabecalho, EstoqueDados, EstoqueRodape


class IntegradorACCERA(object):
    def __init__(self):
        try:
            self.cx = Connecta()
            self.cx.connectDB()
            result = self.cx.query("select (select PROPRIO.PRPCGC from PROPRIO) as cd_loja, f.FORCGC, coalesce(pa.PROCODAUX, e.procod) as barras, '' numero_lote, '' data_validade_lote, case when coalesce(e.ESTATUSDO, 0) < 0 then 0 else e.ESTATUSDO end as quantidade_estoque, case when coalesce(e.ESTATUSDO, 0) <= 0 then 'H' else 'H' end as tipo_estoque, (select current_timestamp from RDB$DATABASE) as data_estoque from estoque e left outer join produto_fornecedor pf on (pf.PROCOD = e.PROCOD and pf.FORCOD in ('0017','0020')) left outer join FORNECEDOR f on (f.FORCOD = pf.FORCOD and f.FORCOD in ('0017','0020')) left outer join PRODUTOAUX pa on (pa.PROCOD = e.PROCOD) where e.DATULTSAI >= '01/01/2014' and exists ( select 1 from PRODUTO_FORNECEDOR where e.PROCOD = PRODUTO_FORNECEDOR.PROCOD and PRODUTO_FORNECEDOR.FORCOD in ('0017','0020') )", [])

            cab_estoque = EstoqueCabecalho()
            cab_estoque.distribuidor_cod = "11802101000100"
            cab_estoque.data_inicial = datetime.now()
            cab_estoque.data_final = datetime.now()

            arq_estoque = 'ACC_POSESTQ_' + datetime.now().strftime('%Y%m%d') + '.txt'

            with open(arq_estoque, 'a') as f:
                f.write(cab_estoque.linha_formatada)
                f.flush()

            for registro in result[1]:
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

            rodape_estoque = EstoqueRodape()
            with open(arq_estoque, 'a') as f:
                f.write(rodape_estoque.linha_formatada)
                f.flush()
        except Exception, e:
            print e

        print 'finalizado'
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appIntegrador = IntegradorACCERA()
    sys.exit(app.exec_())
