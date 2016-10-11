#!/usr/bin/env python
# encoding: utf-8
# ----------------------------------------------------------------------
# Autor:     ronald                                                    
# Projeto:   IntegradorACCERA                                            
# Modulo:    funcoes                                                    
# Criado em: 04 de Agosto de 2016 as 14:39         
# ----------------------------------------------------------------------

import warnings
import re
from datetime import datetime
from collections import OrderedDict
from decimal import Decimal

__author__ = 'ronald'


def isDecimal(dados):
    if dados is None or str(dados).strip() == "":
        return False

    if not isinstance(dados, Decimal) and not isinstance(dados, float):
        try:
            dados = float(dados)
        except:
            return False

        return True
    elif isinstance(dados, Decimal):
        return True
    elif isinstance(dados, float):
        return True
    else:
        return False


def isEmail(dados):
    if dados is None or str(dados).strip() == "":
        return False
    dados = str(dados).strip()
    expressao = "^[a-zA-Z0-9][a-zA-Z0-9\\._-]+@([a-zA-Z0-9\\._-]+\\.)[a-zA-Z-0-9]{2,3}"
    if re.match(expressao, dados):
        return True
    else:
        return False


def remove_letras(dados, remove_ponto=False):
    if dados is None or str(dados).strip() == "":
        return 0
    if remove_ponto:
        new = re.sub("[^\d]", "", str(dados))
    else:
        new = re.sub("[^\d\.]", "", str(dados))
    return new


def remove_caracteres_especiais(texto=unicode):
    """
    Funcao que remove caracteres especiais
    :param texto:
    :return:
    """
    tabela = {
        u'Ã?': 'C', u'�': ' ', u'': ' ',
        u"Á": "A", u"Â": "A", u"À": "A", u"Ã": "A",
        u"É": "E", u"È": "E", u"Ê": "E",
        u"Í": "I", u"Ì": "I", u"Î": "I",
        u"Ó": "O", u"Ò": "O", u"Ô": "O", u"Õ": "O",
        u"Ú": "U", u"Ù": "U", u"Û": "U",
        u"Ç": "C", "'": " ", '"': " ", u"º": " ",
        u"ª": " ", u"¨": " ", u"^": " ", u"~": " ",
        "\n": " ", "\n\r": " ", u"´": " ", u"1": "1",
        u"²": "2", u"³": "3", u"?": " "
    }
    texto = texto.upper()

    for key in tabela.keys():
        texto = texto.replace(key, tabela[key])

    while texto.__contains__("  "):
        texto = texto.replace("  ", " ")

    texto = texto.strip()
    return texto


def strIsDate(date=str):
    '''
    Funcao que verifica se a string e uma data valida

    :param date: String a ser validado
    :return: True se a data for valida e False se a data for invalida

    >>> def f(date=str):
    ...     return strIsDate(date)
    >>> f('25/09/1993')#doctest:+NORMALIZE_WHITESPACE
    True
    >>> f('1993/09/25')#doctest:+NORMALIZE_WHITESPACE
    True
    >>> f('')#doctest:+NORMALIZE_WHITESPACE
    False
    >>> f('adsd')#doctest:+NORMALIZE_WHITESPACE
    False
    >>> f(None)#doctest:+NORMALIZE_WHITESPACE
    False
    >>> f()#doctest:+NORMALIZE_WHITESPACE
    False
    '''
    try:
        datetime.strptime(date, '%d/%m/%Y')
        return True
    except:
        try:
            datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
            return True
        except:
            try:
                datetime.strptime(date, '%Y/%m/%d')
                return True
            except:
                try:
                    datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                    return True
                except:
                    try:
                        datetime.strptime(date, '%d-%m-%Y')
                        return True
                    except:
                        try:
                            datetime.strptime(date, '%d-%m-%Y %H:%M:%S')
                            return True
                        except:
                            try:
                                datetime.strptime(date, '%Y-%m-%d')
                                return True
                            except:
                                try:
                                    datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                                    return True
                                except:
                                    return False


def strToDate(date=str):
    try:
        tmp = datetime.strptime(date, '%d/%m/%Y')
        return [True, tmp]
    except:
        try:
            tmp = datetime.strptime(date, '%Y/%m/%d')
            return [True, tmp]
        except:
            return [False, datetime.now()]


