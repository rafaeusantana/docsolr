PASTA_BRUTOS=/var/www/diarios_brutos
PASTA_CSVS=~/pordia
PASTA_DL=~/docsolr
PASTA_SCRIPTS=$PASTA_DL/scripts
LOGFILE=$PASTA_SCRIPTS/log.log
ANO=$(date +%Y)

#Redireciona saida normal e de erro para terminal atual e LOGFILE
#exec 3>&1 1> >(tee -a $LOGFILE >&3)
#Redireciona saida normal e de erro para LOGFILE
exec 1>>$LOGFILE 2>>$LOGFILE

echo "----------------------------------------"
cd $PASTA_SCRIPTS
date
# rodar_desbrut.sh
python3 desbrutalizador.py $PASTA_CSVS/ $PASTA_BRUTOS/*_${ANO:2:4}
if [ $? -eq 0 ]; then
    # Novos arquivos para processar
    # rodar_index.sh
    python3 indexar.py $PASTA_CSVS
    # rodar_7z.sh
    7z u -up0q0r2x1y2z1w2 -mx=9 $PASTA_DL/public/arquivos-baixar/zips/diarios-$ANO.7z $PASTA_BRUTOS/*_${ANO:2:4}
    7z u -up0q0r2x1y2z1w2 -mx=9 $PASTA_DL/public/arquivos-baixar/zips/diarios-CSV-$ANO.7z $PASTA_CSVS/$ANO*.csv
    python hasher.py $PASTA_DL/public/arquivos-baixar/zips
fi
