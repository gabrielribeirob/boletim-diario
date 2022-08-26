# Boletim diário da B3
 Coleta informações advindas do Boletim Diário da B3, disponível em: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/boletim-diario-do-mercado/

 ## Descrição
 O presente código faz um scrap baseado na url de download dos capítulos disponibilizados no Boletim Diário da B3. Uma vez baixados, os arquivos (que estão em formato pdf) são parseados e deles são extraidas tabelas que ficam salvas em formato DataFrame Os dados ali disponíveis são de acesso público e fazem parte do serviço de dados da B3.

 A primeira parte do código é o Scraper, que baixa e salva os arquivos em uma pasta destino.
 Já a segunda, possui o parseador de pdf's, extraindo deles as informações mais relevantes (baseada no arquivo de prospecção disponível no BaseCamp) e retornando dataframes com as tabelas respectivas. 
