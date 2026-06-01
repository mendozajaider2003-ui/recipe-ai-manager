import requests
import json
import logging
from .config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_recipe_from_ingredients(ingredients: list) -> dict:
    if not ingredients:
        logger.warning("No ingredients provided")
        return {
            "nombre": "Sin Ingredientes",
            "ingredientes_json": [],
            "pasos_json": ["Añade ingredientes para generar una receta"],
            "tiempo": "0",
            "dificultad": "Fácil"
        }

    prompt = f"""
    Eres un chef experto. Genera una receta creativa usando algunos o todos estos ingredientes: {', '.join(ingredients)}.
    Responde ÚNICAMENTE en formato JSON con la siguiente estructura:
    {{
        "nombre": "Nombre de la receta",
        "ingredientes_json": ["ingrediente 1 con cantidad", "ingrediente 2 con cantidad"],
        "pasos_json": ["paso 1", "paso 2"],
        "tiempo": "tiempo estimado (ej: 30 min)",
        "dificultad": "Fácil/Media/Difícil"
    }}
    """
    
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    logger.info(f"Enviando petición a OpenRouter con ingredientes: {ingredients}")
    logger.info(f"Usando modelo: {settings.OPENROUTER_MODEL}")
    logger.info(f"API Key (primeros 20 chars): {settings.OPENROUTER_API_KEY[:20]}...")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers, 
            json=data,
            timeout=30
        )
        logger.info(f"Código de respuesta: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Error HTTP: {response.status_code} - {response.text}")
            return _fallback(ingredients, f"HTTP {response.status_code}")
        
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        logger.info(f"Respuesta de IA (primeros 200 chars): {content[:200]}...")
        
        # Intentar extraer el JSON si el modelo añade texto extra
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            json_str = content[start:end]
            logger.info("JSON extraído correctamente")
            recipe_data = json.loads(json_str)
        else:
            logger.info("No se encontraron llaves, parseando directamente")
            recipe_data = json.loads(content)
        
        # Asegurar formato correcto
        return {
            "nombre": recipe_data.get("nombre", "Receta sin nombre"),
            "ingredientes_json": recipe_data.get("ingredientes_json", []),
            "pasos_json": recipe_data.get("pasos_json", []),
            "tiempo": recipe_data.get("tiempo", "30 min"),
            "dificultad": recipe_data.get("dificultad", "Media")
        }
        
    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con OpenRouter")
        return _fallback(ingredients, "Timeout")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Error de conexión: {e}")
        return _fallback(ingredients, f"ConnectionError: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decodificando JSON: {e}")
        logger.error(f"Contenido que falló: {content[:500]}")
        return _fallback(ingredients, f"JSONDecodeError: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return _fallback(ingredients, str(e))

def _fallback(ingredients: list, error_msg: str = "") -> dict:
    logger.error(f"Usando fallback. Error: {error_msg}")
    return {
        "nombre": "Receta de Emergencia",
        "ingredientes_json": ingredients,
        "pasos_json": ["Mezclar todos los ingredientes", "Cocinar a fuego medio", "¡Disfrutar!"],
        "tiempo": "15",
        "dificultad": "Fácil"
    }