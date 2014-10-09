README
======

Para deixar esta aplicação funcionando, siga os seguintes passos:


**Instalar o Ruby on Rails**

Para o desenvolvimento desta aplicação foram utilizadas as seguintes versões de software:

Versão do Ruby: 2.1.2

Versão do Rails: 4.1.2


**Configuração**

- Crie um diretório com todo o conteúdo deste repositório.

- Rode o seguinte código na linha de comando:

```
cd (diretório da aplicação)
bundle install
rake db:migrate
```

- Para alterar a porta que dá acesso ao Solr (por padrão 8080), altere
os arquivos solr.yml e jetty.yml do diretório conf.


**Inicialização**

Depois de rodar o seguinte código na linha de comando:

```
cd (diretório da aplicação)
rails s
```

Você poderá acessar o site em http://localhost:3000.

***Atenção!!!:*** Caso você vá rodar o código em produção dessa forma, não esqueça de alterar as senhas no arquivo **config/secrets.yml** conforme as instruções no mesmo.


**Configurações do Solr**

Os arquivos armazenados no diretório files_solr deste repositório devem
ser colocados na pasta base do solr (no ubuntu /usr/share/solr).


**Indexação de conteúdo**

Para indexar o CSV com o conteúdo dos DOCs, basta utilizar a api do Solr:

http://localhost:8080/solr/docsolr/update/csv?stream.file=/home/rafa/Downloads/saidas/saida001.csv&commit=true&header=true&fieldnames=id,data,retranca,tipo_conteudo,secretaria,orgao,texto&stream.contentType=text/csv;charset=utf-8

- Se o arquivo não possui o nome dos campos, então header=false.

- id e não ID (isso ajudou na integração com a biblioteca Blacklight).

- Pelos meus testes iniciais, consegui indexar um arquivo de dezenas de mb desta forma, então é
recomendável criar vários arquivos de no máximo algumas dezenas de mb e indexá-los através da api do solr.


