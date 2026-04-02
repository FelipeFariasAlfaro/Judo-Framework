# language: es
@genai @pruebas-ia
Característica: Evaluación de Respuestas GenAI - Judo Framework

  # El flujo correcto es:
  # 1. Llamar al endpoint de tu API GenAI con pasos REST normales
  # 2. Extraer el campo de respuesta con "uso el campo de respuesta..."
  # 3. Evaluar con RAG, validaciones semánticas o LLM como juez
  #
  # Importar en environment.py:
  #   from judo.genai.steps_genai_es import *
  #
  # Configurar en .env (solo para el juez LLM):
  #   JUDO_AI_PROVIDER=openai
  #   JUDO_OPENAI_API_KEY=sk-...
  #   JUDO_AI_MODEL=gpt-4o

  Antecedentes:
    Dado que configuro la URL base como "https://mi-api-genai.com"
    Y configuro el header "Authorization" como "Bearer ${AI_API_KEY}"

  # -----------------------------------------------------------------------
  # ESTRATEGIA 1: RAG - Comparar respuesta contra documento local
  # -----------------------------------------------------------------------

  @rag @documento-local
  Escenario: Respuesta del chatbot está fundamentada en el manual del producto
    Dado que cargo el contexto RAG desde el archivo "docs/manual_producto.pdf"
    Y establezco el prompt del juez como "¿Cuál es el precio del plan básico?"
    Cuando envío una petición POST a "/chat" con el cuerpo
      """
      {
        "pregunta": "¿Cuál es el precio del plan básico?",
        "session_id": "test-001"
      }
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "respuesta" como respuesta de IA
    Y la respuesta de IA no debe estar vacía
    Y la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.6
    Y la respuesta de IA debe contener hechos del contexto RAG con umbral 0.5

  @rag @contexto-inline
  Escenario: Respuesta del asistente usa información del contexto proporcionado
    Dado que establezco el contexto RAG
      """
      Producto: CloudAPI Pro
      Precio plan básico: $29/mes
      Precio plan profesional: $99/mes
      Precio plan enterprise: $299/mes
      Soporte: Email 24/7 en todos los planes
      Límite de requests: 10,000/mes en básico, ilimitado en enterprise
      """
    Cuando envío una petición POST a "/assistant/query" con el cuerpo
      """
      {
        "query": "¿Cuánto cuesta el plan profesional?",
        "context_id": "pricing-2024"
      }
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "answer" como respuesta de IA
    Y la respuesta de IA debe contener "99"
    Y la similitud semántica de la respuesta de IA con el contexto RAG debe ser al menos 0.4

  @rag @multiples-documentos
  Escenario: Respuesta integra información de múltiples documentos
    Dado que cargo el contexto RAG desde múltiples archivos
      | archivo                        |
      | docs/politicas_privacidad.txt  |
      | docs/terminos_servicio.txt     |
    Cuando envío una petición POST a "/legal/query" con el cuerpo
      """
      {"pregunta": "¿Cómo se manejan mis datos personales?"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "respuesta" como respuesta de IA
    Y la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.5

  # -----------------------------------------------------------------------
  # ESTRATEGIA 2: Validaciones Semánticas
  # -----------------------------------------------------------------------

  @semantica @similitud
  Escenario: Respuesta es semánticamente similar a la respuesta esperada
    Cuando envío una petición GET a "/qa/capital-france"
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "answer" como respuesta de IA
    Y la similitud semántica de la respuesta de IA con "París es la capital de Francia." debe ser al menos 0.5

  @semantica @relevancia
  Escenario: Respuesta es relevante para la pregunta formulada
    Cuando envío una petición POST a "/chat" con el cuerpo
      """
      {"message": "Explica qué es una API REST"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "content" como respuesta de IA
    Y la respuesta de IA debe ser relevante para "¿Qué es una API REST?" con umbral 0.4
    Y la longitud de la respuesta de IA debe ser mayor a 50 caracteres
    Y la longitud de la respuesta de IA debe ser menor a 2000 caracteres

  @semantica @toxicidad
  Escenario: Respuesta del chatbot no contiene contenido tóxico
    Cuando envío una petición POST a "/chat" con el cuerpo
      """
      {"message": "Escribe un mensaje de bienvenida para nuevos empleados"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "response" como respuesta de IA
    Y la respuesta de IA no debe ser tóxica con umbral 0.9
    Y la respuesta de IA no debe contener "odio"
    Y la respuesta de IA no debe contener "violencia"

  @semantica @hechos
  Escenario: Respuesta contiene hechos específicos requeridos
    Cuando envío una petición GET a "/info/python"
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "description" como respuesta de IA
    Y la respuesta de IA debe contener los hechos requeridos
      | hecho           |
      | Python          |
      | programación    |
      | lenguaje        |

  @semantica @completitud
  Escenario: Respuesta cubre todos los temas requeridos
    Cuando envío una petición POST a "/explain" con el cuerpo
      """
      {"topic": "HTTP methods"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "explanation" como respuesta de IA
    Y la respuesta de IA debe cubrir los temas requeridos con umbral 0.75
      | tema   |
      | GET    |
      | POST   |
      | PUT    |
      | DELETE |

  @semantica @tono
  Escenario: Respuesta de soporte tiene tono profesional
    Cuando envío una petición POST a "/support/response" con el cuerpo
      """
      {"complaint": "Mi pedido llegó dañado"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "response" como respuesta de IA
    Y el tono de la respuesta de IA debe ser "professional" con umbral 0.4
    Y el tono de la respuesta de IA debe ser "empathetic" con umbral 0.3

  # -----------------------------------------------------------------------
  # ESTRATEGIA 3: LLM como Juez
  # -----------------------------------------------------------------------

  @juez @criterio-simple
  Escenario: Juez evalúa calidad de respuesta con criterio simple
    Dado que establezco el prompt del juez como "¿Qué es el aprendizaje automático?"
    Cuando envío una petición POST a "/ai/explain" con el cuerpo
      """
      {"question": "¿Qué es el aprendizaje automático?"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "answer" como respuesta de IA
    Y evalúo la respuesta de IA con el juez usando criterio "La respuesta debe explicar claramente el aprendizaje automático, mencionar que las máquinas aprenden de datos y ser comprensible para un no técnico." y umbral 0.7
    Y la evaluación del juez debe pasar

  @juez @criterio-multilinea
  Escenario: Juez evalúa respuesta con rúbrica detallada
    Dado que establezco el prompt del juez como "Escribe un correo declinando una reunión"
    Cuando envío una petición POST a "/generate/email" con el cuerpo
      """
      {"task": "decline meeting email", "tone": "professional"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "email_text" como respuesta de IA
    Y evalúo la respuesta de IA con el juez usando umbral 0.7
      """
      La respuesta debe:
      1. Ser educada y profesional en tono
      2. Declinar claramente la reunión
      3. Ofrecer una alternativa o explicación
      4. Ser concisa (menos de 150 palabras)
      5. No contener lenguaje ofensivo ni informal
      """
    Y la evaluación del juez debe pasar
    Y la puntuación del juez debe ser al menos 0.65

  @juez @rag-combinado
  Escenario: Juez evalúa respuesta contra contexto RAG (combinación RAG + Juez)
    Dado que cargo el contexto RAG desde el archivo "docs/politica_devoluciones.txt"
    Y establezco el prompt del juez como "¿Cuál es la política de devoluciones?"
    Cuando envío una petición POST a "/support/chat" con el cuerpo
      """
      {"message": "¿Cuál es la política de devoluciones?"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "reply" como respuesta de IA
    Y la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.5
    Y evalúo la respuesta de IA con el juez contra el contexto RAG usando criterio "La respuesta debe ser factualmente consistente con la política de devoluciones y dar información clara al cliente." y umbral 0.7
    Y la evaluación del juez debe pasar

  @juez @juez-separado
  Escenario: Usar modelo diferente como juez (modelo más potente evalúa modelo más económico)
    Dado que configuro el juez de IA con proveedor "openai" y modelo "gpt-4o"
    Y establezco el prompt del juez como "Explica la recursión en programación"
    Cuando envío una petición POST a "/ai/mini/explain" con el cuerpo
      """
      {"concept": "recursion", "level": "beginner"}
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "explanation" como respuesta de IA
    Y evalúo la respuesta de IA con el juez usando criterio "La explicación debe ser correcta, usar un ejemplo concreto y ser comprensible para un principiante." y umbral 0.7
    Y la evaluación del juez debe pasar
    Y imprimo el resultado de la evaluación del juez

  # -----------------------------------------------------------------------
  # Combinación de las 3 estrategias
  # -----------------------------------------------------------------------

  @completo @todas-estrategias
  Escenario: Evaluación completa combinando RAG + Semántica + Juez
    Dado que cargo el contexto RAG desde el archivo "docs/manual_soporte.txt"
    Y configuro el juez de IA con proveedor "openai" y modelo "gpt-4o"
    Y establezco el prompt del juez como "¿Cómo soluciono el error de conexión?"
    Cuando envío una petición POST a "/support/ai" con el cuerpo
      """
      {
        "issue": "Connection timeout error",
        "product": "MyApp v2.0"
      }
      """
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "solution" como respuesta de IA
    # Validaciones básicas
    Y la respuesta de IA no debe estar vacía
    Y la respuesta de IA no debe ser tóxica con umbral 0.9
    # RAG: verificar que usa el manual
    Y la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.5
    # Semántica: verificar relevancia y tono
    Y la respuesta de IA debe ser relevante para "¿Cómo soluciono el error de conexión?" con umbral 0.4
    Y el tono de la respuesta de IA debe ser "professional" con umbral 0.4
    # Juez: evaluación holística
    Y evalúo la respuesta de IA con el juez contra el contexto RAG usando umbral 0.7
      """
      La respuesta debe:
      1. Dar pasos concretos para resolver el error de conexión
      2. Ser consistente con la documentación del manual
      3. Ser clara y comprensible para el usuario final
      4. No inventar información no presente en el manual
      """
    Y la evaluación del juez debe pasar
    Y imprimo el resultado de la evaluación del juez

  # -----------------------------------------------------------------------
  # Debug
  # -----------------------------------------------------------------------

  @debug
  Escenario: Inspeccionar respuesta de IA para desarrollo
    Cuando envío una petición GET a "/ai/test"
    Entonces el código de respuesta debe ser 200
    Y uso el campo de respuesta "text" como respuesta de IA
    Y imprimo el texto de respuesta de IA
