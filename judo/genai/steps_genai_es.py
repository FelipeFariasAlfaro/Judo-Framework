"""
Judo Framework - Pasos de Evaluación GenAI (Español)

PROPÓSITO: Evaluar respuestas de IA obtenidas mediante pasos REST normales.
El flujo es:
  1. Llamar al endpoint de tu API GenAI usando pasos REST normales de Judo
  2. Extraer el texto de la respuesta de IA en una variable
  3. Usar estos pasos para evaluar esa respuesta

Tres estrategias de evaluación:
  - RAG (Retrieval Augmented Generation): comparar respuesta contra contexto
    de documentos locales o bases de datos
  - Validaciones semánticas: medir similitud, relevancia, toxicidad, etc.
  - LLM como juez: usar un modelo de IA para evaluar la calidad de la respuesta

Importar en environment.py:
    from judo.genai.steps_genai_es import *

Configuración en .env:
    JUDO_AI_PROVIDER=openai          # openai | claude | gemini (solo para el juez)
    JUDO_OPENAI_API_KEY=sk-...
    JUDO_AI_MODEL=gpt-4o
    JUDO_AI_TEMPERATURE=0.0
    JUDO_AI_TIMEOUT=60
"""

import os
from behave import step

from .judge import GenAIJudge
from .context_loader import ContextLoader
from .evaluators import (
    SemanticSimilarityEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
    FactualAccuracyEvaluator,
    HallucinationEvaluator,
    ToneEvaluator,
    CompletenessEvaluator,
)


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _get_judge(context) -> GenAIJudge:
    if not hasattr(context, "_judo_ai_judge") or context._judo_ai_judge is None:
        from .client import GenAIClient
        judge_client = getattr(context, "_judo_ai_judge_client", None) or GenAIClient()
        context._judo_ai_judge = GenAIJudge(judge_client)
    return context._judo_ai_judge


def _get_loader(context) -> ContextLoader:
    if not hasattr(context, "_judo_ctx_loader"):
        context._judo_ctx_loader = ContextLoader()
    return context._judo_ctx_loader


def _get_response_text(context) -> str:
    text = getattr(context, "_judo_eval_text", None)
    assert text, (
        "No hay texto de respuesta de IA para evaluar. "
        "Usa 'uso el campo de respuesta \"<campo>\" como respuesta de IA' primero."
    )
    return text


def _get_rag_context(context) -> str:
    ctx = getattr(context, "_judo_rag_context", None)
    assert ctx, (
        "No hay contexto RAG cargado. "
        "Usa 'cargo el contexto RAG desde ...' primero."
    )
    return ctx


# ===========================================================================
# PASO 0 — Conectar la respuesta a evaluar
# ===========================================================================

@step('uso el campo de respuesta "{field}" como respuesta de IA')
def step_es_use_response_field(context, field):
    """
    Extrae un campo de la última respuesta HTTP y lo establece como texto
    a evaluar por los pasos GenAI siguientes.

    Ejemplo:
        Cuando envío una petición GET a "/chat/respuesta"
        Entonces el código de respuesta debe ser 200
        Y uso el campo de respuesta "respuesta" como respuesta de IA
    """
    assert hasattr(context, "judo_context") and context.judo_context.response, \
        "No hay respuesta HTTP disponible. Realiza una llamada REST primero."
    resp = context.judo_context.response
    data = resp.json if resp.json else {}
    parts = field.split(".")
    val = data
    for part in parts:
        if isinstance(val, dict):
            val = val.get(part)
        elif isinstance(val, list):
            try:
                val = val[int(part)]
            except (ValueError, IndexError):
                val = None
        else:
            val = None
        if val is None:
            break
    assert val is not None, f"Campo '{field}' no encontrado en la respuesta: {data}"
    context._judo_eval_text = str(val)


@step('uso el campo de respuesta "{field}" como respuesta de IA con valor por defecto "{fallback}"')
def step_es_use_response_field_fallback(context, field, fallback):
    """Igual que el anterior pero usa un valor por defecto si el campo no existe."""
    try:
        step_es_use_response_field(context, field)
    except AssertionError:
        context._judo_eval_text = fallback


@step('establezco el texto de respuesta de IA como "{text}"')
def step_es_set_response_text(context, text):
    """Establece manualmente el texto a evaluar."""
    context._judo_eval_text = text


@step('establezco el texto de respuesta de IA')
def step_es_set_response_text_multiline(context):
    """Establece el texto de respuesta de IA desde un bloque multilínea."""
    context._judo_eval_text = context.text.strip()


