#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    cds_lojas                                                    
# Criado em: 04 de Agosto de 2016 as 13:59         
# ----------------------------------------------------------------------
from datetime import datetime
from utils.funcoes import remove_letras, strftime, remove_caracteres_especiais


class CDsLojasCabecalho(object):
    def __init__(self):
        super(CDsLojasCabecalho, self).__init__()
        self.__tipo_registro = 'H'
        self.__distribuidor_cod = None
        self.__data_criacao_arquivo = None

    @property
    def distribuidor_cod(self):
        return self.__distribuidor_cod

    @distribuidor_cod.setter
    def distribuidor_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError(u'Código do distribuidor inválido!\nCod: {}'.format(value))
        else:
            self.__distribuidor_cod = remove_letras(value, True)

    @property
    def data_criacao_arquivo(self):
        return self.__data_criacao_arquivo

    @data_criacao_arquivo.setter
    def data_criacao_arquivo(self, value):
        if value is None or not isinstance(value, datetime):
            raise ValueError(u"Data da criação do arquivo inválido!\nData: {}".format(value))
        else:
            self.__data_criacao_arquivo = strftime(value, '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2}\n".format(self.__tipo_registro, self.__distribuidor_cod, self.__data_criacao_arquivo)


class CDsLojasDados(object):
    def __init__(self):
        super(CDsLojasDados, self).__init__()
        self.__tipo_registro = 'V'
        self.__cd_loja_cod = None
        self.__cd_loja_descricao = None
        self.__cd_loja_uf = None
        self.__cd_loja_cidade = None
        self.__cd_loja_bairro = None
        self.__cd_loja_cep = None
        self.__cd_loja_status = None

    @property
    def cd_loja_cod(self):
        return self.__cd_loja_cod

    @cd_loja_cod.setter
    def cd_loja_cod(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError(u'Código do Centro de Distruição/Loja é inválido!\nCódigo: {}'.format(value))
        else:
            self.__cd_loja_cod = remove_letras(value, True)

    @property
    def cd_loja_descricao(self):
        return self.__cd_loja_descricao

    @cd_loja_descricao.setter
    def cd_loja_descricao(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError(u"Descrição do Centro de Distruição/Loja não pode ser vazio!")
        else:
            self.__cd_loja_descricao = remove_caracteres_especiais(value)

    @property
    def cd_loja_uf(self):
        return self.__cd_loja_uf

    @cd_loja_uf.setter
    def cd_loja_uf(self, value):
        if value is None or unicode(value).strip() == "":
            raise ValueError(u"UF do Centro de Distribuição / Loja não pode ser vazio!")
        else:
            self.__cd_loja_uf = value

    @property
    def cd_loja_cidade(self):
        return self.__cd_loja_cidade

    @cd_loja_cidade.setter
    def cd_loja_cidade(self, value):
        if value is None or unicode(value).strip() == "":
            raise ValueError(u"Cidade do Centro de Distribuição / Loja não pode ser vazio!")
        else:
            self.__cd_loja_cidade = remove_caracteres_especiais(value)

    @property
    def cd_loja_bairro(self):
        return self.__cd_loja_bairro

    @cd_loja_bairro.setter
    def cd_loja_bairro(self, value):
        if value is None or unicode(value).strip() == "":
            raise ValueError(u"Bairro do Centro de Distribuição / Loja não pode ser vazio!")
        else:
            self.__cd_loja_bairro = remove_caracteres_especiais(value)

    @property
    def cd_loja_cep(self):
        return self.__cd_loja_cep

    @cd_loja_cep.setter
    def cd_loja_cep(self, value):
        if value is None or unicode(value).strip() == "":
            raise ValueError(u"Cep do Centro de Distribuição / Loja não pode ser vazio!")
        else:
            self.__cd_loja_cep = remove_letras(value, True)
            
    @property
    def cd_loja_status(self):
        return self.__cd_loja_status
    
    @cd_loja_status.setter
    def cd_loja_status(self, value):
        if value is None or unicode(value).strip() == "":
            raise ValueError(u"Status do Centro de Distribuição / Loja não pode ser vazio!")
        else:
            self.__cd_loja_status = value

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3};{4};{5};{6};{7}\n".format(
            self.__tipo_registro, self.__cd_loja_cod, self.__cd_loja_descricao,
            self.__cd_loja_uf, self.__cd_loja_cidade, self.__cd_loja_bairro,
            self.__cd_loja_cep, self.__cd_loja_status
        )


class CDsLojasRodape(object):
    def __init__(self):
        super(CDsLojasRodape, self).__init__()
        self.__tipo_registro = "E"

    @property
    def linha_formatada(self):
        return u"{0}".format(self.__tipo_registro)