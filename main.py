import socket
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from db import connection
from db import interface

Tcp_info = connection.Base.metadata.tables['tcp']
Tcp_result = connection.Base.metadata.tables['tcp_result']
def check_tcp(params):
    name, host, port, first_query, second_query, timeout, interval = params
    while True:
        responses = []
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            start_time = time.time()
            s.connect((host, port))
            for query in [first_query, second_query]:
                s.send(query.encode())
                response = s.recv(1024)
                responses.append(response)
            end_time = time.time()
            wait_time = end_time - start_time
            s.close()
            time.sleep(interval)
            tcp_data = {
                "name": name,
                "status": "ok",
                "tmstmp": time.time(),
                "request_time": wait_time,
                "first_response": responses[0],
                "second_response": responses[1]
            }
            print(tcp_data)
            interface.set_row(Tcp_result, tcp_data)
        except Exception as e:
            print(e)
        
        
def run_task_with_timeout(params):
    p = multiprocessing.Process(target=check_tcp, args=(params,))
    print('Запрос к ', params[0])
    p.start()
    p.join(timeout=8)
    if p.is_alive():
        print('Убиваем ', params[0])
        p.terminate()
        p.join()

while True:
    TCPs = interface.get_row(Tcp_info)
    tasks = []
    for TCP in TCPs:
        name, host, port = TCP.name, TCP.host, TCP.port
        print(host)
        print(port)
        first_query, second_query = TCP.first_query, TCP.second_query
        timeout, interval = TCP.timeout, TCP.request_interval
        params = (name, host, port, first_query, second_query, timeout, interval)
        tasks.append(params)
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(run_task_with_timeout, tasks)
    time.sleep(10)
    print('Получаем новые данные')
        
        
        