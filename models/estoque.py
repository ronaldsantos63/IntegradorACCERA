#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    estoque                                                    
# Criado em: 04 de Agosto de 2016 as 14:00         
# ----------------------------------------------------------------------

from datetime import datetime
from utils.funcoes import remove_letras, remove_caracteres_especiais, strftime, isDecimal, strIsDate


class EstoqueCabecalho(object):
    def __init__(self):
        super(EstoqueCabecalho, self).__init__()
        self.__tipo_registro = 'H'
        self.__distribuidor_cod = None
        self.__data_inicial = None  # Menor Data de estoque que é contemplada no arquivo
        self.__data_final = None  # Maior Data de estoque que é contemplada no arquivo

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
        if value is None or not isinstance(value, datetime):
            raise ValueError("Data inicial nao e uma data valida!\nData: {}".format(value))
        else:
            self.__data_inicial = strftime(value, '%Y%m%d', True)

    @property
    def data_final(self):
        return self.__data_final

    @data_final.setter
    def data_final(self, value):
        if value is None or not isinstance(value, datetime):
            raise ValueError("Data inicial nao e uma data valida!\nData: {}".format(value))
        else:
            self.__data_final = strftime(value, '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3}\n".format(
                self.__tipo_registro, self.__distribuidor_cod, self.__data_inicial,
                self.__data_final
        )


class EstoqueDados(object):
    def __init__(self):
        super(EstoqueDados, self).__init__()
        self.__tipo_registro = "V"
        self.__cd_loja_cod = None
        self.__fornecedor_cod = None
        self.__produto_barras = None
        self.__lote_numero = ""
        self.__lote_data_validade = ""
        self.__estoque_quantidade = None  # Deve ser multiplicado por 1000
        self.__estoque_tipo = "0"  # Tipos de estoque (H - Estoque físico no estabelecimento | T - Estoque que está chegando no estebelecimento | C - Estoque comprometido para venda futura | H - para estoque negativo)
        self.__estoque_data = None  # Data da posição do estoque

    @property
    def cd_loja_cod(self):
        return self.__cd_loja_cod

    @cd_loja_cod.setter
    def cd_loja_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("Codigo do Centro de Distribuicao / Loja e invalido!\nCod: {}".format(value))
        else:
            self.__cd_loja_cod = remove_letras(value, True)

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
    def produto_barras(self):
        return self.__produto_barras

    @produto_barras.setter
    def produto_barras(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("Codigo de Barras e invalido!\nCod: {}".format(value))
        else:
            self.__produto_barras = int(remove_letras(value, True))

    @property
    def lote_numero(self):
        return self.__lote_numero

    @lote_numero.setter
    def lote_numero(self, value):
        if value is None:
            raise ValueError("Numero do lote nao pode ser vazio!")
        else:
            self.__lote_numero = value

    @property
    def lote_data_validade(self):
        return self.__lote_data_validade

    @lote_data_validade.setter
    def lote_data_validade(self, value):
        if value is None or (not isinstance(value, datetime) and unicode(value).strip() != ''):
            raise ValueError("Data de validade nao e uma data valida!\nData: {}".format(value))
        else:
            if strIsDate(value):
                self.__lote_data_validade = strftime(value, '%Y%m%d', True)
            else:
                self.__lote_data_validade = value

    @property
    def estoque_quantidade(self):
        return self.__estoque_quantidade

    @estoque_quantidade.setter
    def estoque_quantidade(self, value):
        if value is None or (not isDecimal(value) and not remove_letras(value).isdigit()):
            raise ValueError("Quantidade de estoque nao e um numero valido!\nEstoque: {}".format(value))
        else:
            if value < 0:
                self.__estoque_quantidade = 0
            else:
                self.__estoque_quantidade = value * 1000

    @property
    def estoque_tipo(self):
        return self.__estoque_tipo

    @estoque_tipo.setter
    def estoque_tipo(self, value):
        if value not in ("H", "T", "C"):
            raise ValueError(
                    "Tipo de estoque invalido!\nValores validos = ('H', 'T', 'C')\nValor passado = {}".format(
                        value))
        else:
            self.__estoque_tipo = value

    @property
    def estoque_data(self):
        return self.__estoque_data

    @estoque_data.setter
    def estoque_data(self, value):
        if value is None or (not isinstance(value, datetime) and not strIsDate(value)):
            str_erro = "Data da posicao do estoque nao e uma data valida!\nData passada = {}".format(value)
            raise ValueError(str_erro)
        else:
            self.__estoque_data = strftime(value, '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3};{4};{5};{6};{7};{8}\n".format(
                self.__tipo_registro, self.__cd_loja_cod, self.__fornecedor_cod,
                self.__produto_barras, self.__lote_numero, self.__lote_data_validade,
                self.__estoque_quantidade, self.__estoque_tipo, self.__estoque_data
        )


class EstoqueRodape(object):
    def __init__(self):
        super(EstoqueRodape, self).__init__()
        self.__tipo_registro = 'E'

    @property
    def linha_formatada(self):
        return u"{0}\n".format(self.__tipo_registro)
