import socket
import json
import random
import time

SERVER_IP = "127.0.0.1"
PORT = 5000

# Función objetivo
# Máximo cerca de x=42
def fitness(x):
    return -(x - 42)**2 + 1000

def connect_to_server(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, port))
        print(f"Conectado a servidor en {ip}:{port}")
        return client
    except ConnectionRefusedError:
        print(f"Error: no hay servidor escuchando en {ip}:{port}. Modo local activado.")
    except OSError as exc:
        print(f"Error de conexión a {ip}:{port}: {exc}. Modo local activado.")
    return None

sock = connect_to_server(SERVER_IP, PORT)

local_best = {
    "x": random.uniform(-100, 100),
    "score": float("-inf")
}

while True:

    # Exploración aleatoria
    candidate_x = local_best["x"] + random.uniform(-5, 5)

    score = fitness(candidate_x)

    if score > local_best["score"]:
        local_best = {
            "x": candidate_x,
            "score": score
        }

    if sock is not None:
        try:
            sock.send(json.dumps(local_best).encode())
            response = sock.recv(1024)
            global_best = json.loads(response.decode())

            # Aprendizaje cooperativo
            if global_best["score"] > local_best["score"]:
                local_best = global_best
        except (ConnectionResetError, BrokenPipeError, OSError) as exc:
            print(f"Conexión al servidor perdida: {exc}. Continuando en modo local.")
            sock = None

    print(
        f"Local: {local_best['x']:.4f} "
        f"Score: {local_best['score']:.2f}"
    )

    time.sleep(0.2)