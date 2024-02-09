import socket
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from db import connection
from db import interface
from db.models import TcpResult, TcpInfo

print(TcpResult)

def check_tcp(params):
    name, host, port, first_request, second_request, timeout, request_interval = params
    while True:
        responses = []
        try:
            print('Запрос к ', host)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            start_time = time.time()
            s.connect((host, port))
            for request in [first_request]:
                s.send(request.encode())
                response = s.recv(1024)
                responses.append(response)
            
            end_time = time.time()
            wait_time = end_time - start_time
            tcp_data = {
                "name": name,
                "status": "ok",
                "tmstmp": time.time(),
                "request_time": wait_time,
                "first_response": responses[0],
                "second_response": 'ghj'
            }
            print(tcp_data)
            tcp_row = interface.get_row(TcpResult, (TcpResult.name == name))
            if tcp_row:
                interface.update_row(TcpResult, (TcpResult.name == name), tcp_data)
            else:
                interface.set_row(TcpResult, tcp_data)
            s.close()
            time.sleep(6)
        except Exception as e:
            print(e)
        
        
def run_task_with_timeout(params):
    p = multiprocessing.Process(target=check_tcp, args=(params,))
    p.start()
    p.join(timeout=16)
    if p.is_alive():
        p.terminate()
        p.join()
        print('Убили ', params[1])

while True:
    
    TCPs = interface.get_row(TcpInfo)
    tasks = []
    for TCP in TCPs:
        name, host, port = TCP['name'] , TCP['host'], TCP['port']
        first_request, second_request = TCP['first_request'], TCP['second_request']
        timeout, request_interval = TCP['timeout'], TCP['request_interval']
        params = (name, host, port, first_request, second_request, timeout, request_interval)
        tasks.append(params)
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(run_task_with_timeout, tasks)
    time.sleep(20)
    print('Получаем новые данные')
        
        
        