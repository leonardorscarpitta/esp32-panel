//Autor Rev3: Fábio Henrique Cabrini
//Devidas modificações realizadas por Leonardo Rocha Scarpitta
#include <WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>
#include "config.h"
#include "DHT.h"

DHT dht(4, DHT22);
// LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

// Configurações - variáveis editáveis
const char* default_SSID = SSID; // Nome da rede Wi-Fi
const char* default_PASSWORD = PASSWORD; // Senha da rede Wi-Fi
const char* default_BROKER_MQTT = BROKER_MQTT; // IP do Broker MQTT
const int default_BROKER_PORT = 1883; // Porta do Broker MQTT
const char* default_TOPICO_SUBSCRIBE = "/TEF/lamp" + LAMPID + "001/cmd"; // Tópico MQTT de escuta
const char* default_TOPICO_PUBLISH_1 = "/TEF/lamp" + LAMPID + "/attrs"; // Tópico MQTT de envio de informações para Broker
const char* default_TOPICO_PUBLISH_2 = "/TEF/lamp" + LAMPID + "/attrs/l"; // Tópico MQTT de envio de informações para Broker
const char* default_ID_MQTT = "fiware_" + LAMPID; // ID MQTT
const int default_D4 = 2; // Pino do LED onboard
// Declaração da variável para o prefixo do tópico
const char* topicPrefix = "lamp" + LAMPID;

// Variáveis para configurações editáveis
char* SSID = const_cast<char*>(default_SSID);
char* PASSWORD = const_cast<char*>(default_PASSWORD);
char* BROKER_MQTT = const_cast<char*>(default_BROKER_MQTT);
int BROKER_PORT = default_BROKER_PORT;
char* TOPICO_SUBSCRIBE = const_cast<char*>(default_TOPICO_SUBSCRIBE);
char* TOPICO_PUBLISH_1 = const_cast<char*>(default_TOPICO_PUBLISH_1);
char* TOPICO_PUBLISH_2 = const_cast<char*>(default_TOPICO_PUBLISH_2);
char* ID_MQTT = const_cast<char*>(default_ID_MQTT);
int D4 = default_D4;

WiFiClient espClient;
PubSubClient MQTT(espClient);
char EstadoSaida = '0';

/*
byte customChars[8][8] = {
  { B00000, B01000, B01111, B01011, B01011, B00011, B00011, B00011 }, // cima1
  { B00000, B01011, B11011, B01011, B01101, B00101, B00001, B00001 }, // cima2
  { B00000, B00000, B10000, B11000, B11101, B10101, B10101, B10111 }, // cima3
  { B00000, B00110, B01110, B11110, B11100, B01100, B01100, B01100 }, // cima4
  { B00011, B00011, B00011, B01011, B01011, B01111, B01000, B00000 }, // baixo1
  { B00001, B00001, B00101, B01101, B01001, B11011, B00110, B00000 }, // baixo2
  { B10111, B10010, B10010, B10000, B10000, B11000, B00000, B00000 }, // baixo3
  { B01100, B01100, B01100, B01100, B01100, B11110, B00011, B00000 }  // baixo4
};

void showLogo() {
  lcd.begin(16, 2);
  for (int i = 0; i < 8; i++) {
    lcd.createChar(i, customChars[i]);
    lcd.setCursor(6 + (i % 4), i / 4); // Definir cursor baseado na posição de cima ou baixo
    lcd.write(byte(i));
  }

  delay(5000);
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("Innovation");
  lcd.setCursor(4, 1);
  lcd.print("Masters");
  delay(2000);
  lcd.clear();
}
*/

void initSerial() {
    Serial.begin(115200);
}

void initWiFi() {
    delay(10);
    Serial.println("------Conexao WI-FI------");
    Serial.print("Conectando-se na rede: ");
    Serial.println(SSID);
    Serial.println("Aguarde");
    reconectWiFi();
}

