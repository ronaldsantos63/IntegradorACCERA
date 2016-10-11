#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    clientes                                                    
# Criado em: 04 de Agosto de 2016 as 14:01         
# ----------------------------------------------------------------------

from utils.funcoes import valida_cnpj, valida_cpf, remove_letras, remove_caracteres_especiais, strftime, strToDate, strIsDate
from datetime import datetime


class ClienteCabecalho(object):
    def __init__(self):
        super(ClienteCabecalho, self).__init__()
        self.__tipo_registro = 'H'
        self.__distribuidor_cod = None
        self.__data_arquivo = None

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
    def data_arquivo(self):
        return self.__data_inicial

    @data_arquivo.setter
    def data_arquivo(self, value):
        if value is None or (not isinstance(value, datetime) and not strIsDate(value)):
            raise ValueError("Data do arquivo nao eh uma data valida!")
        else:
            if not isinstance(value, unicode) or not isinstance(value, str):
                self.__data_arquivo = strftime(value, '%Y%m%d', True)
            else:
                self.__data_arquivo = strftime(strToDate(value), '%Y%m%d', True)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2}\n".format(
                self.__tipo_registro, self.__distribuidor_cod, self.__data_arquivo
        )


class ClienteDados(object):
    def __init__(self):
        super(ClienteDados, self).__init__()
        self.__tipo_registro = 'V'
        self.__cpf_cnpj = None
        self.__razao_social = None
        self.__fantasia = None
        self.__pais = None
        self.__regiao = ''
        self.__estado = None
        self.__cidade = None
        self.__bairro = None
        self.__endereco = None
        self.__grupo_rede = ""
        self.__pdv_classificacao = ""
        self.__vendedor_nome = None
        self.__data_cadastro = None
        self.__pdv_cep = None
        self.__contato_email = ""
        self.__status = None  # Valores aceitos A - Ativo | I - Inativo

    @property
    def cpf_cnpj(self):
        return self.__cpf_cnpj

    @cpf_cnpj.setter
    def cpf_cnpj(self, value):
        if value is None or (not valida_cpf(unicode(value)) and not valida_cnpj(unicode(value))):
            raise ValueError('O CPF/CNPJ informado nao eh um valido!\nCPF/CNPJ informado: {}'.format(value))
        else:
            self.__cpf_cnpj = remove_letras(value, True)

    @property
    def razao_social(self):
        return self.__razao_social

    @razao_social.setter
    def razao_social(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError("Razao Social nao pode ser vazio!")
        else:
            self.__razao_social = remove_caracteres_especiais(value)

    @property
    def fantasia(self):
        return self.__fantasia

    @fantasia.setter
    def fantasia(self, value):
        if value is None or unicode(value).strip() == '':
            self.__fantasia = ''
        else:
            self.__fantasia = remove_caracteres_especiais(value)

    @property
    def pais(self):
        return self.__pais

    @pais.setter
    def pais(self, value):
        if value is None or unicode(value).strip() == '':
            self.__pais = 'BRA'
        else:
            self.__pais = value.upper()

    @property
    def regiao(self):
        return self.__regiao

    @regiao.setter
    def regiao(self, value):
        if value is None or unicode(value).strip() == '':
            self.__regiao = ''
        else:
            self.__regiao = remove_caracteres_especiais(value)

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError("A UF Informada nao eh valida!")
        else:
            self.__estado = value

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError("A Cidade informada nao eh valida!")
        else:
            self.__cidade = remove_caracteres_especiais(value)

    @property
    def bairro(self):
        return self.__bairro

    @bairro.setter
    def bairro(self, value):
        if value is None or unicode(value).strip() == "":
            raise ValueError("Bairro informado nao eh valido!")
        else:
            self.__bairro = remove_caracteres_especiais(value)

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, value):
        if value is None or unicode(value).strip() == "":
            raise ValueError("Endereco informado nao eh valido!")
        else:
            self.__endereco = remove_caracteres_especiais(value).replace(";", " ")

    @property
    def grupo_rede(self):
        return self.__grupo_rede

    @grupo_rede.setter
    def grupo_rede(self, value):
        if value is None or unicode(value).strip() == '':
            self.__grupo_rede = ""
        else:
            self.__grupo_rede = remove_caracteres_especiais(value)

    @property
    def pdv_classificacao(self):
        return self.__pdv_classificacao

    @pdv_classificacao.setter
    def pdv_classificacao(self, value):
        if value is None or unicode(value).strip() == "":
            self.__pdv_classificacao = ""
        else:
            self.__pdv_classificacao = remove_caracteres_especiais(value)

    @property
    def vendedor_nome(self):
        return self.__vendedor_nome

    @vendedor_nome.setter
    def vendedor_nome(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError("Nome do Vendedor eh invalido!")
        else:
            self.__vendedor_nome = remove_caracteres_especiais(value)

    @property
    def data_cadastro(self):
        return self.__data_cadastro

    @data_cadastro.setter
    def data_cadastro(self, value):
        if value is None or (not strIsDate(value) and not isinstance(value, datetime)):
            raise ValueError("Data do cadastro nao eh uma data valida!\nData informada: {}".format(value))
        else:
            if isinstance(value, unicode) or isinstance(value, str):
                self.__data_cadastro = strftime(strToDate(value)[1], '%Y%m%d', True)
            else:
                self.__data_cadastro = strftime(value, '%Y%m%d', True)

    @property
    def pdv_cep(self):
        return self.__pdv_cep

    @pdv_cep.setter
    def pdv_cep(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("Cep informado nao eh valido!")
        else:
            self.__pdv_cep = remove_letras(value, True)

    @property
    def contato_email(self):
        return self.__contato_email

    @contato_email.setter
    def contato_email(self, value):
        if value is None or unicode(value).strip() == "":
            self.__contato_email = ""
        else:
            self.__contato_email = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in ('A', "I"):
            raise ValueError("Status informado nao eh valido!\nValores validos [ A; I ]\nValor informado: {}",
                             format(value))
        else:
            self.__status = value

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15};{16}\n".format(
                self.__tipo_registro, self.__cpf_cnpj, self.__razao_social, self.__fantasia,
                self.__pais, self.__regiao, self.__estado, self.__cidade, self.__bairro,
                self.__endereco, self.__grupo_rede, self.__pdv_classificacao, self.__vendedor_nome,
                self.__data_cadastro, self.__pdv_cep, self.__contato_email, self.__status
        )


class ClienteRodape(object):
    def __init__(self):
        super(ClienteRodape, self).__init__()
        self.__tipo_registro = "E"

    @property
    def linha_formatada(self):
        return u"{0}\n".format(self.__tipo_registro)
