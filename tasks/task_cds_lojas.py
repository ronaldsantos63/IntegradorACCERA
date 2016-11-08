#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    task_cds_lojas                                                    
# Criado em: 05 de Agosto de 2016 as 16:45         
# ----------------------------------------------------------------------

from os import path, remove
from PyQt4.QtCore import QThread, pyqtSignal
from datetime import datetime

from models.cds_lojas import CDsLojasCabecalho, CDsLojasDados, CDsLojasRodape

__app_titulo__ = 'IntegradorACCERA'


class TaskCDsLojas(QThread):
    alerta = pyqtSignal(str, str, str, str)
    tray_msg = pyqtSignal(str, str, str)
    progress_max = pyqtSignal(int)
    progress_value = pyqtSignal(int)
    info = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TaskCDsLojas, self).__init__(parent)
        self.pai = parent

    def run(self):
        try:
            if self.pai.conectado_bd[0]:
                self.tray_msg.emit('i', __app_titulo__, u'Processando CDs/Lojas...')
                self.info.emit(u'Processando CDs/Lojas...')
                self.sleep(1)

                result = self.pai.cx.query("select p.PRPCGC, p.PRPDES, p.PRPUF, p.PRPMUN, p.PRPBAI, p.PRPCEP, 'A' as status_loja from PROPRIO p", [])

                cdsLojasCab = CDsLojasCabecalho()
                cdsLojasCab.distribuidor_cod = str(self.pai.txt_cod_distrbuidor.text())
                cdsLojasCab.data_criacao_arquivo = datetime.now()

                arqCDsLoja = 'ACC_CADSITE_' + datetime.now().strftime('%Y%m%d') + '.txt'

                if path.exists(arqCDsLoja):
                    remove(arqCDsLoja)

                with open(arqCDsLoja, 'a') as f:
                    f.write(cdsLojasCab.linha_formatada)
                    f.flush()

                dados = result[1].fetchall()
                self.progress_max.emit(len(dados))

                contador = 0

                for registro in dados:
                    contador += 1

                    cdslojasDados = CDsLojasDados()
                    cdslojasDados.cd_loja_cod = registro[0]
                    cdslojasDados.cd_loja_descricao = registro[1]
                    cdslojasDados.cd_loja_uf = registro[2]
                    cdslojasDados.cd_loja_cidade = registro[3]
                    cdslojasDados.cd_loja_bairro = registro[4]
                    cdslojasDados.cd_loja_cep = registro[5]
                    cdslojasDados.cd_loja_status = registro[6]

                    with open(arqCDsLoja, 'a') as f:
                        f.write(cdslojasDados.linha_formatada)
                        f.flush()

                    self.progress_value.emit(contador)

                cdslojasRodape = CDsLojasRodape()
                with open(arqCDsLoja, 'a') as f:
                    f.write(cdslojasRodape.linha_formatada)
                    f.flush()

                self.tray_msg.emit('i', __app_titulo__, u'CDs/Lojas Finalizado')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__, 'CDs/Lojas Finalizado', "")
            else:
                self.tray_msg.emit('i', __app_titulo__ + " - CDs/Lojas", u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!')
                if self.pai.isVisible():
                    self.alerta.emit('i', __app_titulo__ + ' - CDs/Lojas', u'Você não está conectado ao banco de dados!\n'
                                                        u'Por favor revise suas configurações de conexão!', "")
            self.info.emit(u'CDs/Lojas Finalizado')
            self.sleep(3)
            self.info.emit("")
            self.progress_value.emit(0)
        except Exception, e:
            print e
            self.progress_value.emit(0)
            self.progress_max.emit(100)
            self.info.emit(u"Erro no processo CDs/Lojas!")
            self.tray_msg.emit('i', __app_titulo__, u'Erro CDs/Lojas!\nErro: {}'.format(e))
            if self.pai.isVisible():
                self.alerta.emit('c', __app_titulo__, 'CDs/Lojas Error', e)
            self.sleep(3)
            self.terminate()