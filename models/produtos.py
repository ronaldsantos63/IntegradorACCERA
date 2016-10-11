#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    produtos                                                    
# Criado em: 04 de Agosto de 2016 as 13:59         
# ----------------------------------------------------------------------

from utils.funcoes import remove_letras, remove_caracteres_especiais, strftime
from datetime import datetime


class ProdutosCabecalho(object):
    def __init__(self):
        super(ProdutosCabecalho, self).__init__()
        self.__tipo_registro = 'H'
        self.__cod_distribuidor = None
        self.__data_criacao_arquivo = None

    @property
    def cod_distribuidor(self):
        return self.__cod_distribuidor

    @cod_distribuidor.setter
    def cod_distribuidor(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError(u'Código do distribuidor inválido!\nCod: {}'.format(value))
        else:
            self.__cod_distribuidor = remove_letras(value, True)

    @property
    def data_criacao_arquivo(self):
        return self.__data_criacao_arquivo

    @data_criacao_arquivo.setter
    def data_criacao_arquivo(self, value):
        if value is None or not isinstance(value, datetime):
            raise ValueError(u'Data de Criação inválida!\nData informada: {}'.format(value))
        else:
            self.__data_criacao_arquivo = strftime(value, '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2}\n".format(self.__tipo_registro, self.__cod_distribuidor, self.__data_criacao_arquivo)


class ProdutosDados(object):
    def __init__(self):
        super(ProdutosDados, self).__init__()
        self.__tipo_registro = 'V'
        self.__fornecedor_cod = None
        self.__fornecedor_descricao = None
        self.__produto_cod = None
        self.__produto_descricao = None
        self.__grupo_cod = 'NI'
        self.__grupo_descricao = 'NI'
        self.__familia_cod = ''
        self.__familia_descricao = ''
        self.__subfamilia_cod = ''
        self.__subfamilia_descricao = ''
        self.__tipo_cod_barras = 'E'
        self.__cod_barras = ''
        self.__tipo_embalagem_venda = ''
        self.__unidade_produto = 'UN'
        self.__volume_embalagem_venda = 1000  # O volume eh qtd_unidade * 1000! ex: qtd_unidade = 2 = 2 * 1000 = 2000
        self.__status_produto = ''  # I = Inativo, A = Ativo
        self.__data_cadastro = ''

    @property
    def fornecedor_cod(self):
        return self.__fornecedor_cod

    @fornecedor_cod.setter
    def fornecedor_cod(self, value):
        if value is None or unicode(value).strip() == '' or not remove_letras(value, True).isdigit():
            raise ValueError('Codigo do fornecedor invalido!\nCod: {}'.format(value))
        else:
            self.__fornecedor_cod = remove_letras(value, True)

    @property
    def fornecedor_descricao(self):
        return self.__fornecedor_descricao

    @fornecedor_descricao.setter
    def fornecedor_descricao(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError('Descricao do produto invalida!\nDescricao: {}'.format(value))
        else:
            self.__fornecedor_descricao = remove_caracteres_especiais(value)

    @property
    def produto_cod(self):
        return self.__produto_cod

    @produto_cod.setter
    def produto_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError('Codigo produto invalido!\nCod: {}'.format(value))
        else:
            self.__produto_cod = int(value)

    @property
    def produto_descricao(self):
        return self.__produto_descricao

    @produto_descricao.setter
    def produto_descricao(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError('Nome do produto invalido!\nNome: {}'.format(value))
        else:
            self.__produto_descricao = remove_caracteres_especiais(value)

    @property
    def grupo_cod(self):
        return self.__grupo_cod

    @grupo_cod.setter
    def grupo_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError('Codigo Grupo invalido!\nCod: {}'.format(value))
        else:
            self.__grupo_cod = int(value)

    @property
    def grupo_descricao(self):
        return self.__grupo_descricao

    @grupo_descricao.setter
    def grupo_descricao(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError('Nome da Familia invalido!\nNome: {}'.format(value))
        else:
            self.__grupo_descricao = remove_caracteres_especiais(value)

    @property
    def familia_cod(self):
        return self.__familia_cod

    @familia_cod.setter
    def familia_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError('Codigo Familia invalido!\nCod: {}'.format(value))
        else:
            self.__familia_cod = int(value)

    @property
    def familia_descricao(self):
        return self.__familia_descricao

    @familia_descricao.setter
    def familia_descricao(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError('Nome da Familia invalido!\nNome: {}'.format(value))
        else:
            self.__familia_descricao = remove_caracteres_especiais(value)

    @property
    def subfamilia_cod(self):
        return self.__subfamilia_cod

    @subfamilia_cod.setter
    def subfamilia_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError('Codigo SubFamilia invalido!\nCod: {}'.format(value))
        else:
            self.__subfamilia_cod = int(value)

    @property
    def subfamilia_descricao(self):
        return self.__subfamilia_descricao

    @subfamilia_descricao.setter
    def subfamilia_descricao(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError('Nome da SubFmilia invalido!\nNome: {}'.format(value))
        else:
            self.__subfamilia_descricao = remove_caracteres_especiais(value)

    @property
    def cod_barras(self):
        return self.__cod_barras

    @cod_barras.setter
    def cod_barras(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError('Codigo de barras invalido!\nCod: {}'.format(value))
        else:
            self.__cod_barras = int(value)

    @property
    def tipo_embalagem_venda(self):
        return self.__tipo_embalagem_venda

    @tipo_embalagem_venda.setter
    def tipo_embalagem_venda(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError('Tipo de Embalagem invalida!\nTipo: {}'.format(value))
        else:
            self.__tipo_embalagem_venda = remove_caracteres_especiais(value)

    @property
    def volume_embalagem_venda(self):
        return self.__volume_embalagem_venda

    @volume_embalagem_venda.setter
    def volume_embalagem_venda(self, value):
        if value is None:
            raise ValueError("Volume embalagem de Venda informado e invalido!\nVolume: {}".format(value))
        else:
            self.__volume_embalagem_venda = value * 1000

    @property
    def status_produto(self):
        return self.__status_produto

    @status_produto.setter
    def status_produto(self, value):
        if value is None:
            self.__status_produto = 'A'
        else:
            if value == 'S':
                self.__status_produto = 'A'
            elif value == 'N':
                self.__status_produto = 'I'
            else:
                self.__status_produto = 'A'

    @property
    def data_cadastro(self):
        return self.__data_cadastro

    @data_cadastro.setter
    def data_cadastro(self, value):
        if value is None:
            self.__data_cadastro = strftime(datetime.now(), '%Y%m%d', True)
        else:
            self.__data_cadastro = strftime(value, '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15};{16};{17}\n".format(
            self.__tipo_registro, self.__fornecedor_cod, self.__fornecedor_descricao, self.__produto_cod,
            self.__produto_descricao, self.__grupo_cod, self.__grupo_descricao, self.__familia_cod,
            self.__familia_descricao, self.__subfamilia_cod, self.__subfamilia_descricao,
            self.__tipo_cod_barras, self.__cod_barras, self.__tipo_embalagem_venda, self.__unidade_produto,
            self.__volume_embalagem_venda, self.__status_produto, self.__data_cadastro
        )


class ProdutosRodape(object):
    def __init__(self):
        super(ProdutosRodape, self).__init__()
        self.__tipo_registro = 'E'

    @property
    def linha_formatada(self):
        return u'{}\n'.format(self.__tipo_registro)