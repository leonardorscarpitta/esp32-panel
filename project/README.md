# ESP32: Coletor de Luminosidade

## Resumo do projeto
Esse projeto foi desenvolvido em C++

## Dependencias
- Máquina virtual, recomenda-se o uso da [Microsoft Azure](https://azure.microsoft.com/en-us) ou [AWS](https://aws.amazon.com/);
- ESP32;
- 4x Cabos Jumpers;
- LDR;

## Manual de Instalação
1. Instale o [Arduino IDE](https://www.arduino.cc/en/software/) em sua máquina
2. Realize o download das bibliotecas necessárias ibliotecas no Arduino: 
```
pip install requests matplotlib datetime python-dotenv
```
3. Crie um arquivo `config.h` dentro da pasta do projeto para que você possa configurar o IP usado, ID da lâmpada e a Rede Wi-Fi.
3.1 Utilize os seguintes parâmetros:
```
#ifndef CONFIG_H
#define CONFIG_H

#define SSID "" // Nome da rede Wi-Fi
#define PASSWORD "" // Senha da rede Wi-Fi
#define BROKER_MQTT "" // IP para conexão com o broker MQTT
#define LAMPID "001" // ID da lâmpada

#endif
```