class Specifier(str):
    """Model %Y and such in `strftime`'s format string."""

    def __new__(cls, *args):
        self = super(Specifier, cls).__new__(cls, *args)
        assert self.startswith('%')
        assert len(self) == 2
        self._regex = re.compile(r'(%*{0})'.format(str(self)))
        return self

    def ispresent_in(self, format):
        m = self._regex.search(format)
        return m and m.group(1).count('%') & 1  # odd number of '%'

    def replace_in(self, format, by):
        def repl(m):
            n = m.group(1).count('%')
            if n & 1:  # odd number of '%'
                prefix = '%' * (n - 1) if n > 0 else ''
                return prefix + str(by)  # replace format
            else:
                return m.group(0)  # leave unchanged

        return self._regex.sub(repl, format)


def strftime(datetime_, format, force=False):
    """`strftime()` that works for year < 1900.

    Disregard calendars shifts.

    >>> def f(fmt, force=False):
    ...     return strftime(datetime(1895, 10, 6, 11, 1, 2), fmt, force)
    >>> f('abc %Y %m %D')
    'abc 1895 10 10/06/95'
    >>> f('%X')
    '11:01:02'
    >>> f('%c') #doctest:+NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ValueError: '%c', '%x' produce unreliable results for year < 1900
    use force=True to override
    >>> f('%c', force=True)
    'Sun Oct  6 11:01:02 1895'
    >>> f('%x') #doctest:+NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ValueError: '%c', '%x' produce unreliable results for year < 1900
    use force=True to override
    >>> f('%x', force=True)
    '10/06/95'
    >>> f('%%x %%Y %Y')
    '%x %Y 1895'
    """
    year = datetime_.year
    if year >= 1900:
        return datetime_.strftime(format)

    # make year larger then 1900 using 400 increment
    assert year < 1900
    factor = (1900 - year - 1) // 400 + 1
    future_year = year + factor * 400

    assert future_year >= 1900

    format = Specifier('%Y').replace_in(format, year)
    result = datetime_.replace(year=future_year).strftime(format)
    if any(f.ispresent_in(format) for f in map(Specifier, ['%c', '%x'])):
        msg = "'%c', '%x' produce unreliable results for year < 1900"
        if not force:
            raise ValueError(msg + " use force=True to override")
        warnings.warn(msg)
        result = result.replace(str(future_year), str(year))
    assert (future_year % 100) == (year % 100)  # last two digits are the same
    return result


def valida_cpf(cpf=str):
    cpf = re.sub('[^\\d]', '', str(cpf))
    if len(cpf) != 11 or cpf == "00000000000" or cpf == "11111111111" or cpf == "22222222222" or \
                    cpf == "33333333333" or cpf == "44444444444" or cpf == "55555555555" or cpf == "66666666666" or \
                    cpf == "77777777777" or cpf == "88888888888" or cpf == "99999999999":
        return False
    else:
        result = 0
        cont = 0
        while cont < 9:
            result += int(cpf[cont]) * (10 - cont)
            cont += 1

        rev = 11 - (result % 11)
        if rev == 10 or rev == 11:
            rev = 0
        if rev != int(cpf[9]):
            return False

        cont = 0
        result = 0
        while cont < 10:
            result += int(cpf[cont]) * (11 - cont)
            cont += 1

        rev = 11 - (result % 11)
        if rev == 10 or rev == 11:
            rev = 0
        if rev != int(cpf[10]):
            return False

        return True


def valida_cnpj(cnpj=str):
    cnpj = re.sub('[^\\d]', '', str(cnpj))
    if len(cnpj) != 14 or cnpj == "00000000000000" or cnpj == "11111111111111" or cnpj == "22222222222222" or \
                    cnpj == "33333333333333" or cnpj == "44444444444444" or cnpj == "55555555555555" or \
                    cnpj == "66666666666666" or cnpj == "77777777777777" or cnpj == "88888888888888" or \
                    cnpj == "99999999999999":
        return False
    else:
        n = [int(i) for i in cnpj[:-2]]
        m = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        dv1 = int(cnpj[-2:][0])
        dv2 = int(cnpj[-2:][1])

        result = 0
        for index, num in enumerate(n):
            result += num * m[index]

        resto = result % 11
        if resto < 2:
            if dv1 != 0:
                return False
        else:
            if resto < 11:
                if dv1 != int(11 - resto):
                    return False
            else:
                if dv1 != int(resto - 11):
                    return False

        m.insert(0, 6)
        n.append(dv1)

        result = 0
        for index, num in enumerate(n):
            result += num * m[index]

        resto = result % 11
        if resto < 2:
            if dv2 != 0:
                return False
        else:
            if resto < 11:
                if dv2 != int(11 - resto):
                    return False
            else:
                if dv2 != int(resto - 11):
                    return False
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod()
