import os
import subprocess
from datetime import timedelta, date

from contador import Contador


UM_DIA = timedelta(days=1)


def reiniciar_pastas():
    os.system("rm -rf temp pdfs docs outros txts 1erros")
    os.system("mkdir temp pdfs docs outros txts 1erros")

def extrair_artigos_zips(anos):
    for ano in anos:
        print(ano)
        zips = os.listdir(ano)
        Contador.iniciar(len(zips))
        for i, zip in enumerate(zips):
            #print(zip)
            # Obtem mes e dia a partir do nome do ZIP
            dia = zip[0:2]
            mes = zip[2:4]
            try:
                # Adiciona um dia, pois os ZIP são guardados no dia anterior à
                # publicação
                data = date(int(ano), int(mes), int(dia))
                data += UM_DIA
                data_texto = data.strftime('%Y%m%d')

                # Descompacta ZIP
                os.system("unzip -nqq '%s/%s' -d temp" % (ano, zip))

                for caminho in ["temp", "temp/Puclicacao", "temp/Licitacao"]:
                    if os.path.exists(caminho):
                        arqs = os.listdir(caminho)
                        for arq in arqs:
                            if arq not in ["Puclicacao", "Licitacao"]:
                                s = ['file','-bi', '%s/%s' % (caminho, arq)]
                                tipo = str(subprocess.check_output(s),'utf8').partition(';')[0]
                                if arq[2] == '.':
                                    nome_novo = data_texto+arq.partition('.')[2]
                                else:
                                    nome_novo = data_texto+arq
                                # Tira espaços do nome do arquivo
                                nome_novo = nome_novo.replace(' ', '')
                                #print(tipo)
                                if tipo == 'text/plain':
                                    print(caminho, arq, nome_novo)
                                    os.system("mv '%s/%s' 'txts/%s'" % (caminho, arq,
                                                                    nome_novo))
                                elif tipo == 'application/pdf':
                                    os.system("mv '%s/%s' 'pdfs/%s'" % (caminho, arq,
                                                                    nome_novo))
                                elif tipo == 'application/msword':
                                    os.system("mv '%s/%s' 'docs/%s'" % (caminho, arq,
                                                                    nome_novo))
                                else:
                                    os.system("mv '%s/%s' 'outros/%s'" % (caminho, arq,
                                                                      nome_novo))
                Contador.atualizar(i)
            except ValueError:
               os.system("cp %s/%s 1erros" % (ano, zip))




os.chdir('../temporario')
anos = [str(x) for x in range(2003,2015)]
reiniciar_pastas()
extrair_artigos_zips(anos)
