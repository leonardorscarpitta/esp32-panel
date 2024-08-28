import requests
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from dotenv import load_dotenv

def clearCmd():
    os.system("clear")


# Clear terminal screen
clearCmd()
# Load dot env to use ambient variables
load_dotenv()

# Global variables for lamp ID and IP address
lampId = os.getenv("LAMPID")
IP = os.getenv("IP")

def testConnection(IP):
    """
    Test the connection to the IoT device by sending a GET request to the specified IP address.

    Args:
        IP (str): The IP address of the IoT device.

    Returns:
        None
    """
    try:
        url = f"http://{IP}:4041/iot/about"
        payload = {}
        headers = {}

        # Send GET request to the IoT device
        response = requests.get(url, headers=headers, data=payload)
        response_json = response.json()
        versionAppeared = response_json.get("version")

        # Check if the response contains the expected version
        if versionAppeared in response.text:
            input("✅ Connection established successfully! Press any key to return to the main page.")
        
    except:
        print("ERROR 404")


def deleteSmartLamp(IP, lampId):
    """
    Delete a smart lamp by sending a DELETE request to the specified IP address.

    Args:
        IP (str): The IP address of the IoT device.
        lampId (str): The ID of the lamp to be deleted.

    Returns:
        None
    """
    url = f"http://{IP}:4041/iot/devices/lamp:{lampId}"

    payload = {}
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }

    # Send DELETE request to remove the lamp
    response = requests.delete(url, headers=headers, data=payload)

    if response.text.strip() == "":
        input("Lamp deleted successfully! Press any key to return to the main page.")


def checkLedStatus(IP, lampId) -> str:
    """
    Check the status of the LED by sending a GET request and retrieving the LED's value.

    Args:
        IP (str): The IP address of the IoT device.
        lampId (str): The ID of the lamp.

    Returns:
        str: The LED status value.
    """
    clearCmd()
    url = f'http://{IP}:1026/v2/entities/urn:ngsi-ld:Lamp:{lampId}/attrs/state'

    payload = {}
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/',
        'accept': 'application/json'
    }

    # Send GET request to retrieve the LED status
    response = requests.get(url, headers=headers, data=payload)
    response_json = response.json()
    led_value = response_json.get("value")

    return led_value


