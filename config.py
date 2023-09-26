
api_key = "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"

# Abre el archivo de texto
with open('Exepcion.txt', 'r') as exep:
    # Lee el contenido del archivo y guárdalo en una variable
    cont_1 = exep.read()

# Exporta el contexto del sistema

Exep_una = cont_1

# Abre el archivo de texto
with open('Contexto.txt', 'r') as archivo:
    # Lee el contenido del archivo y guárdalo en una variable
    contenido = archivo.read()

# Exporta el contexto del sistema
contexto = contenido

Context_txt = {
        "role": "system",
        "content": contexto
    }