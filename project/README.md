# ESP32: Coletor de Luminosidade

## Resumo do projeto
Esse projeto foi desenvolvido em C++ para coletar a umidade, temperatura e luminosidade de um ambiente de adega de vinhos monitorado com o objetivo de garantir a qualidade máxima da bebida.

## Dependencias
- Máquina virtual, recomenda-se o uso da [Microsoft Azure](https://azure.microsoft.com/en-us) ou [AWS](https://aws.amazon.com/);
- ESP32;
- 1x display LCD 16x2; 
- 1x DHT22;
- 3x Resistores;
- LDR;
- 3x Leds (Vermelho, Amarelo e Verde);
- 3x Resistores (≈ 3,15Ω);
- 1x Buzzer
- **Média de** 20x Cabos Jumpers (Dependerá de qual DHT, LDR e Display LCD serão usados);

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