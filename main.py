import socket
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from db import connection
from db import interface

Tcp_info = connection.Base.metadata.tables['tcp']
Tcp_result = connection.Base.metadata.tables['tcp_result']
print(Tcp_result)

def check_tcp(params):
    name, host, port, first_query, second_query, timeout, request_interval = params
    while True:
        responses = []
        try:
            print('Запрос к ', host)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            start_time = time.time()
            s.connect((host, port))
            for query in [first_query]:
                s.send(query.encode())
                response = s.recv(1024)
                print(query, response)
                responses.append(response)
            
            end_time = time.time()
            wait_time = end_time - start_time
            print(wait_time)
            tcp_data = {
                "name": name,
                "status": "ok",
                "tmstmp": time.time(),
                "request_time": wait_time,
                "first_response": responses[0],
                "second_response": 'ghj'
            }
            print(tcp_data)
            tcp_row = interface.get_row(Tcp_result, (Tcp_result.name == name))
            if tcp_row:
                interface.update_row(Tcp_info, (Tcp_info.host == host, Tcp_info.port == port), tcp_data)
            else:
                interface.set_row(Tcp_result, tcp_data)
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
    TCPs = interface.get_row(Tcp_info)
    tasks = []
    for TCP in TCPs:
        name, host, port = TCP.name, TCP.host, TCP.port
        first_query, second_query = TCP.first_query, TCP.second_query
        timeout, request_interval = TCP.timeout, TCP.request_interval
        params = (name, host, port, first_query, second_query, timeout, request_interval)
        tasks.append(params)
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(run_task_with_timeout, tasks)
    time.sleep(20)
    print('Получаем новые данные')
        
        
        