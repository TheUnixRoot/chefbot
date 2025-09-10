# ChefBot
Chatbot locally feed with recipes, using local chroma_db for searching and using ollama models to retrieve the right recipe upon your conversation with the model

## Requirements
- Python
- Cue for json validator schema, you can download it from github.com/cue-lang/cue/releases

## How to run/develop
Create a virtual environment like
```
python -m venv .py/venv
```
Activate the environment and run 
```
pip install -r requirements.txt
```
For running the interactive chatbot
```
streamlit run ./scripts/app.py
```
For validating
```
cue vet -c ./recetas/schema/schema.cue ./recetas/pizza.json
```
