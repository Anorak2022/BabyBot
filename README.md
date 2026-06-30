# 👶 BabyBot

Asistente virtual conversacional enfocado en resolver dudas sobre el embarazo y brindar recomendaciones personalizadas, construido con **Rasa** y reforzado con la **API de OpenAI** para ampliar la cobertura de respuestas más allá del modelo NLP entrenado.

## 📋 Descripción

BabyBot es un chatbot de dominio especializado en salud materna. Fue entrenado con más de **1,000 intenciones**, permitiéndole reconocer una amplia variedad de preguntas relacionadas al embarazo y ofrecer respuestas y recomendaciones útiles a las usuarias. Cuando una consulta se sale del alcance del modelo entrenado en Rasa, el sistema recurre a la API de OpenAI para generar una respuesta complementaria, manteniendo la conversación fluida y resolutiva.

El proyecto fue diseñado, entrenado y desplegado de forma independiente, incluyendo la puesta en producción en un servidor web.

## ✨ Características

- 🧠 Motor conversacional basado en **Rasa Open Source** (NLU + Core)
- 💬 Más de 1,000 intenciones entrenadas sobre dudas y recomendaciones de embarazo
- 🤖 Integración con **OpenAI API** como capa de refuerzo para consultas complejas o fuera de dominio
- ⚙️ Acciones personalizadas (`actions/`) para lógica de negocio específica
- ☁️ Desplegado en servidor web en producción

## 🛠️ Tecnologías

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python |
| Framework NLP/NLU | Rasa |
| IA Generativa | OpenAI API |
| Despliegue | Servidor Web |

## 📁 Estructura del proyecto

```
BabyBot/
├── actions/          # Acciones personalizadas (custom actions de Rasa)
├── data/             # Datos de entrenamiento: NLU, historias y reglas
├── models/           # Modelos entrenados
├── tests/            # Pruebas del bot
├── config.yml        # Configuración del pipeline de NLU y políticas de diálogo
├── domain.yml        # Dominio del bot: intents, entidades, respuestas y slots
├── credentials.yml   # Credenciales de los canales de conexión
└── endpoints.yml     # Configuración de endpoints (acciones, tracker store, etc.)
```

## 🚀 Instalación y uso

### Requisitos previos

- Python 3.8+
- pip
- Cuenta y API Key de OpenAI

### Pasos

1. Clonar el repositorio
   ```bash
   git clone https://github.com/Anorak2022/BabyBot.git
   cd BabyBot
   ```

2. Crear un entorno virtual e instalar dependencias
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   pip install rasa openai
   ```

3. Configurar las credenciales
   - Agregar tu API Key de OpenAI en el archivo correspondiente de configuración/variables de entorno.

4. Entrenar el modelo
   ```bash
   rasa train
   ```

5. Iniciar el servidor de acciones (en una terminal aparte)
   ```bash
   rasa run actions
   ```

6. Ejecutar el bot en modo interactivo
   ```bash
   rasa shell
   ```

## 🧪 Pruebas

```bash
rasa test
```

## 📌 Estado del proyecto

Proyecto funcional, desplegado y probado en servidor web. Desarrollo y mantenimiento individual.

## 👤 Autor

**Irvin Adonay Peraza Hernández**
Backend Developer — APIs & Services
📧 irvin13peraza@gmail.com
🔗 [github.com/Anorak2022](https://github.com/Anorak2022)

## 📄 Licencia

Este proyecto es de uso personal/educativo. Si deseas reutilizarlo, contáctame.
