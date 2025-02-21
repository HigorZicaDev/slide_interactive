# TUTORIAL PYTHON WEBSOCKET

A ideia central desse tutorial é explorar como funcionam os websockets usando a linguagem de programação python e criar um exemplo real de uso para o mercado.

IDEIA : APRESENTAÇÕES SLIDES COM INTERAÇÕES DE PARTICIPANTES USANDO PYTHON (FASTAPI) WEBSOCKETS.

Vamos iniciar o projeto python : 

- Criar pasta do código do nosso projeto slide_interactive

```bash
mkdir slide_interactive
```

## 1º Passo: criar um ambiente de desenvolvimento venv e instalar dependências do projeto :

- Comandos para criar o ambiente podem varias de acordo com sistema operacional nesse exemplo estamos usando Windows (caso você esteja em outro sistema operacional faça uma pesquisa dos comandos equivalentes para seu sistema operacional).

```bash
# criar ambiente
python -m venv venv
# ativar ambiente
venv\Scripts\activate 
```

- Instalar as dependências necessárias : (atenção para usar websockets em um server uvicorn precisamos instalar a versão standart)

```bash
pip install "uvicorn[standard]"

pip install fastapi
```

## 2º Passo: Criar o arquivo que vai conter a lógica da nossa aplicação python na raiz da pasta slide_interactive.

- Criar um arquivo chamado [main.py](http://main.py).
- O código em [main.py](http://main.py) é responsável por abrir uma conexão com o websocket na url e porta : [http://localhost:8000](http://localhost:8000).
- Ele vai armazenar as conexões (usuarios) e as respostas em duas váriaveis List Dict criadas abaixo no código fonte e depois vamos manipular as respostas para serem exibidas na nossa página de dashboard simultaneamente enquanto os formulários são preenchidos.

```bash
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

```

## 3º Passo: Criar nossos arquivos responsáveis pelo frontend (onde o usuário vai realizar suas ações de preencher o formulário e onde receberemos as respostas no dashboard).

- Primeiro arquivo a ser criado form.html (responsável por capturar as respostas e envia-las a nosso Backend que já está preparada no arquivo [main.py](http://main.py)).

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preencher Formulário</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
    </style>
</head>
<body>

    <h2>Preencha o Formulário</h2>
    <form id="form">
        <input type="text" id="name" placeholder="Nome" required>
        <input type="email" id="email" placeholder="E-mail" required>

        <h3>Qual linguagem de programação você utiliza?</h3>
        <label><input type="checkbox" name="language" value="Python"> Python</label>
        <label><input type="checkbox" name="language" value="Nodejs"> Node.js</label>
        <label><input type="checkbox" name="language" value="C#"> C#</label>
        <label><input type="checkbox" name="language" value="Java"> Java</label>
        <label><input type="checkbox" name="language" value="PHP"> PHP</label>
        <label><input type="checkbox" name="language" value="Golang"> Golang</label>

        <h3>Qual é seu nível de experiência?</h3>
        <label><input type="radio" name="experience" value="Iniciante"> Iniciante</label>
        <label><input type="radio" name="experience" value="Intermediário"> Intermediário</label>
        <label><input type="radio" name="experience" value="Avançado"> Avançado</label>

        <h3>Objetivo ao participar?</h3>
        <textarea id="goal" maxlength="200"></textarea>

        <button type="submit">Enviar</button>
    </form>

    <script>
        const socket = new WebSocket("ws://localhost:8000/ws");

        document.getElementById("form").addEventListener("submit", function(event) {
            event.preventDefault();
            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;

            const languages = [...document.querySelectorAll("input[name='language']:checked")].map(el => el.value);
            const experience = document.querySelector("input[name='experience']:checked")?.value || "";
            const goal = document.getElementById("goal").value;

            const data = { name, email, languages, experience, goal };
            socket.send(JSON.stringify(data));

            document.getElementById("form").reset();
            alert("Resposta enviada com sucesso!");
        });
    </script>

</body>
</html>

```

- Segundo arquivo que vamos criar é o index.html onde vamos exibir as respostas dos usuários de maneira totalmente simultânea através de uma tabela e um gráfico.

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard em Tempo Real</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        table { width: 80%; margin: auto; border-collapse: collapse; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
    </style>
</head>
<body>

    <h2>Dashboard em Tempo Real</h2>
    <table>
        <thead>
            <tr>
                <th>Nome</th>
                <th>Email</th>
                <th>Linguagens</th>
                <th>Experiência</th>
                <th>Objetivo</th>
            </tr>
        </thead>
        <tbody id="dashboard"></tbody>
    </table>

    <h2>Gráfico de Linguagens Utilizadas</h2>
    <canvas id="chart"></canvas>

    <script>
        const socket = new WebSocket("ws://localhost:8000/ws");
        let responses = [];

        function updateDashboard() {
            const dashboard = document.getElementById("dashboard");
            dashboard.innerHTML = "";

            const languageCount = { Python: 0, Nodejs: 0, "C#": 0, Java: 0, PHP: 0, Golang: 0 };

            responses.forEach(user => {
                const row = `<tr>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>${user.languages.join(", ")}</td>
                    <td>${user.experience}</td>
                    <td>${user.goal}</td>
                </tr>`;
                dashboard.innerHTML += row;

                user.languages.forEach(lang => {
                    languageCount[lang]++;
                });
            });

            updateChart(languageCount);
        }

        function updateChart(data) {
            const ctx = document.getElementById("chart").getContext("2d");
            if (window.myChart) window.myChart.destroy();

            window.myChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: Object.keys(data),
                    datasets: [{
                        label: "Número de usuários",
                        data: Object.values(data),
                        backgroundColor: ["red", "blue", "green", "yellow", "purple", "orange"]
                    }]
                }
            });
        }

        socket.onmessage = function(event) {
            responses = JSON.parse(event.data);
            updateDashboard();
        };
    </script>

</body>
</html>

```

## 4º Passo: Enfim vamos testar se a nossa aplicação está funcionando e se temos a interatividade proporcionada pelo poder do websocket.

- Primeiro passo executar o comando abaixo para criar o servidor uvicorn e subir a aplicação Backend.

```bash
uvicorn main:app --reload 
```

Segundo passo executar o servidor frontend para conseguir visualizar e simular pelo navegador as ações de preencher o formulário e exibir no dashboard as respostas em tempo real. Nesse exemplo estarei usando a extensão do vscode Live server pois é a mais simples e funcional que encontrei. Fica a dica de testar com outros serviços.

```bash
Play live server.
```

[slide_interactive_demo.mp4](slide_interactive_demo.mp4)