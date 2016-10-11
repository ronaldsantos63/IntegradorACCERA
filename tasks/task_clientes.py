#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_clientes                                                    
# Criado em: 22 de Agosto de 2016 as 10:13         
# ----------------------------------------------------------------------

from PyQt4.QtCore import QThread, pyqtSignal

from datetime import datetime

from controllers.connecta import Connecta
from models.clientes import ClienteCabecalho, ClienteDados, ClienteRodape


class TaskClientes(QThread):
    alerta = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TaskClientes, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            self.cx = Connecta()
            self.cx.connectDB()

            arqClientes = 'ACC_PDVS_' + datetime.now().strftime('%Y%m%d') + '.txt'

            cab_cli = ClienteCabecalho()

            cab_cli.distribuidor_cod = '11802101000100'
            cab_cli.data_arquivo = datetime.now()

            with open(arqClientes, 'a') as f:
                f.write(cab_cli.linha_formatada)

            rod_cli = ClienteRodape()

            result = self.cx.query(
                "select c.CLICPFCGC, c.CLIDES, c.CLIFAN, 'BRA' as pais, '' regiao, c.CLIEST, c.CLICID, c.CLIBAI, c.CLIEND, '' grupo_rede, '' pdv_classificacao, (select PROPRIO.PRPCGC || ' - ' || PROPRIO.PRPDES from PROPRIO) vendedor, c.CLIDTCAD, c.CLICEP, c.CLIEMAIL, case when coalesce(c.STACOD, '000') = '000' then 'A' else 'I' end cli_status from CLIENTE c where c.CLICOD <> '000000000000000'",
                [])

            if result[0]:
                for registro in result[1]:
                    dados_cli = ClienteDados()
                    dados_cli.cpf_cnpj = registro[0]
                    dados_cli.razao_social = registro[1]
                    dados_cli.fantasia = registro[2]
                    dados_cli.pais = registro[3]
                    dados_cli.regiao = registro[4]
                    dados_cli.estado = registro[5]
                    dados_cli.cidade = registro[6]
                    dados_cli.bairro = registro[7]
                    dados_cli.endereco = registro[8]
                    dados_cli.grupo_rede = registro[9]
                    dados_cli.pdv_classificacao = registro[10]
                    dados_cli.vendedor_nome = registro[11]
                    dados_cli.data_cadastro = registro[12]
                    dados_cli.pdv_cep = registro[13]
                    dados_cli.contato_email = registro[14]
                    dados_cli.status = registro[15]

                    with open(arqClientes, 'a') as f:
                        f.write(dados_cli.linha_formatada)
                        f.flush()
            else:
                print result[1]

            with open(arqClientes, 'a') as f:
                f.write(rod_cli.linha_formatada)
                f.flush()
        except Exception, e:
            print e