import socket
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from db import connection
from db import interface
from db.models import TcpResult, TcpInfo


def check_tcp(params):
    name, host, port, first_request, second_request, timeout, request_interval = params
    while True:
        try:
            print('Запрос к ', host)
            connect_start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((host, port))
            connect_end = time.time()


            request_start = time.time()
            s.sendall(first_request.encode())
            first_response = s.recv(4096)
            print('Получили первый ответ: ', host)
           
            """
            if second_request:
                s.sendall(second_request.encode())
                second_response = s.recv(4096)
                print('Получили второй ответ: ', host)
            """
            request_end = time.time()
            s.close()
            tcp_data = {
                "name": name,
                "status": "ok",
                "tmstmp": time.time(),
                "request_time": request_end - request_start,
                "connect_time": connect_end - connect_start,
                "first_response": first_response,
                "second_response": 'second_response'
            }
            tcp_row = interface.get_row(TcpResult, (TcpResult.name == name))
            print(tcp_row)
            if tcp_row:
                interface.update_row(TcpResult, (TcpResult.name == name), tcp_data)
                print('Обновили запись: ', host)
            else:
                interface.set_row(TcpResult, tcp_data)
                print('Сделали запись: ', host)
            
            time.sleep(5)
        except Exception as e:
            print('Check: ', e)
        
        
def run_task_with_timeout(params):
    p = multiprocessing.Process(target=check_tcp, args=(params,))
    p.start()
    p.join(timeout=15)
    if p.is_alive():
        p.terminate()
        p.join()
        print('Убили ', params[1])

while True:
    
    TCPs = interface.get_row(TcpInfo)
    if not TCPs:
        continue
    tasks = []
    for TCP in TCPs:
        name, host, port = TCP['name'] , TCP['host'], TCP['port']
        first_request, second_request= TCP['first_request'], TCP['second_request']
        timeout, request_interval = TCP['timeout'], TCP['request_interval']
        params = (name, host, port, first_request, second_request, timeout, request_interval)
        tasks.append(params)
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(run_task_with_timeout, tasks)
    time.sleep(17)
    print('Получаем новые данные')
        
        
        