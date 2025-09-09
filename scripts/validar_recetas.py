#!/usr/bin/env python3
"""
Script para validar archivos JSON de recetas contra el esquema definido.
"""

import json
import os
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator
import sys

# Definir rutas desde la raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
RECETAS_PATH = PROJECT_ROOT / "recetas"
SCHEMA_PATH = PROJECT_ROOT / "schema_receta.json"

def cargar_schema():
    """Carga el esquema JSON desde el archivo."""
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo de esquema en {SCHEMA_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: El archivo de esquema no es un JSON válido: {e}")
        sys.exit(1)

def validar_receta(archivo_receta, schema):
    """Valida una receta individual contra el esquema."""
    try:
        with open(archivo_receta, 'r', encoding='utf-8') as f:
            receta = json.load(f)
        
        # Crear validador
        validator = Draft202012Validator(schema)
        
        # Validar
        validator.validate(receta)
        return True, None
        
    except FileNotFoundError:
        return False, f"Archivo no encontrado: {archivo_receta}"
    except json.JSONDecodeError as e:
        return False, f"JSON inválido: {e}"
    except ValidationError as e:
        return False, f"Error de validación: {e.message}"
    except Exception as e:
        return False, f"Error inesperado: {e}"

def validar_todas_las_recetas():
    """Valida todas las recetas en el directorio."""
    print("🔍 Validando recetas contra el esquema...")
    print(f"📁 Directorio de recetas: {RECETAS_PATH}")
    print(f"📋 Esquema: {SCHEMA_PATH}")
    print("-" * 60)
    
    # Cargar esquema
    schema = cargar_schema()
    
    # Buscar archivos JSON
    archivos_json = list(RECETAS_PATH.glob("*.json"))
    
    if not archivos_json:
        print("⚠️  No se encontraron archivos JSON en el directorio de recetas.")
        return
    
    recetas_validas = 0
    recetas_invalidas = 0
    
    for archivo in archivos_json:
        print(f"\n📄 Validando: {archivo.name}")
        
        es_valida, error = validar_receta(archivo, schema)
        
        if es_valida:
            print(f"✅ {archivo.name} - VÁLIDA")
            recetas_validas += 1
        else:
            print(f"❌ {archivo.name} - INVÁLIDA")
            print(f"   Error: {error}")
            recetas_invalidas += 1
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 60)
    print(f"✅ Recetas válidas:   {recetas_validas}")
    print(f"❌ Recetas inválidas: {recetas_invalidas}")
    print(f"📋 Total procesadas:  {recetas_validas + recetas_invalidas}")
    
    if recetas_invalidas > 0:
        print(f"\n⚠️  Se encontraron {recetas_invalidas} receta(s) que no cumplen con el esquema.")
        print("   Revisa los errores mostrados arriba para corregirlas.")
        sys.exit(1)
    else:
        print(f"\n🎉 ¡Todas las recetas son válidas según el esquema!")

def mostrar_campos_requeridos():
    """Muestra los campos requeridos del esquema."""
    schema = cargar_schema()
    
    print("📋 CAMPOS REQUERIDOS EN EL ESQUEMA:")
    print("-" * 40)
    
    required_fields = schema.get('required', [])
    for field in required_fields:
        description = schema['properties'].get(field, {}).get('description', 'Sin descripción')
        print(f"• {field}: {description}")
    
    print(f"\n📝 CAMPOS OPCIONALES DISPONIBLES:")
    print("-" * 40)
    
    optional_fields = [field for field in schema['properties'].keys() if field not in required_fields]
    for field in optional_fields:
        description = schema['properties'].get(field, {}).get('description', 'Sin descripción')
        print(f"• {field}: {description}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--campos":
        mostrar_campos_requeridos()
    else:
        validar_todas_las_recetas()
