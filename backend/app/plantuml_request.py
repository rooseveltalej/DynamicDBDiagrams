from fastapi import HTTPException
import requests
import zlib
import base64

def format_schema(schema):
    """Formatea el scheme recibido de la conexión a las BD para usarse en plantUML"""
    tables = {}
    relationships = set()

    for row in schema:
        table_name = row[1]  # Cambiado a índice 1 para el nombre de la tabla
        column_name = row[2]
        data_type = row[3]
        pk_status = row[4]
        fk_source_table = row[5]
        fk_source_column = row[6]
        fk_target_table = row[7]
        fk_target_column = row[8]

        if table_name not in tables:
            tables[table_name] = []

        tables[table_name].append((column_name, data_type, pk_status))

        if fk_source_table and fk_target_table:
            relationships.add((fk_source_table, fk_source_column, fk_target_table, fk_target_column))

    uml_output = "@startuml\n\n"

    for table, columns in tables.items():
        uml_output += f"entity {table} {{\n"
        for column, data_type, pk_status in columns:
            uml_output += f"  + {column}: {data_type}\n" if pk_status == 'PK' else f"  {column}: {data_type}\n"
        uml_output += "}\n\n"

    for source_table, source_column, target_table, target_column in relationships:
        uml_output += f"{source_table} ||--o{{ {target_table} : \"{source_column} -> {target_column}\"\n"

    uml_output += "@enduml"

    print(uml_output)
    return uml_output

def encode_plantuml(text):
    # Remove the zlib header (first two bytes) and the checksum (last four bytes)
    zlibbed_str = zlib.compress(text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]

    # Encode to base64
    encoded = base64.b64encode(compressed_string)

    # Translate base64 to PlantUML's encoding alphabet
    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    base64_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    translation_table = str.maketrans(base64_alphabet, plantuml_alphabet)

    # Return the translated string
    return encoded.decode('utf-8').translate(translation_table)

def generate_uml_image(encoded_text):
    # Base URL for PlantUML server
    base_url = "http://www.plantuml.com/plantuml/png/"

    # Full URL with encoded UML text
    full_url = base_url + encoded_text

    # Make the request
    response = requests.get(full_url)

    print(full_url)

    # Save the resulting image
    if response.status_code == 200:
        with open("uml_diagram.png", "wb") as file:
            file.write(response.content)
        print("Image generated and saved as uml_diagram.png")
    else:
        print(f"Error generating diagram: {response.status_code}")

    return(full_url)
