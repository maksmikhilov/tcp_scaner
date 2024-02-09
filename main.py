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
        try:
            print('Запрос к ', host)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            start_time = time.time()
            s.connect((host, port))
            
            s.sendall(first_request.encode())
            first_response = s.recv(4096)
            
            s.sendall(second_request.encode())
            second_response = s.recv(4096)
            
            s.close()
            end_time = time.time()
            wait_time = end_time - start_time
            tcp_data = {
                "name": name,
                "status": "ok",
                "tmstmp": time.time(),
                "request_time": wait_time,
                "first_response": first_response,
                "second_response": second_response
            }
            tcp_row = interface.get_row(TcpResult, (TcpResult.name == name))
            if tcp_row:
                interface.update_row(TcpResult, (TcpResult.name == name), tcp_data)
            else:
                interface.set_row(TcpResult, tcp_data)
            
            time.sleep(request_interval)
        except Exception as e:
            print('Check: ', e)
        
        
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
        
        
        