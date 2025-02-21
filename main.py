from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict

app = FastAPI()

# Lista para armazenar conexões e respostas
connected_clients: List[WebSocket] = []
responses: List[Dict] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    # Se for a página do dashboard (index.html), envia histórico de respostas
    await websocket.send_json(responses)

    try:
        while True:
            data = await websocket.receive_json()
            responses.append(data)  # Salva a resposta

            # Envia atualização para todos os clientes conectados
            for client in connected_clients:
                await client.send_json(responses)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