def provisionSmartLamp(IP, lampId) -> str:
    """
    Provision a new smart lamp by sending a POST request to the IoT device.

    Args:
        IP (str): The IP address of the IoT device.
        lampId (str): The ID of the new lamp.

    Returns:
        None
    """
    url = f"http://{IP}:4041/iot/devices"

    payload = json.dumps({
        "devices": [
            {
                "device_id": f"lamp:{lampId}",
                "entity_name": f"urn:ngsi-ld:Lamp:{lampId}",
                "entity_type": "Lamp",
                "protocol": "PDI-IoTA-UltraLight",
                "transport": "MQTT",
                "commands": [
                    {
                        "name": "on",
                        "type": "command"
                    },
                    {
                        "name": "off",
                        "type": "command"
                    }
                ],
                "attributes": [
                    {
                        "object_id": "s",
                        "name": "state",
                        "type": "Text"
                    },
                    {
                        "object_id": "l",
                        "name": "luminosity",
                        "type": "Integer"
                    }
                ]
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }

    # Send POST request to provision the new lamp
    response = requests.post(url, headers=headers, data=payload)

    print(response.text)


def registerLampCommands(IP, lampId) -> str:
    """
    Register commands for the smart lamp by sending a POST request to the IoT device.

    Args:
        IP (str): The IP address of the IoT device.
        lampId (str): The ID of the lamp.

    Returns:
        None
    """
    url = f"http://{IP}:1026/v2/registrations"

    payload = json.dumps({
        "description": "Lamp Commands",
        "dataProvided": {
            "entities": [
                {
                    "id": f"urn:ngsi-ld:Lamp:{lampId}",
                    "type": "Lamp"
                }
            ],
            "attrs": [
                "on",
                "off"
            ]
        },
        "provider": {
            "http": {
                "url": f"http://{IP}:4041"
            },
            "legacyForwarding": True
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }

    # Send POST request to register commands
    response = requests.post(url, headers=headers, data=payload)

    print(response.text)


def searchLamp(IP, lampId):
    url = f"http://{IP}:4041/iot/devices/lamp{lampId}"

    payload = ""
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    input(response.text)


def changeLedStatus(IP, lampId, status):
    """
    Change the LED status by sending a PATCH request to the IoT device.

    Args:
        IP (str): The IP address of the IoT device.
        lampId (str): The ID of the lamp.
        status (str): The desired status ("on" or "off").

    Returns:
        None
    """
    execute = "on" if status == "OFF" else "off"
    url = f"http://{IP}:1026/v2/entities/urn:ngsi-ld:Lamp:{lampId}/attrs"

    if status == "on":
        payload = json.dumps({
            "off": {
                "type": "command",
                "value": ""
            }
        })
    else:
        payload = json.dumps({
            "on": {
                "type": "command",
                "value": ""
            }
        })
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.text)


time_data = []
luminosity_data = [1]
def collect_luminosity_data(IP, lampId, collectN = 8):
    """
    Coleta informações sobre a luminosidade da lâmpada e gera um gráfico em tempo real.

    Args:
        IP (str): O endereço IP do dispositivo IoT.
        lampId (str): O ID da lâmpada.

    Returns:
        None
    """
    time_data.clear()
    luminosity_data.clear()

    url = f"http://{IP}:1026/v2/entities/urn:ngsi-ld:Lamp:{lampId}/attrs/luminosity"

    payload = {}
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/',
        'accept': 'application/json'
    }

    # Data for the graphic

    for _ in range(collectN):  # Collect data in a number defined by de user
        response = requests.get(url, headers=headers, data=payload)
        response_json = response.json()
        luminosity = response_json.get("value")
        current_time = datetime.now()

        time_data.append(current_time)
        luminosity_data.append(luminosity)

    # Creating graphic
    plt.figure()
    plt.plot(time_data, luminosity_data, marker='o')
    plt.title(f"Luminosity Data Over Time - [{lampId}]")
    plt.xlabel("Time")
    plt.ylabel("Luminosity")
    plt.grid(True)

    # Saving the graphic in a file
    plt.savefig('luminosity_graph.png')
    print("Gráfico salvo como 'luminosity_graph.png'.")

def main():
    # Run luminosity data at least once
    print("Starting the program and collecting luminosity data...")
    status = collect_luminosity_data(IP, lampId)
    # Main program loop
    while True:
        clearCmd()
        ledStatus = checkLedStatus(IP, lampId)
        avgLuminosity = round(sum(luminosity_data) / len(luminosity_data), 3)
        print(f"💡 Average luminosity - {avgLuminosity}")
        print(f"🆔 Lamp ID - Lamp:{lampId}")
        print(f"🌐 Connected IPv4 - {IP}")
        print("==========*==========")
        print("""
    ___                         _____         _     
    |_ _|_ __   _____   ____ _  |_   _|__  ___| |__  
    | || '_ \ / _ \ \ / / _` |   | |/ _ \/ __| '_ \ 
    | || | | | (_) \ V / (_| |   | |  __/ (__| | | |
    |___|_| |_|\___/ \_/ \__,_|   |_|\___|\___|_| |_|
    """)
        print("==========*==========")
        print("[0] - Test your connection")
        print("[1] - Current status of your led")
        print("[2] - Delete a smart lamp")
        print("[3] - Provision a new Smart Lamp")
        print("[4] - Register Lamp Commands")
        print("[5] - Search for your lamp")
        print("[6] - Change LED status")
        print("[7] - Generate a graphic")
        print("==========*==========")
        option = int(input("Select an option - "))

        # Handle user input
        match option:
            case 0:
                testConnection(IP)
            case 1:
                input(f"🔦 Current status of your LED - {checkLedStatus(IP, lampId).upper()}")
            case 2:
                deleteSmartLamp(IP, lampId)
            case 3:
                provisionSmartLamp(IP, lampId)
            case 4:
                registerLampCommands(IP, lampId)
            case 5:
                searchLamp(IP, lampId)
            case 6:
                changeLedStatus(IP, lampId, ledStatus)
            case 7:
                collectN = int(input("Number of data collections (1/s)"))
                print(f"Collecting data in {collectN} cycles!")
                collect_luminosity_data(IP, lampId, collectN)
            case _:
                clearCmd()
                print("Invalid option!")
                break

if __name__ == "__main__":
    main()
