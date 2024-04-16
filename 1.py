import socket

from pyModbusTCP.client import ModbusClient

url = "74983955mm.vicp.fun"
ip_address = socket.gethostbyname(url)
ModbusBMS = ModbusClient(host=ip_address, port=18786, unit_id=1, auto_open=True, auto_close=False)
data = ModbusBMS.read_holding_registers(0, 100)
print(data)
