from flask import Flask, request, render_template
import ply.lex as lex

# Definición de 20 antónimos
antonimos = {
    "morir": "vivir",
    "alegría": "tristeza",
    "claro": "oscuro",
    "fácil": "difícil",
    "frío": "calor",
    "bueno": "malo",
    "viejo": "nuevo",
    "alto": "bajo",
    "lejos": "cerca",
    "rápido": "lento",
    "fuerte": "débil",
    "luz": "oscuridad",
    "entrada": "salida",
    "subir": "bajar",
    "ganar": "perder",
    "rico": "pobre",
    "día": "noche",
    "joven": "anciano",
    "inicio": "fin",
    "amor": "odio"
}

# Tokens del lexer
tokens = ['TOKEN', 'SIMBOLO', 'DIGITO']

t_ignore = ' \t'

# Función para manejar saltos de línea y contar líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_DIGITO(t):
    r'\d+'
    t.value = (t.value, '', '', 'x', t.lexer.lineno)  # Incluye el número de línea actual
    return t

def t_SIMBOLO(t):
    r'[^\w\s]'
    t.value = (t.value, '', 'x', '', t.lexer.lineno)  # Incluye el número de línea actual
    return t

def t_TOKEN(t):
    r'[a-zA-Z]+'
    if t.value in antonimos:
        t.value = (t.value, antonimos[t.value], '', '', t.lexer.lineno)  # Incluye el número de línea actual
    else:
        t.value = (t.value, '', '', '', t.lexer.lineno)
    return t

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Configuración de Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        text = request.form['text']
        lexer.lineno = 1  # Reinicia el contador de líneas para cada nueva entrada
        lexer.input(text)
        for tok in lexer:
            results.append(tok.value)
    return render_template('Antonimo.html', results=results, antonimos=antonimos)

if __name__ == '__main__':
    app.run(debug=True)
