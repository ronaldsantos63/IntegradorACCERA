#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    vendas                                                    
# Criado em: 04 de Agosto de 2016 as 14:00         
# ----------------------------------------------------------------------

from datetime import datetime

from utils.funcoes import remove_letras, isDecimal, strIsDate, strftime, strToDate, remove_caracteres_especiais


class VendasCabecalho(object):
    def __init__(self):
        super(VendasCabecalho, self).__init__()
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


class VendasDados(object):
    def __init__(self):
        self.__tipo_registro = 'V'
        self.__cd_loja_cod = None
        self.__fornecedor_cod = None
        self.__produto_barras = None
        self.__lote_numero = ''
        self.__lote_data_validade = ''
        self.__saida_quantidade = None  # A quantidade deve ser multiplicada por 1000
        self.__valor_unitario = None  # Valor final da transacao (Valor do produto + impostos) na nota fiscal, ja com desconto subtraido deve ser multiplicado por 100
        self.__moeda = 'BRL'
        self.__transacao_identificador = None  # Numero da Nota fiscal[Venda, devolucao, transferencia, etc...]
        self.__transacao_data = None
        self.__transacao_tipo = None  # V - Venda | DV - Devolucao | C - Cancelamento | B - Bonificacao | T - Transferencia | P - Pedido | Toda devolucao ou cancelamento deve ter o registro de transacao originaria
        self.__cfop = None
        self.__pdv_identificador_tipo = None  # "1" - CPF | "2" - CNPJ
        self.__pdv_identificador = None  # CPF ou CNPJ de acordo com o tipo informado
        self.__pdv_descricao = None  # Razao social do distribuidor
        self.__pdv_cep = None  # Somente numeros
        self.__pdv_classificacao = None
        self.__vendedor_nome = None  # Na ausencia do vendedor preencher com a razao social da empresa
        self.__campo_livre1 = None  # Nome que define o que sera enviado no campo livre
        self.__campo_livre2 = None  # Nome que define o que sera enviado no campo livre

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
    def saida_quantidade(self):
        return self.__saida_quantidade

    @saida_quantidade.setter
    def saida_quantidade(self, value):
        if value is None or (not isDecimal(value) and not remove_letras(value, True).isdigit()):
            raise ValueError('Quantidade informada nao eh um numero valido!\nQuantidade: {}'.format(value))
        else:
            self.__saida_quantidade = int(value) * 1000

    @property
    def valor_unitario(self):
        return self.__valor_unitario

    @valor_unitario.setter
    def valor_unitario(self, value):
        if value is None or (not isDecimal(value) and not remove_letras(value, True).isdigit()):
            raise ValueError('Valor informado da unidade nao eh valida!\nValor: {}'.format(value))
        else:
            self.__valor_unitario = int(value * 100)

    @property
    def transacao_identificador(self):
        return self.__transacao_identificador

    @transacao_identificador.setter
    def transacao_identificador(self, value):
        if value is None or (not remove_letras(value, True).isdigit()):
            raise ValueError('Identificador informado nao eh um numero valido!\nIdentificador: {}'.format(value))
        else:
            self.__transacao_identificador = int(value)

    @property
    def transacao_data(self):
        return self.__transacao_data

    @transacao_data.setter
    def transacao_data(self, value):
        if value is None or not strIsDate(unicode(value)):
            raise ValueError("Data da transacao nao eh uma valida!Data: {}".format(value))
        else:
            if not isinstance(value, unicode) and not isinstance(value, str):
                self.__transacao_data = strftime(value, '%Y%m%d', True)
            else:
                value = strToDate(value)[1]
                self.__transacao_data = strftime(value, '%Y%m%d', True)

    @property
    def transacao_tipo(self):
        return self.__transacao_tipo

    @transacao_tipo.setter
    def transacao_tipo(self, value):
        if unicode(value).upper() not in ('V', 'DV', 'C', 'B', 'T', 'P'):
            raise ValueError(
                    "Tipo de transacao informado nao eh valido!\nTipos validos: ['P', 'DV', 'C', 'B', 'T', 'P']\nTipo informado: {}".format(
                            value))
        else:
            self.__transacao_tipo = value.upper()

    @property
    def cfop(self):
        return self.__cfop

    @cfop.setter
    def cfop(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("O CFOP informado nao eh um numero valido!\nCFOP informado: {}".format(value))
        else:
            self.__cfop = remove_letras(value, True)[:-1]

    @property
    def pdv_identificador_tipo(self):
        return self.__pdv_identificador_tipo

    @pdv_identificador_tipo.setter
    def pdv_identificador_tipo(self, value):
        if value not in ('1', '2'):
            raise ValueError("Tipo de identificacao PDV nao eh valido!\nTipos validos: ['1', '2']\nTipo informado: {}".format(value))
        else:
            self.__pdv_identificador_tipo = value

    @property
    def pdv_identificador(self):
        return self.__pdv_identificador

    @pdv_identificador.setter
    def pdv_identificador(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("CPF/CNPJ do cliente nao eh valido!\nCPF/CNPJ passado: {}".format(value))
        else:
            self.__pdv_identificador = remove_letras(value, True)

    @property
    def pdv_descricao(self):
        return self.__pdv_descricao

    @pdv_descricao.setter
    def pdv_descricao(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError("Descricao do PDV nao pode ser vazio!")
        else:
            self.__pdv_descricao = remove_caracteres_especiais(value)

    @property
    def pdv_cep(self):
        return self.__pdv_cep

    @pdv_cep.setter
    def pdv_cep(self, value):
        if value is None or not remove_letras(value, True).isdigit():
            raise ValueError("Cep do PDV informado nao eh valido!\nCep informado: {}".format(value))
        else:
            self.__pdv_cep = remove_letras(value, True)

    @property
    def pdv_classificacao(self):
        return self.__pdv_classificacao

    @pdv_classificacao.setter
    def pdv_classificacao(self, value):
        if value is None:
            self.__pdv_classificacao = ''
        else:
            self.__pdv_classificacao = value

    @property
    def vendedor_nome(self):
        return self.__vendedor_nome

    @vendedor_nome.setter
    def vendedor_nome(self, value):
        if value is None or unicode(value).strip() == '':
            raise ValueError("Nome do vendedor nao pode ser vazio!")
        else:
            self.__vendedor_nome = value

    @property
    def campo_livre1(self):
        return self.__campo_livre1

    @campo_livre1.setter
    def campo_livre1(self, value):
        if value is None or unicode(value).strip() == '':
            self.__campo_livre1 = ''
        else:
            self.__campo_livre1 = remove_caracteres_especiais(value)

    @property
    def campo_livre2(self):
        return self.__campo_livre1

    @campo_livre2.setter
    def campo_livre2(self, value):
        if value is None or unicode(value).strip() == '':
            self.__campo_livre2 = ''
        else:
            self.__campo_livre2 = remove_caracteres_especiais(value)

    @property
    def linha_formatada(self):
        return u"{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15};{16};{17};{18};{19};{20}\n".format(
            self.__tipo_registro, self.__cd_loja_cod, self.__fornecedor_cod, self.__produto_barras, self.__lote_numero,
            self.__lote_data_validade, self.__saida_quantidade, self.__valor_unitario, self.__moeda,
            self.__transacao_identificador, self.__transacao_data, self.__transacao_tipo, self.__cfop,
            self.__pdv_identificador_tipo, self.__pdv_identificador, self.__pdv_descricao, self.__pdv_cep,
            self.__pdv_classificacao, self.__vendedor_nome, self.__campo_livre1, self.__campo_livre2
        )


class VendasRodape(object):
    def __init__(self):
        super(VendasRodape, self).__init__()
        self.__tipo_registro = 'E'

    @property
    def linha_formatada(self):
        return "{0}\n".format(self.__tipo_registro)