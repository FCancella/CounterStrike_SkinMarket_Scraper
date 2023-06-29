# CounterStrike Skin Market Scraper - Dash x BUFF163  
## Objetivo:
O objetivo principal deste código é identificar e aproveitar as melhores oportunidades de negociação de skins no mercado nacional de Counter-Strike. Para isso, o código busca as melhores ofertas dentro da plataforma brasileira [Dash Skins](dashskins.com.br) e compara com o mercado global representado pelo site chinês, [BUFF163](buff.163.com).

O código visa facilitar o processo de "transportar" dinheiro do mercado nacional para o mercado global, buscando lucros por meio do spread, e permitindo aos usuários tirarem proveito das vantagens oferecidas por um mercado mais amplo, com uma oferta maior.
  
## História:
Este código foi desenvolvido com o objetivo de identificar as melhores oportunidades de negociação de skins no mercado de CS:GO, aproveitando a diferença de preços entre a plataforma brasileira Dash Skins e o mercado global representado pelo serviço Buff.163.

No mercado nacional de skins de CS:GO, embora seja significativo, a oferta de produtos e os preços baixos são limitados quando comparados ao mercado global. Atualmente, a Dash Skins é o único site brasileiro que permite aos usuários anunciar seus itens por qualquer preço desejado, oferecendo um ambiente de "livre mercado". Por outro lado, o Buff.163 é reconhecido como o maior mercado global de skins, especialmente aquecido no mercado chinês. No entanto, o Buff aceita apenas pagamentos nacionais chineses, impossibilitando transações diretas de usuários estrangeiros.

Diante desse cenário, surgiu a ideia de adquirir skins na Dash Skins e vendê-las no Buff para aproveitar as vantagens oferecidas por um mercado global. Durante essa operação, notei que alguns itens na Dash Skins estavam com preços mais baixos em relação ao Buff. A fimde explorar esse "spread", e identificar as melhores ofertas, comeceio desenvolvimento deste código em conjunto com o ChatGPT.

A escolha de utilizar o ChatGPT para desenvolver este projeto teve dois propósitos: avaliar sua eficiência na colaboração com um ser humano e testar a viabilidade de programar utilizando bibliotecas com aa quais eu não possuía conhecimento prévio.

Com base em conhecimentos em HTML, CSS e Python, consegui criar toda a lógica necessária para realizar o web scraping dos dados, evitando erros e bloqueios durante o processo. O ChatGPT desempenhou um papel fundamental no projeto, uma vez que sem ele qualquer um seria incapaz de aprender o suficiente de BeautifulSoup e selenium a fim realizar este projeto. Em vários momentos, a IA foi capaz de fornecer soluções para problemas encontrados, como a necessidade de suporte para JavaScript, que foi resolvida com a transição para o Selenium.

Com todos os aspectos discutidos e as dúvidas esclarecidas, foi possível programar em conjunto com o ChatGPT um modelo extremamente útil para a finalidade deste projeto.

## Lógica e Especificações:
Para coletar os dados dos produtos na Dash Skins, utilizei a biblioteca BeautifulSoup. Através da análise do HTML da página, é possível extrair informações como nome e preço dos itens anunciados.

Em seguida, procuro o preço desses mesmos produtos no Buff.163, e como a plataforma não permite acesso direto a usuários não logados, contornei essa restrição utilizando o site csgoskins.gg, que fornece informações sobre preços de itens anunciados no Buff.

Com todos os dados coletados, aplico filtros com base em parâmetros como o valor do spread e número de ofertas, armazenando as informações em um DataFrame e exibindo-as no terminal.

## Uso:
1. Clone o repositório e instale as dependências necessárias.
2. Execute o código alterando os parametros, se necessario.  
   - Preco Min./Max. de busca ([aqui](https://github.com/FCancella/CounterStrike_SkinMarket_Scraper/blob/7769895304e5847b966cabab530212e616ad761e/dashXbuff_v3.py#L69))  
   - Numero de paginas ([aqui](https://github.com/FCancella/CounterStrike_SkinMarket_Scraper/blob/7769895304e5847b966cabab530212e616ad761e/dashXbuff_v3.py#L68C1-L68C1))  
   - Filtros das ofertas ([aqui](https://github.com/FCancella/CounterStrike_SkinMarket_Scraper/blob/7769895304e5847b966cabab530212e616ad761e/dashXbuff_v3.py#L149))  
3. Analise os resultados exibidos no terminal, que mostrarão as melhores oportunidades de negociação encontradas (Compra e Venda). 

## Alternativa de uso:
1. Entre na pasta [executavel](https://github.com/FCancella/CounterStrike_SkinMarket_Scraper/tree/main/executavel) e faça o download do programa
  
## Contato:
Para mais informações ou dúvidas sobre este projeto, entre em contato através do email: cancellacdc@gmail.com.  

### Aprimoramentos, sugestões e contribuições são bem-vindos!
