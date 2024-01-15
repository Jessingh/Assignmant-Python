"""
Author: Jessica Singh
Date:   January/24
Description: This Python script leverages the Flask web framework to create a RESTful API 
             for interacting with Cisco DEVNet SandBox via Netmiko.
"""

# Import necessary modules from Flask and Netmiko libraries
from flask import Flask, request, jsonify
from netmiko import ConnectHandler

# Create a Flask web application
app = Flask(__name__)

# Cisco DevNet Sandbox device details
device_info = {
    'device_type': 'cisco_xr',
    'ip': 'sandbox-iosxr-1.cisco.com',
    'username': 'USER',
    'password': 'PASSWORD',
    'port': 22,  # SSH port
}

# Creates a pathway for handling network interaction via REST POST request
@app.route('/network_interaction', methods=['POST'])
def network_interaction():
    try:
        # Extract data from the incoming request
        data = request.json

        # Assuming data includes information like command to be executed
        command = data.get('command')

        # Interact with the network device using Netmiko
        netmiko_response = send_netmiko_request(device_info, command)

        # Split the netmiko_response into lines
        lines = netmiko_response.split('\n')

        # Remove empty lines
        lines = [line.strip() for line in lines if line.strip()]

        # Create a dictionary with key 'netmiko_response' and value as the lines list
        response_data = {'netmiko_response': lines}

        # Convert the dictionary into a JSON response
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
# Configuring a loopback on the device
@app.route('/configure_loopback', methods=['POST'])
def configure_loopback():
    try:
        # Extract data from the incoming request
        data = request.json

        # Assuming data includes information like loopback_number and ip_address
        loopback_number = data.get('loopback_number')
        ip_address = data.get('ip_address')

        # Configuration command for the loopback interface
        config_commands = [
            f'interface Loopback{loopback_number}',
            f'ip address {ip_address}',
            'commit',  
            'exit'     
        ]

        # Interact with the network device using Netmiko
        netmiko_response = send_netmiko_config(device_info, config_commands)
    
        # Split the netmiko_response into lines
        lines = netmiko_response.split('\n')

        # Remove empty lines
        lines = [line.strip() for line in lines if line.strip()]

        # Create a dictionary with key 'netmiko_response' and value as the lines list
        response_data = {'netmiko_response': lines}

        # Convert the dictionary into a JSON response
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
# Deleting a loopback on the device 
@app.route('/delete_loopback', methods=['POST'])
def delete_loopback():
    try:
        # Extract data from the incoming request
        data = request.json

        # Assuming data includes information like loopback_number
        loopback_number = data.get('loopback_number')

        # Configuration command to delete the loopback interface
        delete_commands = [
            f'no interface Loopback{loopback_number}',
            'commit',  
            'exit'     
        ]

        # Interact with the network device using Netmiko
        netmiko_response = send_netmiko_config(device_info, delete_commands)
    
        # Split the netmiko_response into lines
        lines = netmiko_response.split('\n')

        # Remove empty lines
        lines = [line.strip() for line in lines if line.strip()]

        # Create a dictionary with key 'netmiko_response' and value as the lines list
        response_data = {'netmiko_response': lines}

        # Convert the dictionary into a JSON response
        return jsonify(response_data)      

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Sends a Netmiko request to a network device.
#The output received from the device after executing the command, or an error message if an exception occurs.
def send_netmiko_request(device_info, command):
    try:
        # Establish an SSH connection using Netmiko
        with ConnectHandler(**device_info) as ssh_conn:
            output = ssh_conn.send_command(command)
        return output
      
    except Exception as e:
        return f'Netmiko Error: {str(e)}'
      
#Sends configuration commands to a network device using Netmiko.
def send_netmiko_config(device_info, config_commands):
    try:
        # Establish an SSH connection using Netmiko
        with ConnectHandler(**device_info) as ssh_conn:
            # Send configuration commands
            output = ssh_conn.send_config_set(config_commands)
        return output
      
    except Exception as e:
        return f'Netmiko Error: {str(e)}'
    
# Run the Flask application on the specified host and port.
# host: '0.0.0.0' allows the application to be accessible externally.
# port: 5000 is the default port for Flask applications
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)    
