from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()


def _generar_prompt(texto_bruto: str) -> str:
    """Construye prompt de extracción estructurada con reglas de normalización"""
    return f"""Eres un asistente experto en análisis de bitácoras de soporte técnico y soporte de aplicaciones (software).

TAREA: Analiza el siguiente texto transcrito de audio (puede contener errores de transcripción) y extrae información estructurada en formato JSON.

REGLAS DE CORRECCIÓN DE TRANSCRIPCIÓN:
- Corrige errores fonéticos comunes: "polisa" → "póliza", "aseguradora" → "aseguradora"
- Corrige nombres mal transcritos según contexto: "Ferretería Lopes" → "Ferretería López"
- Mantén números y cantidades tal como se mencionan
- Si una palabra no tiene sentido, infiere su significado por el contexto

REGLAS DE EXTRACCIÓN:

1. "cliente": (Nombre de la persona o contacto principal)
- Busca nombres propios de personas: "Sr. García", "Juan Pérez", "Doña María"
- Frases como: "habló con [nombre]", "atendí a [nombre]", "llamó [nombre]"
- Si solo hay nombre de negocio y no persona, usa "No especificado"
- Si no hay mención, usa "Desconocido"

2. "empresa": (Nombre del negocio o establecimiento)
- Busca nombres de negocios: "Refaccionaria García", "Ferretería López", "Taller Mecánico El Rápido"
- Patrones: "en [negocio]", "del negocio [nombre]", "la empresa [nombre]"
- Tipos comunes: ferretería, refaccionaria, taller, farmacia, consultorio, papelería
- Si solo hay nombre de persona y no negocio, usa "No especificado"
- Si no hay mención, usa "Desconocido"

3. "poliza": (boolean)
- true SOLO si menciona explícitamente: "póliza", "poliza", "polisa", "tiene contrato", "soporte incluido", "servicio contratado", "cobertura", "está en garantía"
- Frases que indican true: "tiene póliza", "cliente con contrato", "está cubierto", "no cobra porque tiene póliza"
- false si dice: "sin póliza", "no tiene contrato", "servicio de pago", "se cobrará"
- En caso de duda o sin mención, usa false

4. "problema": (Descripción técnica del problema)
- Extrae el problema técnico principal sin interpretar demasiado
- Mantén términos técnicos mencionados: "switch", "router", "servidor", "impresora"
- Incluye síntomas específicos: "no hay internet", "impresora no responde", "sistema lento"
- Preserva detalles importantes: equipos afectados, errores mencionados
- Primera letra mayúscula, resto minúsculas salvo nombres propios
- Si no hay descripción clara, usa "Sin descripción del problema"

5. "solucion": (Acción realizada o resultado)
- Describe la solución o acción específica tomada
- Mantén procedimientos mencionados: "reiniciar", "configurar", "reemplazar", "actualizar"
- Incluye resultados si se mencionan: "quedó funcionando", "sigue pendiente", "se programó visita"
- Preserva detalles técnicos: componentes cambiados, configuraciones ajustadas
- Primera letra mayúscula
- Si no hay solución, usa "Pendiente de resolución"

6. "monto": (number)
- Extrae la cifra exacta mencionada sin símbolos
- "mil quinientos" → 1500, "dos mil" → 2000
- Términos de costo cero: "sin cargo", "gratis", "sin costo", "incluido en póliza", "cortesía" → 0.0
- Si dice "se cobrará", "pendiente de cotizar" pero no da monto → 0.0
- Si no se menciona monto, usa 0.0

FORMATO DE SALIDA (JSON sin formato Markdown):
{{{{
"cliente": "string",
"empresa": "string",
"poliza": boolean,
"problema": "string",
"solucion": "string",
"monto": number
}}}}

TEXTO TRANSCRITO (puede contener errores):
{texto_bruto}

IMPORTANTE: 
- Responde SOLO con el JSON válido
- NO agregues explicaciones, comentarios ni bloques de código Markdown
- Corrige errores ortográficos evidentes manteniendo el significado original
- Diferencia claramente entre nombre de persona (cliente) y nombre de negocio (empresa)"""


def _limpiar_respuesta(texto_respuesta: str) -> str:
    """Remueve delimitadores Markdown de respuesta del modelo"""
    texto_respuesta = texto_respuesta.strip()
    if texto_respuesta.startswith("```json"):
        texto_respuesta = texto_respuesta[7:]
    if texto_respuesta.startswith("```"):
        texto_respuesta = texto_respuesta[3:]
    if texto_respuesta.endswith("```"):
        texto_respuesta = texto_respuesta[:-3]
    return texto_respuesta.strip()


class IAService:
    """Implementa extracción estructurada mediante API de Gemini"""

    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    def estructurar_texto(self, texto_bruto: str) -> dict:
        """Ejecuta inferencia para extraer entidades estructuradas del texto"""
        prompt = _generar_prompt(texto_bruto)

        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.95,
                max_output_tokens=400,
            )
        )

        texto_respuesta = _limpiar_respuesta(response.text)
        return json.loads(texto_respuesta)
