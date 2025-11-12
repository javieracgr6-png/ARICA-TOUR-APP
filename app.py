<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asistente Turístico - Arica y Parinacota</title>
    <style>
        :root {
            --primary-color: #1a5276;
            --secondary-color: #f39c12;
            --accent-color: #e74c3c;
            --light-color: #ecf0f1;
            --dark-color: #2c3e50;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: #f5f7fa;
            color: var(--dark-color);
            line-height: 1.6;
        }
        
        header {
            background: linear-gradient(135deg, var(--primary-color), #2980b9);
            color: white;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }
        
        .logo {
            font-size: 2.5rem;
            margin-right: 1rem;
        }
        
        h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .chat-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            margin-bottom: 2rem;
        }
        
        .chat-header {
            background-color: var(--primary-color);
            color: white;
            padding: 1rem;
            text-align: center;
            font-weight: bold;
        }
        
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
        }
        
        .message {
            max-width: 80%;
            padding: 0.8rem 1.2rem;
            margin-bottom: 1rem;
            border-radius: 18px;
            line-height: 1.4;
            position: relative;
        }
        
        .user-message {
            align-self: flex-end;
            background-color: var(--secondary-color);
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .bot-message {
            align-self: flex-start;
            background-color: var(--light-color);
            color: var(--dark-color);
            border-bottom-left-radius: 5px;
        }
        
        .chat-input {
            display: flex;
            padding: 1rem;
            border-top: 1px solid #eee;
        }
        
        .chat-input input {
            flex: 1;
            padding: 0.8rem 1rem;
            border: 1px solid #ddd;
            border-radius: 30px;
            outline: none;
            font-size: 1rem;
        }
        
        .chat-input button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            margin-left: 1rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s;
        }
        
        .chat-input button:hover {
            background-color: #154360;
        }
        
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin-top: 1rem;
        }
        
        .quick-action {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 0.6rem 1.2rem;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9rem;
        }
        
        .quick-action:hover {
            background-color: var(--primary-color);
            color: white;
            transform: translateY(-2px);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }
        
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }
        
        .feature-card h3 {
            margin-bottom: 0.8rem;
            color: var(--primary-color);
        }
        
        footer {
            background-color: var(--dark-color);
            color: white;
            text-align: center;
            padding: 1.5rem;
            margin-top: 2rem;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .chat-messages {
                height: 300px;
            }
            
            .message {
                max-width: 90%;
            }
            
            .features {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo-container">
            <div class="logo">🏔️</div>
            <div>
                <h1>Asistente Turístico</h1>
                <p class="subtitle">Descubre la belleza de Arica y Parinacota</p>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="chat-container">
            <div class="chat-header">
                Asistente Virtual - ¿En qué puedo ayudarte?
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">
                    ¡Hola! Soy tu asistente turístico para la región de Arica y Parinacota. ¿En qué puedo ayudarte? Puedes preguntarme sobre lugares para visitar, actividades, gastronomía, alojamiento o transporte.
                </div>
            </div>
            <div class="chat-input">
                <input type="text" id="userInput" placeholder="Escribe tu pregunta aquí..." autocomplete="off">
                <button id="sendButton">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2 21L23 12L2 3V10L17 12L2 14V21Z" fill="white"/>
                    </svg>
                </button>
            </div>
        </div>
        
        <div class="quick-actions">
            <div class="quick-action" data-question="Lugares para visitar">Lugares para visitar</div>
            <div class="quick-action" data-question="Gastronomía típica">Gastronomía típica</div>
            <div class="quick-action" data-question="Actividades al aire libre">Actividades al aire libre</div>
            <div class="quick-action" data-question="Alojamiento recomendado">Alojamiento recomendado</div>
            <div class="quick-action" data-question="Clima y mejor época para visitar">Clima y mejor época</div>
            <div class="quick-action" data-question="Transporte y cómo llegar">Transporte y cómo llegar</div>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">🗺️</div>
                <h3>Mapa Interactivo</h3>
                <p>Explora los principales atractivos turísticos de la región en nuestro mapa interactivo.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📸</div>
                <h3>Galería de Fotos</h3>
                <p>Descubre la belleza de Arica y Parinacota a través de impresionantes imágenes.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🍽️</div>
                <h3>Gastronomía Local</h3>
                <p>Conoce los sabores únicos de la región y los mejores lugares para probarlos.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🏨</div>
                <h3>Alojamiento</h3>
                <p>Encuentra el lugar perfecto para hospedarte según tus preferencias y presupuesto.</p>
            </div>
        </div>
    </div>
    
    <footer>
        <p>Asistente Turístico Arica y Parinacota &copy; 2023 - Todos los derechos reservados</p>
    </footer>

    <script>
        // Base de conocimientos del asistente
        const knowledgeBase = {
            "lugares para visitar": "En Arica y Parinacota puedes visitar: 1. Morro de Arica - Icono histórico con vista panorámica. 2. Catedral de San Marcos - Diseñada por Gustave Eiffel. 3. Parque Nacional Lauca - Con el lago Chungará, uno de los más altos del mundo. 4. Poblado de Parinacota - Típico pueblo altiplánico. 5. Playas como La Lisera y El Laucho. 6. Valle de Azapa - Con geoglifos y museo arqueológico.",
            
            "gastronomía típica": "La gastronomía de Arica y Parinacota incluye: 1. Chairo - Sopa altiplánica con carne y verduras. 2. Asado de llama - Carne típica de la zona. 3. Queso de cabra - Producido localmente. 4. Aceitunas de Azapa - Reconocidas a nivel nacional. 5. Pescados y mariscos frescos - Por su ubicación costera. 6. Api - Bebida caliente de maíz morado.",
            
            "actividades al aire libre": "Actividades recomendadas: 1. Trekking en el Parque Nacional Lauca. 2. Observación de aves en el humedal del río Lluta. 3. Surf en las playas de Arica. 4. Tour por las iglesias altiplánicas. 5. Visita a termas naturales como Jurasi. 6. Sandboard en las dunas de Arica.",
            
            "alojamiento recomendado": "Opciones de alojamiento: 1. Hoteles en el centro de Arica - Para acceso a servicios. 2. Hospedajes en Putre - Para explorar el altiplano. 3. Cabañas en el valle de Azapa - Para una experiencia rural. 4. Refugios en el Parque Nacional Lauca - Para aventureros. 5. Hostales para mochileros - Opción económica.",
            
            "clima y mejor época para visitar": "Clima: Arica tiene clima desértico costero con temperaturas estables todo el año (15-25°C). En el altiplano, el clima es más extremo con días cálidos y noches frías. Mejor época: Todo el año para Arica, pero para el altiplano (Parinacota) se recomienda abril-noviembre para evitar lluvias estivales.",
            
            "transporte y cómo llegar": "Cómo llegar: 1. Avión: Aeropuerto Chacalluta de Arica con vuelos desde Santiago. 2. Bus: Varias empresas conectan Arica con el resto de Chile. 3. Auto: Ruta 5 Norte hasta Arica. Transporte local: 1. Colectivos a Putre y otros pueblos. 2. Tours organizados al altiplano. 3. Transporte público urbano en Arica.",
            
            "cultura y tradiciones": "La cultura de Arica y Parinacota es rica y diversa: 1. Fiesta de la Virgen de las Peñas - Celebrada en Putre. 2. Carnaval Andino Con la Fuerza del Sol - En Arica. 3. Pueblos originarios Aymara - Con tradiciones ancestrales. 4. Arte rupestre y geoglifos - En el valle de Azapa. 5. Música y danzas tradicionales - Influencia andina y costera.",
            
            "eventos y festivales": "Principales eventos: 1. Fiesta de San Pedro - Junio, celebraciones costeras. 2. Aniversario de Arica - Junio, con diversas actividades. 3. Fiesta de la Tirana - Julio, importante celebración religiosa. 4. Festival de la Oliva - Octubre, en el valle de Azapa. 5. Arica Nativa - Noviembre, festival de cine rural."
        };

        // Elementos del DOM
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendButton = document.getElementById('sendButton');
        const quickActions = document.querySelectorAll('.quick-action');

        // Función para agregar mensaje al chat
        function addMessage(message, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Función para procesar la pregunta del usuario
        function processQuestion(question) {
            const lowerQuestion = question.toLowerCase();
            let response = "Lo siento, no tengo información sobre ese tema. ¿Podrías reformular tu pregunta? Puedo ayudarte con lugares para visitar, gastronomía, actividades, alojamiento, clima, transporte, cultura o eventos.";
            
            // Buscar coincidencias en la base de conocimientos
            for (const key in knowledgeBase) {
                if (lowerQuestion.includes(key)) {
                    response = knowledgeBase[key];
                    break;
                }
            }
            
            // Respuestas específicas para saludos
            if (lowerQuestion.includes('hola') || lowerQuestion.includes('buenos días') || lowerQuestion.includes('buenas tardes')) {
                response = "¡Hola! Soy tu asistente turístico para Arica y Parinacota. ¿En qué puedo ayudarte hoy?";
            }
            
            if (lowerQuestion.includes('gracias') || lowerQuestion.includes('thank you')) {
                response = "¡De nada! Estoy aquí para ayudarte. ¿Tienes alguna otra pregunta sobre Arica y Parinacota?";
            }
            
            return response;
        }

        // Función para enviar mensaje
        function sendMessage() {
            const question = userInput.value.trim();
            if (question === '') return;
            
            addMessage(question, true);
            userInput.value = '';
            
            // Simular tiempo de respuesta
            setTimeout(() => {
                const response = processQuestion(question);
                addMessage(response, false);
            }, 1000);
        }

        // Event Listeners
        sendButton.addEventListener('click', sendMessage);
        
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        quickActions.forEach(action => {
            action.addEventListener('click', () => {
                const question = action.getAttribute('data-question');
                userInput.value = question;
                sendMessage();
            });
        });
    </script>
</body>
</html>
