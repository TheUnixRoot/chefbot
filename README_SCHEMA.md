# Esquema de Recetas - Proyecto Kuzco

## Descripción

Este proyecto utiliza un esquema JSON para validar y estructurar los archivos de recetas. El esquema garantiza que todas las recetas tengan un formato consistente y contengan la información necesaria.

## Archivos del Esquema

- `schema_receta.json`: Esquema JSON Schema que define la estructura de las recetas
- `scripts/validar_recetas.py`: Script de Python para validar recetas contra el esquema

## Campos Requeridos

Cada receta **debe** incluir los siguientes campos:

- `titulo`: Nombre de la receta
- `descripcion`: Descripción breve de la receta
- `tiempo_preparacion`: Tiempo estimado (ej: "45 minutos")
- `dificultad`: Nivel de dificultad (Muy fácil, Fácil, Intermedio, Difícil, Muy difícil)
- `ingredientes`: Array de objetos con `nombre` y `cantidad`
- `pasos`: Array de strings con los pasos de preparación
- `tags`: Array de etiquetas para categorización

## Campos Opcionales

El esquema también soporta muchos campos opcionales para información adicional:

- `porciones`: Número de porciones
- `calorias_por_porcion`: Calorías aproximadas por porción
- `categoria`: Categoría principal (Desayuno, Almuerzo, Cena, etc.)
- `origen`: País o región de origen
- `tipo_cocina`: Array de tipos de cocina
- `temporada`: Temporadas recomendadas
- `equipo_necesario`: Equipos de cocina necesarios
- `consejos`: Consejos útiles para la preparación
- `variaciones`: Variaciones posibles de la receta
- `informacion_nutricional`: Información nutricional detallada
- `fecha_creacion`, `fecha_actualizacion`: Fechas de creación y actualización
- `autor`: Autor de la receta
- `fuente`: Fuente original
- `valoracion`: Valoración de 1-5 estrellas
- `imagen`: URL o ruta de la imagen

## Uso del Script de Validación

### Instalar dependencias

```bash
pip install jsonschema
```

### Validar todas las recetas

```bash
python scripts/validar_recetas.py
```

### Ver campos disponibles

```bash
python scripts/validar_recetas.py --campos
```

## Ejemplo de Receta Válida

```json
{
  "titulo": "Pizza Clásica",
  "descripcion": "Una receta tradicional y sencilla, llena de sabor a italia. Perfecta para cualquier ocasión.",
  "tiempo_preparacion": "45 minutos",
  "dificultad": "Fácil",
  "porciones": 4,
  "categoria": "Cena",
  "origen": "Italia",
  "ingredientes": [
    { 
      "nombre": "Harina", 
      "cantidad": "500 g" 
    },
    { 
      "nombre": "Sal", 
      "cantidad": "8 g" 
    },
    { 
      "nombre": "Levadura seca", 
      "cantidad": "7 g" 
    }
  ],
  "pasos": [
    "En un bol, mezcla la harina, la sal y la levadura seca.",
    "Añade el agua tibia y el aceite de oliva virgen extra.",
    "Mezcla hasta que se forme una masa suave y elástica."
  ],
  "tags": ["pizza", "clásica", "tradicional", "italiana", "queso"],
  "consejos": [
    "Deja reposar la masa en un lugar cálido para mejor fermentación",
    "Precalienta bien el horno para obtener una base crujiente"
  ]
}
```

## Validación Automática

El esquema incluye validaciones para:

- Tipos de datos correctos
- Longitudes mínimas y máximas de strings
- Valores enumerados para campos como dificultad y categoría
- Patrones regex para campos como tiempo de preparación
- Unicidad en arrays donde sea apropiado
- Rangos válidos para valores numéricos

## Beneficios del Esquema

1. **Consistencia**: Todas las recetas siguen la misma estructura
2. **Validación**: Detecta errores antes de procesar las recetas
3. **Documentación**: El esquema sirve como documentación de la estructura
4. **Integración**: Facilita la integración con herramientas de búsqueda y análisis
5. **Extensibilidad**: Fácil agregar nuevos campos manteniendo compatibilidad
