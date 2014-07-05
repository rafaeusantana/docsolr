"""Faz Solr indexar CSVs depois de dividir por dia"""

import os
import subprocess

pasta = "/home/andres/pordia/"

for nome in sorted(os.listdir(pasta)):
	caminho = pasta + nome
	link = " 'http://localhost:8080/solr/docsolr/update/csv?stream.file=%s&commit=true&header=true&fieldnames=id,data,retranca,tipo_conteudo,secretaria,orgao,texto&stream.contentType=text/csv'" % caminho
	r = subprocess.call("curl"+ link, shell=True)
	print(caminho)
	print(r)
