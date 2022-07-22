from datetime import datetime, timedelta
import lxml, requests, os, tabula


class BoletimDiario():
    def __init__(self, capitulo='resumo', date=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')) -> None:
        """_summary_

        Args:
            capitulo (str, optional): capitlo a ser requisitado. Opções possíveis:
            a) resumo;
            b) maiores_oscilacoes;
            c) after_market;
            Defaults como 'resumo'.
            date (str, optional): colocar data em formato YYYY/MM/DD;
            Defaults como datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'), que implica o dia anterior ao da requisição.
        """
        self.dicio          = {
            'resumo'            : 'BDI_01_',
            'maiores_oscilacoes': 'BDI_01-1_',
            'after_market'      : 'BDI_03-3_',
            'url_base'          : 'https://up2dataweb.blob.core.windows.net/bdi/'
        }
        self.date            = date
        self.capitulo        = capitulo
        self.capitulo_codigo = self.dicio[f'{self.capitulo}']
        self.folder_name     = self._folder_name()
        if  self.folder_name not in os.listdir():
            self._create_folder
        
    #---------------------------------------------------------------------------------------------
    # Seção do Scraper
    #---------------------------------------------------------------------------------------------
    def get_request(self, url:str):
        """_summary_

        Args:
            url (str): Url do pdf que será baixado

        Returns:
            <class 'requests.models.Response'>: resposta da requisição
        """
        r = requests.get(url)
        return r


    def _create_url(self):
        """Cria a url para download do pdf. 

        Returns:
            str: url para download da informação específica
        """
        date = self.date.replace('/','').replace('-','')
        base = str(self.dicio['url_base'])
        return base+self.capitulo_codigo+date+'.pdf'

    
    def _folder_name(self):
        """Cria o nome do path para a pasta que receberá o download do pdf.

        Returns:
            str: string com o nome do path para a pasta.
        """
        path    = os.getcwd()
        folder  = str(path) + '\\' + str('Boletim_Diario') + '_' + str(self.capitulo).capitalize() + '_' + str(self.date)
        return folder
    
    @staticmethod
    def _create_folder(self):
        """Cria uma pasta para receber o download do pdf.
        """
        folder  = self._folder_name()
        return os.mkdir(folder)
    

    def download_pdf(self):
        folder   = self._folder_name()
        response = self.get_request(self._create_url())
        with open(os.path.join(folder,self.capitulo)+str('.pdf'), "wb") as file:
            file.write(response.content)
    
    #---------------------------------------------------------------------------------------------
    # Seção do Parseador
    #---------------------------------------------------------------------------------------------
    def get_resumo_info(self):
        """Faz o parseamento do pdf de resumos extraindo as informações das tabelas: 
        1) Derivativos Médias Diárias de Contratos Negociados;
        2) Ações Médias Diárias de Negociação;
        Returns:
            tuple: Tupla com 2 DataFrames:
            0    : DataFrame com informações relativas aos derivativos;
            1    : DataFrame com informações relativas às ações.
        """
        path_resumo = os.path.join(self._folder_name(),self.capitulo)+str('.pdf')
        tabela      = tabula.read_pdf(path_resumo,pages=1)
        # Ações
        acoes       = tabela[0][['Unnamed: 1', 'Número de negócios', 'Volume (R$) Milhões']]
        # Derivativos
        derivativos = tabela[0][['Unnamed: 0', 'Total com minis', 'Total sem minis']]
        return derivativos, acoes
    

    def get_maiores_oscilacoes_info(self):
        """Faz o parseamento do pdf de maiores oscilações, extraindo as informações das tabelas:
        1) Ações do IBOVESPA - Maiores Altas;
        2) Ações do IBOVESPA - Maiores Baixas.

        Returns:
            tuple: Tupla com 2 DataFrames:
            0    : DataFrame com informações relativas às maiores altas da bolsa no dia;
            1    : DataFrame com informações relativas às maiores baixas da bolsa no dia.
        """
        path_oscilacoes        = os.path.join(self._folder_name(),self.capitulo)+str('.pdf')
        tabela_page_1          = tabula.read_pdf(path_oscilacoes,pages=1)
        tabela_page_2          = tabula.read_pdf(path_oscilacoes,pages=2)
        # Ações do IBOVESPA - Maiores Altas
        ibovespa_maiores_altas = tabela_page_1[0][['Ação', 'Unnamed: 0', 'Unnamed: 1', 'Preço (R$)', 'Oscilação (%)']]
        # Ações do IBOVESPA - Maiores Baixas
        ibovespa_maiores_baixas = tabela_page_1[0][['Ação.1', 'Unnamed: 2', 'Unnamed: 3', 'Preço (R$).1', 'Oscilação (%).1']]
        return ibovespa_maiores_altas, ibovespa_maiores_baixas



