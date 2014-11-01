#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright 2014 Andrés Mantecon Ribeiro Martano & Rafael Santana
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------


import os, sys
import subprocess
import urllib.request


MSG_AJUDA = """
Indexa no Solr os CSVs com os artigos dos Diários Oficiais.

USO:
script.py <dir_csvs>

dir_csvs: Diretório com os CSVs
"""

LINK = 'http://localhost:8080/solr/update/csv?stream.file=%s&commit=true&header=true&fieldnames=id,data,retranca,tipo_conteudo,secretaria,orgao,texto&stream.contentType=text/csv'


def verificar_csvs_indexados(dir_csvs):
    try:
        arq = open(os.path.join(dir_csvs, "INDEXADOS"), 'r')
        indexados = arq.read().splitlines()
        arq.close()
        return indexados
    except FileNotFoundError:
        return []

def registrar_indexado(dir_csvs, nome):
    arq = open(os.path.join(dir_csvs, "INDEXADOS"), 'a')
    print("%s" % nome, file=arq)
    arq.close()

def listar_csvs_dir(dir_csvs):
    return [i for i in os.listdir(dir_csvs) if i[-4:].lower() == ".csv"]

def indexar_csv(caminho_csv):
    print("Indexando", caminho_csv)
    retorno = urllib.request.urlopen(LINK % caminho_csv).read().decode('utf-8')
    if '<int name="status">0</int>' in retorno:
        print("Feito")
        return True
    else:
        print("------------")
        print(retorno)
        print("------------")
        return False

def indexar_faltantes(dir_csvs, indexados):
    for csv in listar_csvs_dir(dir_csvs):
        if csv not in indexados:
            if indexar_csv(os.path.join(dir_csvs, csv)):
                registrar_indexado(dir_csvs, csv)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(MSG_AJUDA)
    else:
        dir_csvs = sys.argv[1]
        indexados = verificar_csvs_indexados(dir_csvs)
        indexar_faltantes(dir_csvs, indexados)