@step('uso la variable "{variable_name}" como respuesta de IA')
def step_es_use_variable_as_response(context, variable_name):
    """Usa el valor de una variable de Judo como texto de respuesta de IA a evaluar."""
    val = context.judo_context.get_variable(variable_name)
    assert val, f"La variable '{variable_name}' está vacía o no está definida."
    context._judo_eval_text = str(val)


@step('almaceno el texto de respuesta de IA en la variable "{variable_name}"')
def step_es_store_eval_text(context, variable_name):
    """Almacena el texto de respuesta de IA actual en una variable de Judo."""
    text = _get_response_text(context)
    context.judo_context.set_variable(variable_name, text)


# ===========================================================================
# ESTRATEGIA 1 — RAG (Retrieval Augmented Generation)
# ===========================================================================

@step('cargo el contexto RAG desde el archivo "{file_path}"')
def step_es_rag_load_file(context, file_path):
    """
    Carga un documento local como contexto RAG.
    Soporta: .txt, .md, .json, .yaml, .csv, .pdf, .docx

    Ejemplo:
        Dado que cargo el contexto RAG desde el archivo "docs/manual_producto.pdf"
    """
    loader = _get_loader(context)
    context._judo_rag_context = loader.load(file_path)


@step('cargo el contexto RAG desde la URL "{url}"')
def step_es_rag_load_url(context, url):
    """
    Obtiene contenido de una URL y lo usa como contexto RAG.

    Ejemplo:
        Dado que cargo el contexto RAG desde la URL "https://docs.miapi.com/faq"
    """
    loader = _get_loader(context)
    context._judo_rag_context = loader.load_url(url)


@step('cargo el contexto RAG desde múltiples archivos')
def step_es_rag_load_multiple(context):
    """
    Carga múltiples archivos como contexto RAG (tabla con columna 'archivo').

    Ejemplo:
        Dado que cargo el contexto RAG desde múltiples archivos
          | archivo                 |
          | docs/manual.pdf         |
          | docs/faq.txt            |
    """
    loader = _get_loader(context)
    files = [row["archivo"] for row in context.table]
    context._judo_rag_context = loader.load_multiple(files)


@step('establezco el contexto RAG')
def step_es_rag_set_inline(context):
    """
    Establece el contexto RAG desde un bloque de texto multilínea.

    Ejemplo:
        Dado que establezco el contexto RAG
          \"\"\"
          Producto: MiApp v2.0
          Precio: $99/mes
          Soporte: 24/7
          \"\"\"
    """
    context._judo_rag_context = context.text.strip()


@step('establezco el contexto RAG como "{text}"')
def step_es_rag_set_inline_single(context, text):
    """Establece el contexto RAG desde una cadena de texto simple."""
    context._judo_rag_context = text


@step('la respuesta de IA debe estar fundamentada en el contexto RAG con umbral {threshold:f}')
def step_es_rag_grounded(context, threshold):
    """
    Verifica que la respuesta de IA está fundamentada en el contexto RAG cargado.
    Detecta alucinaciones — contenido no respaldado por el contexto.
    Umbral: 0.0-1.0 (recomendado: 0.6-0.8)

    Ejemplo:
        Entonces la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.7
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    evaluator = HallucinationEvaluator()
    result = evaluator.evaluate(response=text, context=rag_ctx, threshold=threshold)
    assert result.passed, (
        f"Verificación de fundamentación RAG FALLÓ: {result.reason}\n"
        f"Puntuación: {result.score:.2%} (umbral: {threshold:.0%})"
    )


@step('la respuesta de IA debe contener hechos del contexto RAG con umbral {threshold:f}')
def step_es_rag_facts(context, threshold):
    """
    Verifica que la respuesta de IA contiene términos clave del contexto RAG.
    Umbral: 0.0-1.0 (recomendado: 0.5-0.8)

    Ejemplo:
        Entonces la respuesta de IA debe contener hechos del contexto RAG con umbral 0.6
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    import re
    words = re.findall(r'\b[A-Za-z0-9\u00C0-\u024F][A-Za-z0-9\u00C0-\u024F\-_\.]{3,}\b', rag_ctx)
    facts = list(dict.fromkeys(w for w in words if len(w) > 4))[:30]
    evaluator = FactualAccuracyEvaluator()
    result = evaluator.evaluate(response=text, facts=facts, threshold=threshold)
    assert result.passed, (
        f"Verificación de hechos RAG FALLÓ: {result.reason}\n"
        f"Términos faltantes: {result.details.get('missing', [])[:10]}"
    )


