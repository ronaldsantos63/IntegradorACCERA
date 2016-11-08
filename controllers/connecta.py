#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    Connecta                                                    
# Criado em: 04 de Agosto de 2016 as 13:50         
# ----------------------------------------------------------------------

import fdb

from PyQt4.QtCore import QSettings


class Connecta(object):
    def __init__(self, parent=None):
        super(Connecta, self).__init__()
        self.__parent = parent
        self.__conn = None
        self.cursorQuery = None
        self.__cursorCommand = None

    def connectDB(self):
        try:
            if not self.__conn is None:
                self.__conn.close()
                self.__conn = None

            self.__parent.cnf.beginGroup('BD')
            host = str(self.__parent.cnf.value('servidor', '127.0.0.1').toString())
            usuario = str(self.__parent.cnf.value('usuario', 'sysdba').toString())
            senha = str(self.__parent.cnf.value('senha', 'masterkey').toString())
            porta = int(self.__parent.cnf.value('porta', '3050').toString())
            banco = str(self.__parent.cnf.value('banco', 'C:/syspdv/syspdv_srv.fdb').toString())
            self.__parent.cnf.endGroup()

            self.__conn = fdb.connect(host=host, user=usuario, password=senha,
                                      port=porta, database=banco, charset='ISO8859_1')
            self.__cursorCommand = self.__conn.cursor()
            print 'Conectado com sucesso!'
            return [True, u'Conectado com sucesso!']
        except Exception, e:
            print u'Erro ao conectar!\nErro: {}'.format(unicode(e))
            return [False, u"Erro ao conectar ao banco de dados!\nErro: {0}".format(unicode(e))]

    def disconnectDB(self):
        try:
            if not self.__conn is None:
                self.__conn.close()
                self.__conn.closed = True
                self.__conn = None
            return [True, u'Desconectado com sucesso!']
        except Exception, e:
            return [False, u'Erro ao desconectar banco de dados!\nErro: {0}'.format(unicode(e))]

    def command(self, sql, params):
        try:
            if params:
                self.__cursorCommand.execute(sql)
            else:
                self.__cursorCommand.execute(sql, params)
            self.__conn.commit()
            return [True, u'Comando executado com successo!']
        except Exception, e:
            return [False, u'Erro executar Comando!\nSQL: {0}\nErro: {1}'.format(sql, unicode(e))]

    def query(self, sql, params=None):
        cursorQuery = self.__conn.cursor()
        try:
            if params:
                cursorQuery.execute(sql, params)
            else:
                cursorQuery.execute(sql)
            return [True, cursorQuery]
        except Exception, e:
            return [False, u'Erro executar consulta!\nSQL: {0}\nErro: {1}'.format(sql, unicode(e))]
