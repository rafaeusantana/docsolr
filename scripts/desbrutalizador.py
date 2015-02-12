#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------


import os
import sys
import shutil
import csv
import errno
import subprocess
import retrancas
from datetime import timedelta, date


MSG_AJUDA = """
Processa os TXTs (com os textos dos artigos dos Diários Oficiais) dentro dos
ZIPs disponibilizados pela prefeitura convertendo-os em CSVs.

USO:
script.py <dir_destino> <itens_origem>+

dir_destino: diretório onde irão os CSVs gerados.
itens_origem: zips "brutos", ou diretórios com zips. Os dois últimos caracteres
do nome das pastas contendo os zips devem ser o número do ano dos zips contidos
nela.
"""

UM_DIA = timedelta(days=1)
csv.field_size_limit(100000000)
ORDEM = ("ID",
         "Data",
         "Retranca",
         "Tipo do Conteúdo",
         "Secretaria",
         "Orgão",
         "Texto")

# ----------------------------------------------------------------------------
# CUIDADO! ESSE DIRETÓRIO SERÁ REMOVIDO! (várias vezes...)
DIR_TEMP = os.path.join("/", "tmp", "diarios_temp")
# ----------------------------------------------------------------------------


def verifica_zip(arq):
    """Retorna True se o arquivo parece ser um ZIP, False caso contrário"""
    return arq.lower()[-4:] == ".zip"


def listar_zips_na_origem(itens_origem):
    zips = []
    for item in itens_origem:
        # Se é um diretório
        if os.path.isdir(item):
            for raiz, dirs, arqs in os.walk(item):
                for arq in arqs:
                    caminho_arq = os.path.join(raiz, arq)
                    if verifica_zip(caminho_arq):
                        zips.append(caminho_arq)
        # Se é um arquivo
        else:
            zips.append(item)
    return zips


def obter_data_zip(zip):
    # Obtém ano a partir do nome da pasta do ZIP
    caminho_zip = os.path.abspath(zip)
    try:
        ano = int("20" + os.path.dirname(caminho_zip)[-2:])
    except ValueError:
        print("Nome da pasta não termina com ano!:", caminho_zip)
        exit()

    # Obtém mês e dia a partir do nome do ZIP
    nome_zip = os.path.basename(zip)
    try:
        dia = int(nome_zip[0:2])
        mes = int(nome_zip[2:4])
    except ValueError:
        print("Nome do zip não começa com dia e mês!:", nome_zip)
        exit()

    # Adiciona um dia, pois os ZIPs são guardados no dia anterior à publicação
    return date(ano, mes, dia) + UM_DIA


def converter_nome_zip_csv(zip):
    return obter_data_zip(zip).strftime('%Y-%m-%d') + ".csv"


def excluir_zips_processados(zips, dir_destino):
    zips_faltantes = []
    csvs = os.listdir(dir_destino)
    for zip in zips:
        csv = converter_nome_zip_csv(zip)
        if csv not in csvs:
            zips_faltantes.append(zip)
    return zips_faltantes


def criar_dir_temp():
    try:
        os.makedirs(DIR_TEMP)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            print("Erro ao tentar criar diretório temporário!")
            exit()


def processar_zips(zips, dir_destino):
    for zip in zips:
        processar_zip(zip, dir_destino)


def descompactar_zip(zip):
    # os.system("unzip -nqq %s -d %s" % (zip, DIR_TEMP))
    os.system('7z x -o%s %s | grep -v "^Extracting  "' % (DIR_TEMP, zip))


def verifica_txt(arq):
    s = ['file', '-bi', arq]
    tipo = str(subprocess.check_output(s), 'utf8').partition(';')[0]
    return tipo == 'text/plain'


def limpa_nome_txt(nome):
    if nome[2] == '.':
        nome = nome.partition('.')[2]
    # Tira espaços do nome do arquivo
    return nome.replace(' ', '')