@step('la similitud semántica de la respuesta de IA con el contexto RAG debe ser al menos {threshold:f}')
def step_es_rag_semantic_similarity(context, threshold):
    """
    Verifica que la respuesta de IA es semánticamente similar al contexto RAG.
    Umbral: 0.0-1.0 (recomendado: 0.4-0.7)

    Ejemplo:
        Entonces la similitud semántica de la respuesta de IA con el contexto RAG debe ser al menos 0.5
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    evaluator = SemanticSimilarityEvaluator()
    result = evaluator.evaluate(response=text, expected=rag_ctx, threshold=threshold)
    assert result.passed, f"Similitud semántica RAG FALLÓ: {result.reason}"


# ===========================================================================
# ESTRATEGIA 2 — Validaciones Semánticas
# ===========================================================================

@step('la respuesta de IA no debe estar vacía')
def step_es_not_empty(context):
    """Verifica que el texto de respuesta de IA no está vacío."""
    text = _get_response_text(context)
    assert text.strip(), "La respuesta de IA está vacía."


@step('la respuesta de IA debe contener "{text}"')
def step_es_contains(context, text):
    """Verifica que la respuesta de IA contiene un texto específico (sin distinción de mayúsculas)."""
    resp = _get_response_text(context)
    assert text.lower() in resp.lower(), (
        f"La respuesta de IA no contiene '{text}'.\nRespuesta: {resp[:300]}"
    )


@step('la respuesta de IA no debe contener "{text}"')
def step_es_not_contains(context, text):
    """Verifica que la respuesta de IA NO contiene un texto específico."""
    resp = _get_response_text(context)
    assert text.lower() not in resp.lower(), (
        f"La respuesta de IA no debería contener '{text}' pero lo contiene."
    )


@step('la longitud de la respuesta de IA debe ser menor a {max_chars:d} caracteres')
def step_es_max_length(context, max_chars):
    """Verifica que la respuesta de IA es más corta que max_chars."""
    resp = _get_response_text(context)
    assert len(resp) < max_chars, (
        f"La respuesta tiene {len(resp)} caracteres, se esperaban menos de {max_chars}."
    )


@step('la longitud de la respuesta de IA debe ser mayor a {min_chars:d} caracteres')
def step_es_min_length(context, min_chars):
    """Verifica que la respuesta de IA es más larga que min_chars."""
    resp = _get_response_text(context)
    assert len(resp) > min_chars, (
        f"La respuesta tiene {len(resp)} caracteres, se esperaban más de {min_chars}."
    )


@step('la similitud semántica de la respuesta de IA con "{expected}" debe ser al menos {threshold:f}')
def step_es_semantic_similarity(context, expected, threshold):
    """
    Verifica la similitud semántica entre la respuesta de IA y un texto esperado.
    Umbral: 0.0-1.0

    Ejemplo:
        Entonces la similitud semántica de la respuesta de IA con "París es la capital de Francia." debe ser al menos 0.6
    """
    text = _get_response_text(context)
    evaluator = SemanticSimilarityEvaluator()
    result = evaluator.evaluate(response=text, expected=expected, threshold=threshold)
    assert result.passed, f"Similitud semántica FALLÓ: {result.reason}"


@step('la respuesta de IA debe ser relevante para "{prompt}" con umbral {threshold:f}')
def step_es_relevance(context, prompt, threshold):
    """
    Verifica que la respuesta de IA es relevante para un prompt/pregunta dado.
    Umbral: 0.0-1.0 (recomendado: 0.3-0.6)

    Ejemplo:
        Entonces la respuesta de IA debe ser relevante para "¿Qué es el aprendizaje automático?" con umbral 0.4
    """
    text = _get_response_text(context)
    evaluator = RelevanceEvaluator()
    result = evaluator.evaluate(response=text, prompt=prompt, threshold=threshold)
    assert result.passed, f"Verificación de relevancia FALLÓ: {result.reason}"


@step('la respuesta de IA no debe ser tóxica con umbral {threshold:f}')
def step_es_toxicity(context, threshold):
    """
    Verifica que la respuesta de IA no contiene contenido tóxico.
    Puntuación 1.0 = limpio, 0.0 = muy tóxico.
    Umbral: 0.0-1.0 (recomendado: 0.8-0.95)

    Ejemplo:
        Entonces la respuesta de IA no debe ser tóxica con umbral 0.9
    """
    text = _get_response_text(context)
    evaluator = ToxicityEvaluator()
    result = evaluator.evaluate(response=text, threshold=threshold)
    assert result.passed, f"Verificación de toxicidad FALLÓ: {result.reason}"


@step('la respuesta de IA debe contener los hechos requeridos')
def step_es_factual_accuracy(context):
    """
    Verifica que la respuesta de IA contiene todos los hechos de la tabla.
    Columnas de la tabla: hecho, (opcional) umbral

    Ejemplo:
        Entonces la respuesta de IA debe contener los hechos requeridos
          | hecho       |
          | Python      |
          | código abierto |
    """
    text = _get_response_text(context)
    facts = [row["hecho"] for row in context.table]
    threshold = float(context.table[0].get("umbral", 0.8)) if context.table else 0.8
    evaluator = FactualAccuracyEvaluator()
    result = evaluator.evaluate(response=text, facts=facts, threshold=threshold)
    assert result.passed, (
        f"Precisión factual FALLÓ: {result.reason}\n"
        f"Faltantes: {result.details.get('missing', [])}"
    )


@step('el tono de la respuesta de IA debe ser "{expected_tone}" con umbral {threshold:f}')
def step_es_tone(context, expected_tone, threshold):
    """
    Verifica que la respuesta de IA tiene el tono esperado.
    Tonos soportados: professional, friendly, formal, concise, empathetic
    Umbral: 0.0-1.0 (recomendado: 0.4-0.6)

    Ejemplo:
        Entonces el tono de la respuesta de IA debe ser "professional" con umbral 0.4
    """
    text = _get_response_text(context)
    evaluator = ToneEvaluator()
    result = evaluator.evaluate(response=text, expected_tone=expected_tone, threshold=threshold)
    assert result.passed, f"Verificación de tono FALLÓ: {result.reason}"


@step('la respuesta de IA debe cubrir los temas requeridos con umbral {threshold:f}')
def step_es_completeness(context, threshold):
    """
    Verifica que la respuesta de IA cubre todos los temas de la tabla.
    Columna de la tabla: tema
    Umbral: 0.0-1.0 (recomendado: 0.7-0.9)

    Ejemplo:
        Entonces la respuesta de IA debe cubrir los temas requeridos con umbral 0.8
          | tema   |
          | GET    |
          | POST   |
          | DELETE |
    """
    text = _get_response_text(context)
    topics = [row["tema"] for row in context.table]
    evaluator = CompletenessEvaluator()
    result = evaluator.evaluate(response=text, required_topics=topics, threshold=threshold)
    assert result.passed, (
        f"Completitud FALLÓ: {result.reason}\n"
        f"Temas faltantes: {result.details.get('missing', [])}"
    )


# ===========================================================================
# ESTRATEGIA 3 — LLM como Juez
# ===========================================================================

@step('configuro el juez de IA con proveedor "{provider}" y modelo "{model}"')
def step_es_configure_judge(context, provider, model):
    """
    Configura un modelo de IA específico para actuar como juez.
    Si no se llama, el juez usa JUDO_AI_PROVIDER del .env.

    Ejemplo:
        Dado que configuro el juez de IA con proveedor "openai" y modelo "gpt-4o"
    """
    from .client import GenAIClient
    from .models import GenAIConfig
    key_map = {
        "openai": "JUDO_OPENAI_API_KEY",
        "claude": "JUDO_CLAUDE_API_KEY",
        "gemini": "JUDO_GEMINI_API_KEY",
    }
    api_key = os.getenv(key_map.get(provider.lower(), "JUDO_AI_API_KEY"), "")
    config = GenAIConfig(provider=provider.lower(), api_key=api_key, model=model)
    context._judo_ai_judge_client = GenAIClient(config)
    context._judo_ai_judge = GenAIJudge(context._judo_ai_judge_client)


@step('establezco el criterio del juez como "{criteria}"')
def step_es_set_judge_criteria(context, criteria):
    """Almacena el criterio de evaluación para usarlo en pasos del juez."""
    context._judo_judge_criteria = criteria


@step('establezco el criterio del juez')
def step_es_set_judge_criteria_multiline(context):
    """Almacena criterios de evaluación multilínea."""
    context._judo_judge_criteria = context.text.strip()


@step('establezco el prompt del juez como "{prompt}"')
def step_es_set_judge_prompt(context, prompt):
    """Almacena el prompt/pregunta original para contexto del juez."""
    context._judo_judge_prompt = prompt


@step('evalúo la respuesta de IA con el juez usando criterio "{criteria}" y umbral {threshold:f}')
def step_es_judge_evaluate(context, criteria, threshold):
    """
    Usa un LLM como juez para evaluar la respuesta de IA según los criterios dados.
    El juez retorna una puntuación (0.0-1.0), veredicto (PASS/FAIL) y razonamiento.

    Ejemplo:
        Entonces evalúo la respuesta de IA con el juez usando criterio "La respuesta debe explicar claramente las APIs REST y mencionar los métodos HTTP." y umbral 0.7
    """
    text = _get_response_text(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
    )


@step('evalúo la respuesta de IA con el juez usando umbral {threshold:f}')
def step_es_judge_evaluate_multiline(context, threshold):
    """
    Usa un LLM como juez con criterios multilínea desde un bloque de texto.

    Ejemplo:
        Entonces evalúo la respuesta de IA con el juez usando umbral 0.7
          \"\"\"
          La respuesta debe:
          1. Ser precisa y factual
          2. Ser concisa (menos de 200 palabras)
          3. Usar lenguaje profesional
          \"\"\"
    """
    text = _get_response_text(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    criteria = context.text.strip()
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
    )


@step('evalúo la respuesta de IA con el juez contra el contexto RAG usando criterio "{criteria}" y umbral {threshold:f}')
def step_es_judge_evaluate_rag(context, criteria, threshold):
    """
    Usa un LLM como juez para evaluar la respuesta contra el contexto RAG.
    El juez recibe el contexto como verdad de referencia para evaluación factual.

    Ejemplo:
        Entonces evalúo la respuesta de IA con el juez contra el contexto RAG usando criterio "La respuesta debe ser consistente con la documentación proporcionada." y umbral 0.7
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
        context=rag_ctx,
    )