void initMQTT() {
    MQTT.setServer(BROKER_MQTT, BROKER_PORT);
    MQTT.setCallback(mqtt_callback);
}

void initDHT() {
    dht.begin();
}

void setup() {
    // showLogo();
    InitOutput();
    initSerial();
    initWiFi();
    initMQTT();
    initDHT();
    delay(5000);
    MQTT.publish(TOPICO_PUBLISH_1, "s|on");
}

void loop() {
    Serial.println("-----=()=-----");
    VerificaConexoesWiFIEMQTT();
    EnviaEstadoOutputMQTT();
    handleUmidityTemperature();
    handleLuminosity();
    MQTT.loop();
}

void reconectWiFi() {
    if (WiFi.status() == WL_CONNECTED)
        return;
    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(100);
        Serial.print(".");
    }
    Serial.println();
    Serial.println("Conectado com sucesso na rede ");
    Serial.print(SSID);
    Serial.println("IP obtido: ");
    Serial.println(WiFi.localIP());

    // Garantir que o LED inicie desligado
    digitalWrite(D4, LOW);
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
    String msg;
    for (int i = 0; i < length; i++) {
        char c = (char)payload[i];
        msg += c;
    }
    Serial.print("- Mensagem recebida: ");
    Serial.println(msg);

    // Forma o padrão de tópico para comparação
    String onTopic = String(topicPrefix) + "@on|";
    String offTopic = String(topicPrefix) + "@off|";

    // Compara com o tópico recebido
    if (msg.equals(onTopic)) {
        digitalWrite(D4, HIGH);
        EstadoSaida = '1';
    }

    if (msg.equals(offTopic)) {
        digitalWrite(D4, LOW);
        EstadoSaida = '0';
    }
}

void VerificaConexoesWiFIEMQTT() {
    if (!MQTT.connected())
        reconnectMQTT();
    reconectWiFi();
}

void EnviaEstadoOutputMQTT() {
    if (EstadoSaida == '1') {
        MQTT.publish(TOPICO_PUBLISH_1, "s|on");
        Serial.println("- Led Ligado");
    }

    if (EstadoSaida == '0') {
        MQTT.publish(TOPICO_PUBLISH_1, "s|off");
        Serial.println("- Led Desligado");
    }
    Serial.println("- Estado do LED onboard enviado ao broker!");
    delay(1000);
}

void InitOutput() {
    pinMode(D4, OUTPUT);
    digitalWrite(D4, HIGH);
    boolean toggle = false;

    for (int i = 0; i <= 10; i++) {
        toggle = !toggle;
        digitalWrite(D4, toggle);
        delay(200);
    }
}

void reconnectMQTT() {
    while (!MQTT.connected()) {
        Serial.print("* Tentando se conectar ao Broker MQTT: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT)) {
            Serial.println("Conectado com sucesso ao broker MQTT!");
            MQTT.subscribe(TOPICO_SUBSCRIBE);
        } else {
            Serial.println("Falha ao reconectar no broker.");
            Serial.println("Haverá nova tentativa de conexão em 2s");
            delay(2000);
        }
    }
}

void handleUmidityTemperature() {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Check if any reads failed and exit early (to try again).
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }

    Serial.print(F("- Humidade: "));
    Serial.print(humidity);
    Serial.print(F("%"));
    Serial.println();
    Serial.print(F("- Temperatura: "));
    Serial.print(temperature);
    Serial.println(F("°C "));

    // Wait a few seconds between measurements.
    delay(2000);
}

void handleLuminosity() {
    const int potPin = 34;
    int sensorValue = analogRead(potPin);
    int luminosity = map(sensorValue, 0, 4095, 0, 100);
    String mensagem = String(luminosity);
    Serial.print("Valor da luminosidade: ");
    Serial.println(mensagem.c_str());
    MQTT.publish(TOPICO_PUBLISH_2, mensagem.c_str());
}
