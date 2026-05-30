import pytest
import json
from app.core.llm import generate_recipe_from_ingredients


def test_construir_prompt_vacio():
    """Prueba que la función maneja lista vacía de ingredientes."""
    ingredientes = []
    resultado = generate_recipe_from_ingredients(ingredientes)
    
    assert isinstance(resultado, dict)
    assert "nombre" in resultado
    assert "ingredientes_json" in resultado
    assert "pasos_json" in resultado
    assert resultado["nombre"] != ""


def test_construir_prompt_con_ingredientes():
    """Prueba que la función genera receta con ingredientes válidos."""
    ingredientes = ["pollo", "arroz", "cebolla"]
    resultado = generate_recipe_from_ingredients(ingredientes)
    
    assert isinstance(resultado, dict)
    assert "nombre" in resultado
    assert "ingredientes_json" in resultado
    assert "pasos_json" in resultado
    assert resultado["nombre"] != ""
    
    # Verificar que los ingredientes estén en formato JSON
    assert isinstance(resultado["ingredientes_json"], str)
    assert isinstance(resultado["pasos_json"], str)


def test_construir_prompt_con_muchos_ingredientes():
    """Prueba que la función maneja muchos ingredientes."""
    ingredientes = ["pollo", "arroz", "cebolla", "tomate", "ajo", "sal", "pimienta", "aceite"]
    resultado = generate_recipe_from_ingredients(ingredientes)
    
    assert isinstance(resultado, dict)
    assert "nombre" in resultado
    assert len(resultado["nombre"]) > 0
    assert "ingredientes_json" in resultado
    assert "pasos_json" in resultado


def test_resultado_contiene_campos_requeridos():
    """Prueba que el resultado contiene todos los campos requeridos."""
    ingredientes = ["tomate", "queso"]
    resultado = generate_recipe_from_ingredients(ingredientes)
    
    campos_requeridos = ["nombre", "ingredientes_json", "pasos_json", "tiempo", "dificultad"]
    for campo in campos_requeridos:
        assert campo in resultado, f"Campo '{campo}' no encontrado en resultado"


def test_resultado_json_valido():
    """Prueba que los campos JSON son válidos."""
    ingredientes = ["pasta", "salsa"]
    resultado = generate_recipe_from_ingredients(ingredientes)
    
    # Intentar parsear los JSON
    try:
        ingredientes_parsed = json.loads(resultado["ingredientes_json"])
        pasos_parsed = json.loads(resultado["pasos_json"])
        
        assert isinstance(ingredientes_parsed, list)
        assert isinstance(pasos_parsed, list)
    except json.JSONDecodeError:
        pytest.fail("Los campos JSON no son válidos")