@step('evalúo la respuesta de IA con el juez contra el contexto RAG usando umbral {threshold:f}')
def step_es_judge_evaluate_rag_multiline(context, threshold):
    """
    LLM como juez contra contexto RAG con criterios multilínea.

    Ejemplo:
        Entonces evalúo la respuesta de IA con el juez contra el contexto RAG usando umbral 0.7
          \"\"\"
          La respuesta debe ser factualmente consistente con el contexto proporcionado.
          No debe introducir información que no esté presente en el contexto.
          \"\"\"
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    criteria = context.text.strip()
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
        context=rag_ctx,
    )


@step('la evaluación del juez debe pasar')
def step_es_judge_pass(context):
    """Verifica que la evaluación del juez LLM pasó."""
    result = getattr(context, "_judo_judge_result", None)
    assert result, "No hay evaluación del juez disponible. Ejecuta un paso 'evalúo...' primero."
    assert result.passed, (
        f"La evaluación del juez FALLÓ.\n"
        f"Puntuación: {result.score:.2%} (umbral: {result.threshold:.0%})\n"
        f"Razonamiento: {result.reasoning}"
    )


@step('la puntuación del juez debe ser al menos {min_score:f}')
def step_es_judge_min_score(context, min_score):
    """Verifica que la puntuación del juez cumple un mínimo."""
    result = getattr(context, "_judo_judge_result", None)
    assert result, "No hay evaluación del juez disponible."
    assert result.score >= min_score, (
        f"Puntuación del juez {result.score:.2%} < mínimo {min_score:.0%}.\n"
        f"Razonamiento: {result.reasoning}"
    )


@step('imprimo el texto de respuesta de IA')
def step_es_print_response(context):
    """Imprime el texto de respuesta de IA actual para depuración."""
    text = getattr(context, "_judo_eval_text", None)
    if text:
        print(f"\n=== Texto de Respuesta de IA ===\n{text}\n================================\n")
    else:
        print("No hay texto de respuesta de IA establecido.")


@step('imprimo el resultado de la evaluación del juez')
def step_es_print_judge(context):
    """Imprime el resultado de la evaluación del juez para depuración."""
    result = getattr(context, "_judo_judge_result", None)
    if result:
        print(f"\n=== Evaluación del Juez ===")
        print(f"Veredicto  : {result.verdict}")
        print(f"Puntuación : {result.score:.2%}")
        print(f"Umbral     : {result.threshold:.0%}")
        print(f"Razonamiento: {result.reasoning}")
        print(f"===========================\n")
    else:
        print("No hay evaluación del juez disponible.")
