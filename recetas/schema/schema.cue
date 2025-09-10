#Receta: {
    titulo: string
    descripcion: string
    tiempo_preparacion: string
    dificultad: #Dificultad
    ingredientes: [...#Ingrediente]
    pasos: [...string]
    tags: [...string]
}

#Dificultad: "Fácil" | "Media" | "Dificil"
#Ingrediente: {
    nombre: string
    cantidad: string
}