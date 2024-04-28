import socket

from pyModbusTCP.client import ModbusClient

# url = "74983955mm.vicp.fun"
# ip_address = socket.gethostbyname(url)
# ModbusBMS = ModbusClient(host=ip_address, port=18786, unit_id=1, auto_open=True, auto_close=False)
# data = ModbusBMS.read_holding_registers(0, 100)
# print(data)
from django.conf import settings

settings.configure(USE_TZ=False)  # 或者False，取决于你的需求
from django.utils import timezone
import datetime

#  Get  the  current  time
now = timezone.now()

#  Extract  the  seconds  and  milliseconds
seconds = now.second
milliseconds = now.microsecond // 1000

#  Round  the  seconds  based  on  the  milliseconds
if milliseconds <= 250:
    #  If  milliseconds  are  less  than  or  equal  to  250,  round  down  to  0
    rounded_seconds = 0
else:
    #  If  milliseconds  are  greater  than  250,  round  up  to  5
    rounded_seconds = 5

#  If  the  rounded  seconds  are  different,  adjust  the  datetime  object
if seconds != rounded_seconds:
    now = now.replace(second=rounded_seconds, microsecond=0)

#  Format  the  datetime  object  to  the  desired  string  format
formatted_now = now.strftime('%Y-%m-%d    %H:%M:%S') + '.000000'

print(formatted_now)
