import requests
import json
from .config import settings

def generate_recipe_from_ingredients(ingredients: list) -> dict:
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
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        
        # Intentar extraer el JSON si el modelo añade texto extra
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            json_str = content[start:end]
            return json.loads(json_str)
        return json.loads(content)
    except Exception as e:
        # Fallback en caso de error
        return {
            "nombre": "Receta de Emergencia",
            "ingredientes_json": ingredients,
            "pasos_json": ["Mezclar todo", "Cocinar hasta que esté listo"],
            "tiempo": "15 min",
            "dificultad": "Fácil"
        }
