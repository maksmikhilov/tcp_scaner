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
            s.settimeout(5)
            start_time = time.time()
            s.connect((host, port))
            
            s.sendall(first_request.encode())
            first_response = s.recv(4096)
            print('Получили первый ответ: ', host)
           
            if second_request:
                s.sendall(second_request.encode())
                second_response = s.recv(4096)
                print('Получили второй ответ: ', host)
            end_time = time.time()
            s.close()
            tcp_data = {
                "name": name,
                "status": "ok",
                "tmstmp": time.time(),
                "request_time": end_time - start_time,
                "first_response": first_response,
                "second_response": second_response
            }
            tcp_row = interface.get_row(TcpResult, (TcpResult.name == name))
            if tcp_row:
                interface.update_row(TcpResult, (TcpResult.name == name), tcp_data)
                print('Обновили запись: ', host)
            else:
                interface.set_row(TcpResult, tcp_data)
                print('Сделали запись: ', host)
            
            time.sleep(10)
        except Exception as e:
            print('Check: ', e)
        
        
def run_task_with_timeout(params):
    p = multiprocessing.Process(target=check_tcp, args=(params,))
    p.start()
    p.join(timeout=20)
    if p.is_alive():
        p.terminate()
        p.join()
        print('Убили ', params[1])

while True:
    
    TCPs = interface.get_row(TcpInfo)
    tasks = []
    for TCP in TCPs:
        name, host, port = TCP['name'] , TCP['host'], TCP['port']
        first_request, = TCP['first_request']
        try:
            second_request = TCP['second_request']
        except:
            second_request = None
        timeout, request_interval = TCP['timeout'], TCP['request_interval']
        params = (name, host, port, first_request, second_request, timeout, request_interval)
        tasks.append(params)
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(run_task_with_timeout, tasks)
    time.sleep(25)
    print('Получаем новые данные')
        
        
        