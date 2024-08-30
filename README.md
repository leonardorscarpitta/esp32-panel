# ESP32: Painel de Controle

## Resumo do projeto
Esse projeto foi desenvolvido em Python com o objetivo de controlar os dispositivos Smart desenvolvidos a princípio para o controle de luminosidade de um ambiente, contendo funções como gerador de gráficos para análise do parâmetro de luminosidade, alteração do status do LED do ESP32 e o registro de um dispositivo novo.

## Manual de Instalação
1. Instale o [Python](https://www.python.org/) em sua máquina
2. Realize o download das bibliotecas necessárias ibliotecas do Python necessárias: 
```
pip install matplotlib datetime python-dotenv
```
2.1 `matplotlib` para a geração de gráficos;
2.2 `datetime` para o registro de horário e data em que as informações foram coletadas;
2.3 `python-dotenv` para a configuração de variáveis de ambiente;
3. Crie um arquivo `.env` dentro da pasta do projeto para que você possa configurar o IP usado e o ID da lâmpada.
3.1 Utilize os seguintes parâmetros:
```
LAMPID=""
IP=""
```
4. Execute o código e aproveite as funções.