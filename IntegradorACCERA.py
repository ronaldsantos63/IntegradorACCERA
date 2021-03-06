#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    IntegradorACCERA                                                    
# Criado em: 04 de Agosto de 2016 as 13:49         
# ----------------------------------------------------------------------

import sys
import os
from collections import OrderedDict

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import resources_rc

from ui.frm_principal import Ui_Principal, _fromUtf8
from views.tray import AnimatedSystemTrayIcon

from controllers.connecta import Connecta

# Threads gera arquivos
from tasks.task_produtos import TaskProdutos
from tasks.task_cds_lojas import TaskCDsLojas
from tasks.task_clientes import TaskClientes
from tasks.task_estoque import TaskEstoque
from tasks.task_notas_fiscais_recebidas import TaskNFR
from tasks.task_vendas import TaskVendas

# Thread de monitoramento
from tasks.task_main import TaskMain
from tasks.task_monit_thread import TaskMonitThread

__app_titulo__ = 'IntegradorACCERA'

class IntegradorACCERA(QMainWindow, Ui_Principal):
    def __init__(self, parent=None):
        super(IntegradorACCERA, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(":logo/images/logo/logo.png"))

        movie = QMovie(':/gifs/images/gifs/loading.gif', QByteArray(), self)
        self.tray = AnimatedSystemTrayIcon(movie, self)
        self.tray.setToolTip("IntegradorACCERA")

        self.cnf = QSettings("IntegradorACCERA.ini", QSettings.IniFormat)
        self.cnf.setFallbacksEnabled(False)
        self.cx = Connecta(self)
        self.conectado_bd = self.cx.connectDB()

        #Conficoes para parar e inicar thread de monitoramento
        self.mutex = QMutex()
        self.cond = QWaitCondition()

        # tab atual
        # Tab 0 = Geral | Tab 1 = ACCERA | Tab 2 = BD
        self.__tab_atual = 0

        # Conexoes
        self.cmb_fornecedor_accera.lineEdit().returnPressed.connect(self.add_forn)
        self.bt_add_forn_accera.clicked.connect(self.add_forn)
        self.bt_sair.clicked.connect(self.close)
        self.bt_gravar.clicked.connect(self.salvar_cnf)
        self.bt_testar.clicked.connect(self.teste)
        self.bt_monitorar.clicked.connect(self.on_off_monit)
        self.bt_gerar_arq_retroativo.clicked.connect(self.gera_retroativo)
        self.tabWidget.currentChanged.connect(self.tab_alterado)
        self.tabWidget.setCurrentIndex(self.__tab_atual)

        self.form_load()

    def showEvent(self, *args, **kwargs):
        self.tray.show()

    def teste(self):
        if self.__tab_atual == 0:
            if not self.conectado_bd[0]:
                QMessageBox.warning(self, __app_titulo__, u'Por favor revise suas configurações com o banco de dados!')
                return
            elif self.txt_cod_distrbuidor.text().trimmed().isEmpty():
                QMessageBox.warning(self, __app_titulo__, u'Por favor preencha o campo código do distribuidor!')
                return
            self.gerar()
        else:
            self.teste_conn_bd()

    def teste_conn_bd(self):
        self.salvar_cnf(True)
        self.conectado_bd = self.cx.connectDB()

        if self.conectado_bd[0]:
            self.bt_monitorar.setEnabled(True)
            self.bt_gerar_arq_retroativo.setEnabled(True)
            self.grp_filtro_arq_retroativo.setEnabled(True)
            self.txt_cod_distrbuidor.setText(self.cx.query("select COALESCE(prpcgc, '') from proprio")[1].fetchone()[0])
        else:
            self.bt_monitorar.setEnabled(False)
            self.bt_gerar_arq_retroativo.setEnabled(False)
            self.grp_filtro_arq_retroativo.setEnabled(False)
        self.popularComboFornecedores()
        QMessageBox.information(self, __app_titulo__, self.conectado_bd[1])

    def tab_alterado(self, indx_tab):
        self.__tab_atual = indx_tab
        if indx_tab == 1:
            self.bt_testar.setEnabled(False)
        elif indx_tab == 0:
            if self.conectado_bd[0]:
                self.bt_testar.setEnabled(True)
            else:
                self.bt_testar.setEnabled(False)
        elif indx_tab == 2:
            self.bt_testar.setEnabled(True)
        elif indx_tab == 3:
            self.bt_testar.setEnabled(False)
            self.dtInicial.setFocus()

    def gerar(self, data=None):

        pool_thread = []

        task_produto = TaskProdutos(self, data)
        task_cds_lojas = TaskCDsLojas(self, data)
        task_estoque = TaskEstoque(self, data)
        task_vendas = TaskVendas(self, data)
        task_clientes = TaskClientes(self, data)
        task_nfe_receb = TaskNFR(self, data)
        if self.grp_accera_produtos.isChecked():

            pool_thread.append(task_produto)

            task_produto.alerta.connect(self.alertas_internos)
            task_produto.progress_max.connect(self.pbar.setMaximum)
            task_produto.progress_value.connect(self.pbar.setValue)
            task_produto.tray_msg.connect(self.tray_message)
            task_produto.info.connect(self.lbl_info.setText)

            if self.grp_accera_cds_lojas.isChecked():
                task_produto.finished.connect(task_cds_lojas.start)

            task_produto.start()
        if self.grp_accera_cds_lojas.isChecked():

            pool_thread.append(task_cds_lojas)

            task_cds_lojas.alerta.connect(self.alertas_internos)
            task_cds_lojas.progress_max.connect(self.pbar.setMaximum)
            task_cds_lojas.progress_value.connect(self.pbar.setValue)
            task_cds_lojas.tray_msg.connect(self.tray_message)
            task_cds_lojas.info.connect(self.lbl_info.setText)

            if self.grp_accera_estoque.isChecked():
                task_cds_lojas.finished.connect(task_estoque.start)

            if not self.grp_accera_produtos.isChecked():
                task_cds_lojas.start()

        if self.grp_accera_estoque.isChecked():

            pool_thread.append(task_estoque)

            task_estoque.alerta.connect(self.alertas_internos)
            task_estoque.progress_max.connect(self.pbar.setMaximum)
            task_estoque.progress_value.connect(self.pbar.setValue)
            task_estoque.tray_msg.connect(self.tray_message)
            task_estoque.info.connect(self.lbl_info.setText)

            if self.grp_accera_vendas_distrib.isChecked():
                task_estoque.finished.connect(task_vendas.start)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked():
                task_estoque.start()

        if self.grp_accera_vendas_distrib.isChecked():

            pool_thread.append(task_vendas)

            task_vendas.alerta.connect(self.alertas_internos)
            task_vendas.progress_max.connect(self.pbar.setMaximum)
            task_vendas.progress_value.connect(self.pbar.setValue)
            task_vendas.tray_msg.connect(self.tray_message)
            task_vendas.info.connect(self.lbl_info.setText)

            if self.grp_accera_clientes.isChecked():
                task_vendas.finished.connect(task_clientes.start)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked() \
                    and not self.grp_accera_estoque.isChecked():
                task_vendas.start()

        if self.grp_accera_clientes.isChecked():

            pool_thread.append(task_clientes)

            task_clientes.alerta.connect(self.alertas_internos)
            task_clientes.progress_max.connect(self.pbar.setMaximum)
            task_clientes.progress_value.connect(self.pbar.setValue)
            task_clientes.tray_msg.connect(self.tray_message)
            task_clientes.info.connect(self.lbl_info.setText)

            if self.grp_accera_nfe_receb.isChecked():
                task_clientes.finished.connect(task_nfe_receb.start)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked() \
                    and not self.grp_accera_estoque.isChecked() and not self.grp_accera_vendas_distrib.isChecked():
                task_clientes.start()

        if self.grp_accera_nfe_receb.isChecked():

            pool_thread.append(task_nfe_receb)

            task_nfe_receb.alerta.connect(self.alertas_internos)
            task_nfe_receb.progress_max.connect(self.pbar.setMaximum)
            task_nfe_receb.progress_value.connect(self.pbar.setValue)
            task_nfe_receb.tray_msg.connect(self.tray_message)
            task_nfe_receb.info.connect(self.lbl_info.setText)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked() \
                    and not self.grp_accera_estoque.isChecked() and not self.grp_accera_vendas_distrib.isChecked() \
                    and not self.grp_accera_clientes.isChecked():
                task_nfe_receb.start()

        task_monit_thread = TaskMonitThread(self, pool_thread)
        task_monit_thread.finished.connect(self.destrava)
        # task_monit_thread.finished.connect(self.mutex.unlock)
        task_monit_thread.start()

    def destrava(self):
        # self.mutex.unlock()
        self.cond.wakeAll()

    def tray_message(self, tipo='i', titulo='IntegradorACCERA', mensagem=''):
        pass

    def form_load(self):
        self.dtFinal.setVisible(False)
        self.popularComboFornecedores()

        #
        self.dtFinal.setDate(QDate.currentDate())
        self.dtInicial.setDate(QDate.currentDate())

        # Lendo conf e populando controles
        # Populando aba geral
        self.cnf.beginGroup('GERAL')
        self.dte_hora.setTime(QTime.fromString(self.cnf.value("hora_gerar_arq", "05:00:00").toString(), Qt.TextDate))
        self.txt_local_gravar_arquivos.setText(self.cnf.value("local_gravar_arquivos", os.getcwd() + os.sep + "arquivos").toString())
        ls_fornecedores = self.cnf.value("lista_accera_fornecedores", []).toPyObject()
        if ls_fornecedores:
            self.popularTabela(ls_fornecedores)
        self.cnf.endGroup()

        # populando conf. ACCERA
        self.cnf.beginGroup('ACCERA')
        self.grp_accera_produtos.setChecked(self.cnf.value("gerar_produtos", True).toBool())
        self.grp_accera_cds_lojas.setChecked(self.cnf.value("gerar_cds_lojas", True).toBool())
        self.grp_accera_estoque.setChecked(self.cnf.value("gerar_estoque", True).toBool())
        self.rad_accera_estoque_posicao_atual.setChecked(self.cnf.value("gerar_estoque_atual", True).toBool())
        self.rad_accera_estoque_ult_5_dias.setChecked(self.cnf.value("gerar_estoque_ult_5_dias", False).toBool())
        self.grp_accera_vendas_distrib.setChecked(self.cnf.value("gerar_vendas_distribuidor", True).toBool())
        self.grp_accera_clientes.setChecked(self.cnf.value("gerar_clientes", True).toBool())
        self.grp_accera_nfe_receb.setChecked(self.cnf.value("gerar_nfe_recebidas", True).toBool())
        self.cnf.endGroup()

        # Populando conf. BD
        self.cnf.beginGroup('BD')
        self.cmb_sgbd.setCurrentIndex(self.cmb_sgbd.findText(self.cnf.value("sgbd", "").toString()))
        self.txt_servidor.setText(self.cnf.value("servidor", "").toString())
        self.txt_usuario.setText(self.cnf.value("usuario", "").toString())
        self.txt_senha.setText(self.cnf.value("senha", "").toString())
        self.txt_porta.setText(self.cnf.value("porta", "").toString())
        self.txt_banco.setText(self.cnf.value("banco", "").toString())
        self.cnf.endGroup()

        if self.conectado_bd[0]:
            self.txt_cod_distrbuidor.setText(self.cx.query("select COALESCE(prpcgc, '') from proprio")[1].fetchone()[0])
        else:
            QMessageBox.warning(self, 'Alerta', u"Você não está conectado ao banco de dados!")
            self.bt_monitorar.setEnabled(False)
            self.bt_gerar_arq_retroativo.setEnabled(False)
            self.grp_filtro_arq_retroativo.setEnabled(False)

    def salvar_cnf(self, teste=True):
        try:
            print teste
            # Salvando dados da aba Geral
            self.cnf.beginGroup("GERAL")
            self.cnf.setValue('hora_gerar_arq', self.dte_hora.time().toString(Qt.TextDate))
            self.cnf.setValue("lista_accera_fornecedores", self.pegaDadosTabela())
            self.cnf.setValue("local_gravar_arquivos", self.txt_local_gravar_arquivos.text())
            self.cnf.endGroup()

            # Salvando dados da aba Conf ACCERA
            self.cnf.beginGroup("ACCERA")
            self.cnf.setValue('gerar_produtos', self.grp_accera_produtos.isChecked())
            self.cnf.setValue('gerar_cds_lojas', self.grp_accera_cds_lojas.isChecked())
            self.cnf.setValue('gerar_estoque', self.grp_accera_estoque.isChecked())
            self.cnf.setValue('gerar_estoque_atual', self.rad_accera_estoque_posicao_atual.isChecked())
            self.cnf.setValue('gerar_estoque_ult_5_dias', self.rad_accera_estoque_ult_5_dias.isChecked())
            self.cnf.setValue('gerar_vendas_distribuidor', self.grp_accera_vendas_distrib.isChecked())
            self.cnf.setValue('gerar_clientes', self.grp_accera_clientes.isChecked())
            self.cnf.setValue('gerar_nfe_recebidas', self.grp_accera_nfe_receb.isChecked())
            self.cnf.endGroup()

            # Salvando dados da aba Conf BD
            self.cnf.beginGroup('BD')
            self.cnf.setValue('sgbd', self.cmb_sgbd.currentText())
            self.cnf.setValue('servidor', self.txt_servidor.text())
            self.cnf.setValue('usuario', self.txt_usuario.text())
            self.cnf.setValue('senha', self.txt_senha.text())
            self.cnf.setValue('porta', self.txt_porta.text())
            self.cnf.setValue('banco', self.txt_banco.text())
            self.cnf.endGroup()

            if not teste:
                QMessageBox.information(self, 'IntegradorACCERA', "Salvo com sucesso!")
            else:
                print 'Configuracao salva pelo botao teste'
        except Exception, e:
            if not teste:
                QMessageBox.critical(self, 'IntegradorACCERA', _fromUtf8(unicode(e)))
            else:
                print 'Erro ao salvar conf pelo botao teste'
                print e

    def add_forn(self):
        """
        Função que adiciona item no controle tb_fornecedores ao clicar no controle bt_add_forn
        """
        r = self.cx.query("select forcod, fordes from fornecedor where fordes = ?",
                          [unicode(self.cmb_fornecedor_accera.currentText())])
        if r[0]:
            r = r[1].fetchall()

            if r:
                for registro in r:
                    linha = 0 if self.tb_fornecedores.rowCount() == 0 else self.tb_fornecedores.rowCount()
                    self.tb_fornecedores.insertRow(linha)
                    self.tb_fornecedores.setItem(linha, 0, QTableWidgetItem(registro[0]))
                    self.tb_fornecedores.setItem(linha, 1, QTableWidgetItem(registro[1]))
                    self.cmb_fornecedor_accera.setCurrentIndex(-1)
            else:
                QMessageBox.warning(self, 'IntegradorACCERA',
                                    u'Não foi encontrado nenhum fornecedor com o nome: {}'.format(
                                            unicode(self.cmb_fornecedor_accera.currentText()))
                                    )
        else:
            print r[1]

    def popularComboFornecedores(self):
        """
        Função que popula o controle ComboFornecedores com os dados do banco de dados!
        """
        if self.conectado_bd[0]:
            r = self.cx.query("select fordes from fornecedor where forcod is not null and forcod <> '0000'")
            self.cmb_fornecedor_accera.clear()
            if r[0]:
                r = r[1].fetchall()
                if r:
                    for item in r:
                        self.cmb_fornecedor_accera.addItem(item[0])
            self.cmb_fornecedor_accera.setCurrentIndex(-1)

    def popularTabela(self, valores=[], colunaOrdenacao=0):
        """
        Função que popula uma tabela com os dados do comboFornecedores
        """
        self.limparTabela()
        nvalores = len(valores)
        progresso = QProgressDialog('Populando Tabela...', 'Cancelar', 0, nvalores, self)
        progresso.setWindowTitle('IntegradorACCERA')
        progresso.setWindowModality(Qt.WindowModal)
        z = 0
        for x in valores:
            # print x
            # print 'Chaves: {}'.format(x.keys())
            # print 'Valores: {}'.format(x.values())
            linha = 0 if self.tb_fornecedores.rowCount() == 0 else self.tb_fornecedores.rowCount()
            self.tb_fornecedores.insertRow(linha)
            self.tb_fornecedores.setItem(linha, 0, QTableWidgetItem(x['codigo']))
            self.tb_fornecedores.setItem(linha, 1, QTableWidgetItem(x['descricao']))
            z += 1
            progresso.setValue(z)

    def pegaDadosTabela(self):
        """
        Função que pega os dados do controle tb_fornecedores

        :return: Lista de Fornecedores
        """
        ls_fornecedores = []
        for row in xrange(0, self.tb_fornecedores.rowCount()):
            fornecedor = OrderedDict()

            fornecedor['codigo'] = self.tb_fornecedores.item(row, 0).text()
            fornecedor['descricao'] = self.tb_fornecedores.item(row, 1).text()

            ls_fornecedores.append(fornecedor)
        return ls_fornecedores

    def limparTabela(self):
        """
        Função que limpa todos os dados do QTable
        """
        self.tb_fornecedores.clearContents()
        while self.tb_fornecedores.rowCount() != 0:
            quatidade = self.tb_fornecedores.rowCount()
            if quatidade == 0:
                self.tb_fornecedores.removeRow(quatidade)
            for x in range(quatidade):
                self.tb_fornecedores.removeRow(x)

    def alertas_internos(self, tipo="i", titulo="IntegradorACCERA", mensagem="Mensagem", erro=""):
        """
        Resposavel por emitir os alertas dos processos em segundo plano em um QMessageBox
        :param tipo: Tipo de Alerta [ i = Informação  | c = Crítico | a = Alerta]
        :param titulo: Titulo da mensagem
        :param mensagem: Mensagem informativa
        :param erro: Mensagem de erro
        """

        alerta = QMessageBox(self)
        if tipo == 'i':
            alerta.setIcon(QMessageBox.Information)
        elif tipo == 'a':
            alerta.setIcon(QMessageBox.Warning)
        elif tipo == 'c':
            alerta.setIcon(QMessageBox.Critical)

        alerta.setWindowTitle(titulo)
        alerta.setText(mensagem)
        if erro != '':
            alerta.setDetailedText(erro)
        alerta.show()

    def on_off_monit(self):
        if self.bt_monitorar.text() == "Iniciar Monitoramento":
            self.bt_monitorar.setText('Parar Monitoramento')
            self.tabWidget.setEnabled(False)

            self.th_main = TaskMain(self, self.mutex, self.cond)
            self.th_main.gerar.connect(self.gerar)
            self.th_main.start()
            self.hide()
            self.tray.showMessage('IntegradorACCERA - informa', u"Aplicação rodando em segundo plano!", self.tray.Information)
        else:
            try:
                self.th_main.parar()
                self.bt_monitorar.setText("Iniciar Monitoramento")
                self.tabWidget.setEnabled(True)
            except Exception, e:
                print e

    def gera_retroativo(self):
        self.gerar(self.dtInicial.dateTime().toPyDateTime())
        self.dtInicial.setFocus()

    def keyPressEvent(self, event=QKeyEvent):
        if event.key() == Qt.Key_F2 and self.txt_local_gravar_arquivos.hasFocus():
            pasta = QFileDialog.getExistingDirectory(self, u"Escolha a pasta onde deseja gravar os arquivos gerados")
            if pasta:
                if not QFile.exists(pasta):
                    QMessageBox.warning(self, "Alerta", u"A pasta seleciona não existe")
                    return
            else:
                return

            self.txt_local_gravar_arquivos.setText(pasta)

    def closeEvent(self, evt):
        if not self.isVisible():
            bt1 = _fromUtf8("Abrir aplicação?")
        else:
            bt1 = "Minimizar para o tray?"

        result = QMessageBox.question(self, _fromUtf8("IntegradorACCERA questiona"), "O que deseja fazer?", bt1,
                                      "Cancelar?", u"Fechar a aplicação?")
        if result == 0:
            print "Evento 0"
            evt.ignore()
            if self.isVisible():
                print "Entrou no if"
                self.hide()
                # self.tray.show()
                self.tray.showMessage(_fromUtf8("IntegradorACCERA Informa"), u"Aplicação rodando em Tray!", self.tray.Information)
            else:
                print "Entrou no else"
                self.show()
        elif 1 == result:
            print "Evento 1"
            evt.ignore()
            if not self.isVisible():
                self.show()
                self.hide()
                self.tray.showMessage(_fromUtf8("Integrador Informa"), u"Aplicação rodando em Tray!", self.tray.Information)
                pass
        elif 2 == result:
            evt.accept()
            qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    appIntegrador = IntegradorACCERA()
    appIntegrador.show()
    sys.exit(app.exec_())
