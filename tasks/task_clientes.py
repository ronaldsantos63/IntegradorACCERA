#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_clientes                                                    
# Criado em: 22 de Agosto de 2016 as 10:13         
# ----------------------------------------------------------------------

from os import path, remove
from PyQt4.QtCore import QThread, pyqtSignal
from datetime import datetime

from models.clientes import ClienteCabecalho, ClienteDados, ClienteRodape

__app_titulo__ = 'IntegradorACCERA'


class TaskClientes(QThread):
    alerta = pyqtSignal(str, str, str, str)
    tray_msg = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)
    info = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TaskClientes, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            if self.pai.conectado_bd[0]:
                self.tray_msg.emit('i', __app_titulo__, u'Processando Clientes...')
                self.info.emit(u'Processando Clientes...')

                arqClientes = 'ACC_PDVS_' + datetime.now().strftime('%Y%m%d') + '.txt'

                if path.exists(arqClientes):
                    remove(arqClientes)

                cab_cli = ClienteCabecalho()

                cab_cli.distribuidor_cod = str(self.pai.txt_cod_distrbuidor.text())
                cab_cli.data_arquivo = datetime.now()

                with open(arqClientes, 'a') as f:
                    f.write(cab_cli.linha_formatada)

                rod_cli = ClienteRodape()

                result = self.pai.cx.query(
                    "select c.CLICPFCGC, c.CLIDES, c.CLIFAN, 'BRA' as pais, '' regiao, c.CLIEST, c.CLICID, c.CLIBAI, c.CLIEND, '' grupo_rede, '' pdv_classificacao, (select PROPRIO.PRPCGC || ' - ' || PROPRIO.PRPDES from PROPRIO) vendedor, c.CLIDTCAD, c.CLICEP, c.CLIEMAIL, case when coalesce(c.STACOD, '000') = '000' then 'A' else 'I' end cli_status from CLIENTE c where c.CLICOD <> '000000000000000' and c.CLICOD is not NULL",
                    [])

                if result[0]:

                    dados = result[1].fetchall()
                    self.progress_max.emit(len((dados)))
                    contador = 0

                    for registro in dados:
                        contador += 1

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

                        self.progress_value.emit(contador)
                else:
                    print result[1]

                with open(arqClientes, 'a') as f:
                    f.write(rod_cli.linha_formatada)
                    f.flush()

                self.tray_msg.emit('i', __app_titulo__, u'Clientes Finalizado')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__, 'Clientes Finalizado', "")
                self.info.emit(u'Clientes Finalizado')
            else:
                self.tray_msg.emit('i', __app_titulo__ + " - Clientes", u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__ + ' - Clientes', u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!', "")
                self.info.emit(u"Você não está conectado ao banco de dados!")
            self.sleep(3)
            self.info.emit("")
            self.progress_value.emit(0)
        except Exception, e:
            print e
            self.progress_value.emit(0)
            self.info.emit(u"Erro ao processar clientes")
            self.tray_msg.emit('i', __app_titulo__, u'Erro Clientes!\nErro: {}'.format(e))
            if self.pai.isVisible():
                self.alerta.emit('c', __app_titulo__, 'Clientes Error', e)
            self.sleep(3)
            self.terminate()
