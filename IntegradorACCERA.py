#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    IntegradorACCERA                                                    
# Criado em: 04 de Agosto de 2016 as 13:49         
# ----------------------------------------------------------------------

import sys
from collections import OrderedDict

from PyQt4.QtGui import QApplication, QMainWindow, QProgressDialog, QTableWidgetItem, QMessageBox
from PyQt4.QtCore import QSettings, QTime, Qt, QString

from ui.frm_principal import Ui_Principal, _fromUtf8
from controllers.connecta import Connecta

# Threads gera arquivos
from tasks.task_produtos import TaskProdutos
from tasks.task_cds_lojas import TaskCDsLojas
from tasks.task_clientes import TaskClientes
from tasks.task_estoque import TaskEstoque
from tasks.task_notas_fiscais_recebidas import TaskNFR
from tasks.task_vendas import TaskVendas

#Thread de monitoramento
from tasks.task_main import TaskMain


class IntegradorACCERA(QMainWindow, Ui_Principal):
    def __init__(self, parent=None):
        super(IntegradorACCERA, self).__init__(parent)
        self.setupUi(self)
        self.__cnf = QSettings("IntegradorACCERA.ini", QSettings.IniFormat)
        self.__cnf.setFallbacksEnabled(False)
        self.__cx = Connecta(self)
        self.__conectado_bd = self.__cx.connectDB()

        # Conexoes
        # self.cmb_fornecedor_accera.currentIndexChanged[QString].connect(self.add_forn)
        self.cmb_fornecedor_accera.lineEdit().returnPressed.connect(self.add_forn)
        self.bt_add_forn_accera.clicked.connect(self.add_forn)
        self.bt_sair.clicked.connect(self.close)
        self.bt_gravar.clicked.connect(self.salvar_cnf)

        self.form_load()

    def gerar(self):
        task_produto = TaskProdutos(self)
        task_cds_lojas = TaskCDsLojas(self)
        task_estoque = TaskEstoque(self)
        task_vendas = TaskVendas(self)
        task_clientes = TaskClientes(self)
        task_nfe_receb = TaskNFR(self)
        if self.grp_accera_produtos.isChecked():
            task_produto.alerta.connect(self.alertas_internos)
            task_produto.progress_max.connect(self.pbar.setMaximum)
            task_produto.progress_value.connect(self.pbar.setValue)
            task_produto.tray_msg.connect(self.tray_message)

            if self.grp_accera_cds_lojas.isChecked():
                task_produto.finished.connect(task_cds_lojas.start)

            task_produto.start()
        if self.grp_accera_cds_lojas.isChecked():
            task_cds_lojas.alerta.connect(self.alertas_internos)
            task_cds_lojas.progress_max.connect(self.pbar.setMaximum)
            task_cds_lojas.progress_value.connect(self.pbar.setValue)
            task_cds_lojas.tray_msg.connect(self.tray_message)

            if self.grp_accera_estoque.isChecked():
                task_cds_lojas.finished.connect(task_cds_lojas.start)

            if not self.grp_accera_produtos.isChecked():
                task_cds_lojas.start()

        if self.grp_accera_estoque.isChecked():
            task_estoque.alerta.connect(self.alertas_internos)
            task_estoque.progress_max.connect(self.pbar.setMaximum)
            task_estoque.progress_value.connect(self.pbar.setValue)
            task_estoque.tray_msg.connect(self.tray_message)

            if self.grp_accera_vendas_distrib.isChecked():
                task_estoque.finished.connect(task_vendas.start)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked():
                task_estoque.start()

        if self.grp_accera_vendas_distrib.isChecked():
            task_vendas.alerta.connect(self.alertas_internos)
            task_vendas.progress_max.connect(self.pbar.setMaximum)
            task_vendas.progress_value.connect(self.pbar.setValue)
            task_vendas.tray_msg.connect(self.tray_message)

            if self.grp_accera_clientes_distrib.isChecked():
                task_vendas.finished.connect(task_clientes.start)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked() \
                    and not self.grp_accera_estoque.isChecked():
                task_vendas.start()

        if self.grp_accera_clientes.isChecked():
            task_clientes.alerta.connect(self.alertas_internos)
            task_clientes.progress_max.connect(self.pbar.setMaximum)
            task_clientes.progress_value.connect(self.pbar.setValue)
            task_clientes.tray_msg.connect(self.tray_message)

            if self.grp_accera_nfe_receb_distrib.isChecked():
                task_clientes.finished.connect(task_nfe_receb.start)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked() \
                    and not self.grp_accera_estoque.isChecked() and not self.grp_accera_vendas_distrib.isChecked():
                task_clientes.start()

        if self.grp_accera_nfe_receb.isChecked():
            task_nfe_receb.alerta.connect(self.alertas_internos)
            task_nfe_receb.progress_max.connect(self.pbar.setMaximum)
            task_nfe_receb.progress_value.connect(self.pbar.setValue)
            task_nfe_receb.tray_msg.connect(self.tray_message)

            if not self.grp_accera_produtos.isChecked() and not self.grp_accera_cds_lojas.isChecked() \
                    and not self.grp_accera_estoque.isChecked() and not self.grp_accera_vendas_distrib.isChecked() \
                    and not self.grp_accera_clientes.isChecked():
                task_nfe_receb.start()

    def tray_message(self, tipo='i', titulo='IntegradorACCERA', mensagem=''):
        pass

    def form_load(self):
        self.popularComboFornecedores()

        # Lendo conf e populando controles
        # Populando aba geral
        self.__cnf.beginGroup('GERAL')
        self.dte_hora.setTime(QTime.fromString(self.__cnf.value("hora_gerar_arq", "05:00:00").toString(), Qt.TextDate))
        ls_fornecedores = self.__cnf.value("lista_accera_fornecedores", []).toPyObject()
        if ls_fornecedores:
            self.popularTabela(ls_fornecedores)
        self.__cnf.endGroup()

        # populando conf. ACCERA
        self.__cnf.beginGroup('ACCERA')
        self.grp_accera_produtos.setChecked(self.__cnf.value("gerar_produtos", True).toBool())
        self.grp_accera_cds_lojas.setChecked(self.__cnf.value("gerar_cds_lojas", True).toBool())
        self.grp_accera_estoque.setChecked(self.__cnf.value("gerar_estoque", True).toBool())
        self.rad_accera_estoque_posicao_atual.setChecked(self.__cnf.value("gerar_estoque_atual", True).toBool())
        self.rad_accera_estoque_ult_5_dias.setChecked(self.__cnf.value("gerar_estoque_ult_5_dias", False).toBool())
        self.grp_accera_vendas_distrib.setChecked(self.__cnf.value("gerar_vendas_distribuidor", True).toBool())
        self.grp_accera_clientes.setChecked(self.__cnf.value("gerar_clientes", True).toBool())
        self.grp_accera_nfe_receb.setChecked(self.__cnf.value("gerar_nfe_recebidas", True).toBool())
        self.__cnf.endGroup()

        # Populando conf. BD
        self.__cnf.beginGroup('BD')
        self.cmb_sgbd.setCurrentIndex(self.cmb_sgbd.findText(self.__cnf.value("sgbd", "").toString()))
        self.txt_servidor.setText(self.__cnf.value("servidor", "").toString())
        self.txt_usuario.setText(self.__cnf.value("usuario", "").toString())
        self.txt_senha.setText(self.__cnf.value("senha", "").toString())
        self.txt_porta.setText(self.__cnf.value("porta", "").toString())
        self.txt_banco.setText(self.__cnf.value("banco", "").toString())
        self.__cnf.endGroup()

        if self.__conectado_bd[0]:
            self.__cx.query("select prpcgc from proprio")

    def salvar_cnf(self):
        try:
            # Salvando dados da aba Geral
            self.__cnf.beginGroup("GERAL")
            self.__cnf.setValue('hora_gerar_arq', self.dte_hora.time().toString(Qt.TextDate))
            self.__cnf.setValue("lista_accera_fornecedores", self.pegaDadosTabela())
            self.__cnf.endGroup()

            # Salvando dados da aba Conf ACCERA
            self.__cnf.beginGroup("ACCERA")
            self.__cnf.setValue('gerar_produtos', self.grp_accera_produtos.isChecked())
            self.__cnf.setValue('gerar_cds_lojas', self.grp_accera_cds_lojas.isChecked())
            self.__cnf.setValue('gerar_estoque', self.grp_accera_estoque.isChecked())
            self.__cnf.setValue('gerar_estoque_atual', self.rad_accera_estoque_posicao_atual.isChecked())
            self.__cnf.setValue('gerar_estoque_ult_5_dias', self.rad_accera_estoque_ult_5_dias.isChecked())
            self.__cnf.setValue('gerar_vendas_distribuidor', self.grp_accera_vendas_distrib.isChecked())
            self.__cnf.setValue('gerar_clientes', self.grp_accera_clientes.isChecked())
            self.__cnf.setValue('gerar_nfe_recebidas', self.grp_accera_nfe_receb.isChecked())
            self.__cnf.endGroup()

            # Salvando dados da aba Conf BD
            self.__cnf.beginGroup('BD')
            self.__cnf.setValue('sgbd', self.cmb_sgbd.currentText())
            self.__cnf.setValue('servidor', self.txt_servidor.text())
            self.__cnf.setValue('usuario', self.txt_usuario.text())
            self.__cnf.setValue('senha', self.txt_senha.text())
            self.__cnf.setValue('porta', self.txt_porta.text())
            self.__cnf.setValue('banco', self.txt_banco.text())
            self.__cnf.endGroup()
            QMessageBox.information(self, 'IntegradorACCERA', "Salvo com sucesso!")
        except Exception, e:
            QMessageBox.critical(self, 'IntegradorACCERA', _fromUtf8(unicode(e)))

    def add_forn(self):
        r = self.__cx.query("select forcod, fordes from fornecedor where fordes = ?", [unicode(self.cmb_fornecedor_accera.currentText())])
        if r[0]:
            r = r[1]
            for registro in r:
                linha = 0 if self.tb_fornecedores.rowCount() == 0 else self.tb_fornecedores.rowCount()
                self.tb_fornecedores.insertRow(linha)
                self.tb_fornecedores.setItem(linha, 0, QTableWidgetItem(registro[0]))
                self.tb_fornecedores.setItem(linha, 1, QTableWidgetItem(registro[1]))
                self.cmb_fornecedor_accera.setCurrentIndex(-1)
        else:
            print r[1]

    def popularComboFornecedores(self):
        r = self.__cx.query("select fordes from fornecedor where forcod <> '0000'")
        if r[0]:
            r = r[1].fetchall()
            for item in r:
                self.cmb_fornecedor_accera.addItem(item[0])
        self.cmb_fornecedor_accera.setCurrentIndex(-1)

    def popularTabela(self, valores=[], colunaOrdenacao=0):
        '''
        Função que popula uma tabela
        '''
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
        ls_fornecedores = []
        for row in xrange(0, self.tb_fornecedores.rowCount()):
            fornecedor = OrderedDict()

            fornecedor['codigo'] = self.tb_fornecedores.item(row, 0).text()
            fornecedor['descricao'] = self.tb_fornecedores.item(row, 1).text()

            ls_fornecedores.append(fornecedor)
        return ls_fornecedores

    def limparTabela(self):
        self.tb_fornecedores.clearContents()
        while self.tb_fornecedores.rowCount() != 0:
            quatidade = self.tb_fornecedores.rowCount()
            if quatidade == 0:
                self.tb_fornecedores.removeRow(quatidade)
            for x in range(quatidade):
                self.tb_fornecedores.removeRow(x)

    def alertas_internos(self, tipo="i", titulo="IntegradorACCERA", mensagem="Mensagem", erro=""):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appIntegrador = IntegradorACCERA()
    appIntegrador.show()
    sys.exit(app.exec_())
