import os
import uvicorn
from multiprocessing import Process
from app.app import app as flask_app
from app.api import api
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port):
    port = start_port
    while is_port_in_use(port):
        port += 1
    return port

def run_flask():
    port = find_available_port(5000)
    flask_app.run(host='0.0.0.0', port=port)

def run_fastapi():
    port = find_available_port(8000)
    uvicorn.run(api, host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Asegurar que el directorio instance existe
    os.makedirs('instance', exist_ok=True)
    
    # Iniciar Flask y FastAPI en procesos separados
    flask_process = Process(target=run_flask)
    fastapi_process = Process(target=run_fastapi)
    
    try:
        flask_process.start()
        fastapi_process.start()
        
        flask_process.join()
        fastapi_process.join()
    except KeyboardInterrupt:
        flask_process.terminate()
        fastapi_process.terminate()
        flask_process.join()
        fastapi_process.join()
