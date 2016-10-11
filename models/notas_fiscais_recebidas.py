#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    notas_fiscais_recebidas                                                    
# Criado em: 04 de Agosto de 2016 as 14:01         
# ----------------------------------------------------------------------

from datetime import datetime

from utils.funcoes import remove_letras, isDecimal, strIsDate, strftime, strToDate, remove_caracteres_especiais


class NFRCabecalho(object):
    def __init__(self):
        super(NFRCabecalho, self).__init__()
        self.__tipo_registro = 'H'
        self.__distribuidor_cod = None
        self.__data_inicial = None  # Menor data
        self.__data_final = None  # Data maior saida

    @property
    def distribuidor_cod(self):
        return self.__distribuidor_cod

    @distribuidor_cod.setter
    def distribuidor_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError('Codigo do Distribuidor invalido!\nCod: {0}'.format(value))
        else:
            self.__distribuidor_cod = remove_letras(value, True)

    @property
    def data_inicial(self):
        return self.__data_inicial

    @data_inicial.setter
    def data_inicial(self, value):
        if value is None or (not isinstance(value, datetime) and not strIsDate(value)):
            raise ValueError("Data inicial da saida nao eh uma data valida!")
        else:
            if not isinstance(value, unicode) or not isinstance(value, str):
                self.__data_inicial = strftime(value, '%Y%m%d', True)
            else:
                self.__data_inicial = strftime(strToDate(value), '%Y%m%d', True)

    @property
    def data_final(self):
        return self.__data_final

    @data_final.setter
    def data_final(self, value):
        if value is None or (not isinstance(value, datetime) and not strIsDate(value)):
            raise ValueError("Data inicial da saida nao eh uma data valida!")
        else:
            if not isinstance(value, unicode) or not isinstance(value, str):
                self.__data_final = strftime(value, '%Y%m%d', True)
            else:
                self.__data_final = strftime(strToDate(value), '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3}\n".format(
            self.__tipo_registro, self.__distribuidor_cod, self.__data_inicial, self.__data_final
        )


class NFRDados(object):
    def __init__(self):
        super(NFRDados, self).__init__()
        self.__tipo_registro = "V"
        self.__fornecedor_cod = None
        self.__nf_numero = None
        self.__nf_acao = None  # Valores validos [ R=>Retornado | E=>Entregue ]
        self.__nf_valor = None  # Deve ser enviado sem separador Decimal e multiplicado por 100 ex: valor: 300.40, 300.40 * 100 = 30040.0 = 30040
        self.__nf_quantidade = None  # Deve ser multiplicado por 1000 e deve conter somente unidades sem quebras
        self.__nf_acao_data = None  # O mesmo que data da emissao
        self.__nf_data_entrada = None  # Data que o produto entrou no estoque

    @property
    def fornecedor_cod(self):
        return self.__fornecedor_cod

    @fornecedor_cod.setter
    def fornecedor_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("Codigo do Fornecedor e invalido!\nCod: {}".format(value))
        else:
            self.__fornecedor_cod = remove_letras(value, True)

    @property
    def nf_numero(self):
        return self.__nf_numero

    @nf_numero.setter
    def nf_numero(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("Numero da Nota Fiscal nao eh valida!\nNumero informado: {}".format(value))
        else:
            self.__nf_numero = int(value)

    @property
    def nf_acao(self):
        return self.__nf_acao

    @nf_acao.setter
    def nf_acao(self, value):
        if unicode(value).upper() not in ('E', 'R'):
            raise ValueError("Acao da NFe informada nao esta entre os valores validos [E, R]!\nValor informado: {}".format(value))
        else:
            self.__nf_acao = value.upper()

    @property
    def nf_valor(self):
        return self.__nf_valor

    @nf_valor.setter
    def nf_valor(self, value):
        if value is None or not isDecimal(value):
            raise ValueError("O valor da NFe informada nao eh valido!\nValor informado: {}".format(value))
        else:
            self.__nf_valor = int(value * 100)

    @property
    def nf_quantidade(self):
        return self.__nf_quantidade

    @nf_quantidade.setter
    def nf_quantidade(self, value):
        if value is None or (not isDecimal(value) and not remove_letras(value, True).isdigit()):
            raise ValueError("O quantidade da NFe informada nao eh valida!\nValor informado: {}".format(value))
        else:
            self.__nf_quantidade = int(value) * 1000

    @property
    def nf_acao_data(self):
        return self.__nf_acao_data

    @nf_acao_data.setter
    def nf_acao_data(self, value):
        if value is None or not strIsDate(unicode(value)):
            raise ValueError("Data da Emissao da Nfe nao eh uma valida!Data: {}".format(value))
        else:
            if not isinstance(value, unicode) and not isinstance(value, str):
                self.__nf_acao_data = strftime(value, '%Y%m%d', True)
            else:
                value = strToDate(value)[1]
                self.__nf_acao_data = strftime(value, '%Y%m%d', True)

    @property
    def nf_data_entrada(self):
        return self.__nf_data_entrada

    @nf_data_entrada.setter
    def nf_data_entrada(self, value):
        if value is None or not strIsDate(unicode(value)):
            raise ValueError("Data da transacao nao eh uma valida!Data: {}".format(value))
        else:
            if not isinstance(value, unicode) and not isinstance(value, str):
                self.__nf_data_entrada = strftime(value, '%Y%m%d', True)
            else:
                value = strToDate(value)[1]
                self.__nf_data_entrada = strftime(value, '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3};{4};{5};{6};{7}\n".format(
            self.__tipo_registro, self.__fornecedor_cod, self.__nf_numero,
            self.__nf_acao, self.__nf_valor, self.__nf_quantidade,
            self.__nf_acao_data, self.__nf_data_entrada
        )


class NFRRodape(object):
    def __init__(self):
        super(NFRRodape, self).__init__()
        self.__tipo_registro = 'E'

    @property
    def linha_formatada(self):
        return u"{0}\n".format(self.__tipo_registro)