def decodificar_nome_txt(nome):
    retranca = nome[0:7].lower()
    # Verifica se está na tabela especial
    achou = retrancas.RETRANCAS_ESP.get(retranca)
    if achou:
        secretaria, orgao = achou
    else:
        # Verifica se está na tabela normal
        publicante = retranca[1:7]
        achou = retrancas.RETRANCAS.get(publicante)
        if not achou:
            secretaria, orgao = '-', '-'
            print('ERRO SECR ORG', retranca, nome)
        else:
            secretaria, orgao = achou

    # Tipo de Conteúdo
    tipo_letra = retranca[0:1]
    conteudo = retrancas.CONTEUDOS.get(tipo_letra)
    if not conteudo:
        conteudo = '-'
        print('ERRO CONTEUDO', tipo_letra, nome)

    return {
        'Tipo do Conteúdo': conteudo,
        'Secretaria': secretaria,
        'Orgão': orgao,
        'Retranca': retranca,
    }


def processar_zip(zip, dir_destino):
    print("Processando:", zip)

    try:
        shutil.rmtree(DIR_TEMP)
    except FileNotFoundError:
        pass
    criar_dir_temp()

    descompactar_zip(zip)

    data = obter_data_zip(zip)
    data_solr = data.strftime('%Y-%m-%dT00:00:00Z')
    data_id = data.strftime('%Y/%m/%d/')

    nome_csv = converter_nome_zip_csv(zip)
    caminho_csv_temp = os.path.join(DIR_TEMP, nome_csv)
    arq_csv = open(caminho_csv_temp, 'w')
    escritor = csv.DictWriter(arq_csv, ORDEM, dialect='unix')
    escritor.writeheader()

    txts_processados = 0
    for raiz, dirs, arqs in os.walk(DIR_TEMP):
        for arq in arqs:
            caminho_arq = os.path.join(raiz, arq)
            if verifica_txt(caminho_arq):
                dados = extrair_dados_txt(caminho_arq)
                if dados:
                    dados['Data'] = data_solr
                    dados['ID'] = data_id + str(txts_processados)
                    escritor.writerow(dados)
                    txts_processados += 1

    arq_csv.close()
    caminho_csv = os.path.join(dir_destino, nome_csv)
    if txts_processados > 0:
        shutil.move(caminho_csv_temp, caminho_csv)
        if txts_processados < 40:
            print("Apenas %s TXTs foram processados neste ZIP. Estranho..." %
                  txts_processados)
    else:
        print("Nenhum TXT foi processado!")

    shutil.rmtree(DIR_TEMP)


def ler_txt_hostil(caminho_txt):
    codificacoes = [
        'utf-8',
        'latin_1',
        'utf_16',
        'cp1250',
    ]
    for codificacao in codificacoes:
        arq = open(caminho_txt, "r", encoding=codificacao)
        try:
            texto = arq.read()
            arq.close()
            return texto
        except UnicodeDecodeError:
            arq.close()
    print('Erro ao Decodificar TXT!', caminho_txt)
    return None


def extrair_dados_txt(caminho_txt):
    nome_limpo = limpa_nome_txt(os.path.basename(caminho_txt))
    if ('ALHAU.' not in nome_limpo) and \
       ('logfechamento' not in nome_limpo.lower()):
        texto = ler_txt_hostil(caminho_txt)
        if texto:
            dados = decodificar_nome_txt(nome_limpo)
            dados['Texto'] = texto
            return dados
    return None

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(MSG_AJUDA)
    else:
        dir_destino = sys.argv[1]
        itens_origem = sys.argv[2:]
        zips = listar_zips_na_origem(itens_origem)
        zips_faltantes = excluir_zips_processados(zips, dir_destino)
        if zips_faltantes:
            processar_zips(zips_faltantes, dir_destino)
        else:
            print("Nenhum zip novo para ser processado...")
            exit(4)
