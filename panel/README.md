# ESP32: Painel de Controle

## Resumo do projeto
Esse projeto foi desenvolvido em Python com o objetivo de controlar os dispositivos Smart desenvolvidos a princípio para o controle de luminosidade de um ambiente, contendo funções como gerador de gráficos para análise do parâmetro de luminosidade, alteração do status do LED do ESP32 e o registro de um dispositivo novo.

## Bibliotecas necessarias
- `matplotlib` para a geração de gráficos;
- `datetime` para o registro de horário e data em que as informações foram coletadas;
- `python-dotenv` para a configuração de variáveis de ambiente;
- `requests` para o tratamento de requisições e dados em json;

## Manual de Instalação
1. Instale o [Python](https://www.python.org/) em sua máquina.
2. Crie um arquivo `.env` dentro da pasta do projeto para que você possa configurar o IP usado e o ID da lâmpada.
3. Realize o download das bibliotecas necessárias ibliotecas do Python necessárias.
4. Rode o código utilizando uma [IDE](https://pt.wikipedia.org/wiki/Ambiente_de_desenvolvimento_integrado) ou o terminal de sua preferencia.

## Parâmetros para configuração do arquivo .env

```
LAMPID=""
IP=""
```