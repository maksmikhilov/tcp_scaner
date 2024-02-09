import socket
import time
import multiprocessing
from db.interface import get_row, set_row
from db import connection
def check_tcp(params):
    name, host, port, first_query, second_query, timeout, interval = params
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            start_time = time.time()
            s.connect((host, port))
            for query in [first_query, second_query]:
                s.send(query.encode())
                response = s.recv(1024)
            end_time = time.time()
            wait_time = end_time - start_time
            s.close()
            time.sleep(interval)
        except Exception as e:
            print(e)
        
        
def run_task_with_timeout(params):
    p = multiprocessing.Process(target=check_tcp, args=(params,))
    p.start()
    p.join(timeout=5)
    if p.is_alive():
        p.terminate()
        p.join()
        
while True:
    TCPs = get_row(Tcp_table)
    print(TCPs)
    tasks = []
    for TCP in TCPs:
        name, host, port = TCP.name, TCP.host, TCP.port
        first_query, second_query = TCP.first_query, TCP.second_query
        timeout, interval = TCP.timeout, TCP.interval
        params = (name, host, port, first_query, second_query, timeout, interval)
        tasks.append(params)
        with multiprocessing.Pool(64) as pool:
            pool.map(run_task_with_timeout, tasks)
        
        