"""Divide CSV com todos os DOs em um por dia"""

import os
import csv

csv.field_size_limit(100000000)

PASTA = "../temporario/"
ordem = ("ID","Data","Retranca","Tipo do Conteúdo","Secretaria","Orgão","Texto")
docs_por_dia = {}

os.system("rm -f %spordia/*" % PASTA)
with open(PASTA+'saida2.csv', newline='') as csvfile:
    leitor = csv.DictReader(csvfile, dialect='unix')
    escritos = []
    data_anterior = None
    arq_csv = None
    for linha in leitor:
        data = linha["Data"][:10]

        if not data in docs_por_dia:
            docs_por_dia[data]=0
        docs_por_dia[data]+=1
        linha["ID"]=data[0:4]+"/"+data[5:7]+"/"+data[8:10]+"/"+str(docs_por_dia[data])

        if data_anterior == data:
            escritor.writerow(linha)
        else:
            if arq_csv:
                arq_csv.close()
            data_anterior = data
            nome_arq = "%spordia/%s.csv" % (PASTA, data)
            arq_csv = open(nome_arq, 'a')
            escritor = csv.DictWriter(arq_csv, ordem, dialect='unix')
            if data not in escritos:
                escritos.append(data)
                escritor.writeheader()
            escritor.writerow(linha)
