import tkinter as tk
from tkinter import messagebox
import re

# Definición de patrones de expresiones regulares para tokens SQL
patterns = [
    (r'\bSELECT\b|\bselect\b', "SELECT"),
    (r'\bUPDATE\b|\bupdate\b', 'UPDATE'),
    (r'\bDELETE\b|\bdelete\b', 'DELETE'),
    (r'\bCREATE\b|\bcreate\b', 'CREATE'),
    (r'\bFROM\b|\bfrom\b', 'FROM'),
    (r'\bWHERE\b|\bwhere\b', 'WHERE'),
    (r'\bSET\b|\bset\b', 'SET'),
    (r'\bAND\b|\band\b', 'AND'),
    (r'\bOR\|\bor\b', 'OR'),
    (r'\b\d+\b', 'NUMBER'),  # Para números
    # Para identificadores (nombres de tablas, columnas, etc.)
    (r'\b\w+\b', 'IDENTIFIER'),
    (r'"', 'COMILLA'),
    (r'\*', 'ASTERISK'),  # Para el asterisco utilizado en SELECT *
    (r'[><=]+', 'OPERATOR'),  # Para el operador de igualdad
    (r';|,', 'SEMICOLON'),  # Para el punto y coma al final de la sentencia
    (r'\s+', None)  # Ignorar espacios en blanco y saltos de línea
]

# Función para analizar el código fuente y generar los tokens


def tokenize(source_code):
    tokens = []
    position = 0
    while position < len(source_code):
        match = None
        for pattern, token_type in patterns:
            regex = re.compile(pattern)
            match = regex.match(source_code, position)
            if match:
                value = match.group(0)
                if token_type:
                    tokens.append((token_type, value))
                break
        if not match:
            raise ValueError(
                f'Error de sintaxis en el código fuente victor: {source_code[position:]}')
        position = match.end()
    return tokens


# Función para analizar la sentencia SELECT y extraer el nombre de la tabla y la cláusula WHERE
def parse_select(tokens):
    
    
    if tokens[0][0] == 'SELECT':
        index = 0
        count = 0
        flag=False
        list_param={}
        
        for token in tokens:
            if token[0]=="FROM":
                index=count
                break           
            if token[0] == "IDENTIFIER":
                list_param[token[1]]=1
                flag=True
                
            count+=1
        
        if not flag:
            list_param[""]=1
            
        
        table_name = tokens[index+1][1]  # Nombre de la tabla
        where_tokens = tokens[index+3:]
        where_clause = ''.join(token[1] for token in where_tokens)

        return list_param, table_name, {where_clause}

    raise ValueError('Error de sintaxis en la sentencia SELECT.')

# Generación de código MQL correspondiente a cada sentencia SQL

# Generación de código MQL para SELECT


def generate_mql_select(list_param,table_name, where_clause):
    mql_code = f'db.{table_name}.find({where_clause},{list_param})'
    return mql_code

# Función principal para analizar el código fuente y generar el código MQL


def verifica_sintaxis(code):
    patron_sql = re.compile(r"\bSELECT\b\s*.*?[*\w]\s*\bFROM\b\s*\w+\s*\bWHERE\b\s*.*", re.IGNORECASE)
    resultado = patron_sql.findall(code)
    
    patron_sql_2 = re.compile(r"\bSELECT\b\s*.*?[*\w]\s*\bFROM\b\s*\w+\s*$", re.IGNORECASE)
    resultado_2 =patron_sql_2.findall(code)
    
    if len(resultado) <=0 and len(resultado_2)<=0:
        raise ValueError('Error de sintaxis en la sentencia SELECT.')  


def transpile(source_code):
    verifica_sintaxis(source_code)
    print("paso la la vida")
    tokens = tokenize(source_code)
    
    print(tokens)
    if tokens[0][0] == 'SELECT' or tokens[0][0] == 'select':
        list_param, table_name, where_clause = parse_select(tokens)
        return generate_mql_select(list_param,table_name, where_clause)
    elif tokens[0][0] == 'UPDATE' or tokens[0][0] == 'update':
        # Implementa la lógica para generar el código MQL de la sentencia UPDATE
        pass
    elif tokens[0][0] == 'DELETE' or tokens[0][0] == 'delete':
        # Implementa la lógica para generar el código MQL de la sentencia DELETE
        pass
    elif tokens[0][0] == 'CREATE' or tokens[0][0] == 'delete':
        # Implementa la lógica para generar el código MQL de la sentencia CREATE
        pass
    else:
        raise ValueError('Se esperaba una sentencia SQL válida.')

# Función para manejar el evento del botón "Transpilar"


def transpile_sql():
    sql_code = sql_entry.get("1.0", tk.END).strip()
    try:
        mql_code = transpile(sql_code)
        mql_text.delete("1.0", tk.END)
        mql_text.insert(tk.END, mql_code)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Crear ventana principal
window = tk.Tk()
window.title("Transpilador SQL a MQL")

# Crear etiqueta y campo de texto para ingresar código SQL
sql_label = tk.Label(window, text="Código SQL:")
sql_label.pack()
sql_entry = tk.Text(window, height=10, width=50)
sql_entry.pack()

# Crear botón "Transpilar"
transpile_button = tk.Button(window, text="Transpilar", command=transpile_sql)
transpile_button.pack()

# Crear etiqueta y campo de texto para mostrar código MQL generado
mql_label = tk.Label(window, text="Código MQL:")
mql_label.pack()
mql_text = tk.Text(window, height=10, width=50)
mql_text.pack()

# Ejecutar el bucle principal de la interfaz gráfica
window.mainloop()
