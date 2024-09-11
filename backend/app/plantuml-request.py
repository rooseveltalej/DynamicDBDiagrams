import requests
import zlib
import base64
import urllib.parse

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

uml_text = """
@startuml
Alice -> Bob: Hello
Bob -> Alice: Hi
@enduml
"""

encoded_text = encode_plantuml(uml_text)
print(f"Encoded UML: {encoded_text}")

def generate_uml_image(encoded_text):
    # Base URL for PlantUML server
    base_url = "http://www.plantuml.com/plantuml/png/"
    
    # Full URL with encoded UML text
    full_url = base_url + encoded_text
    
    # Make the request
    response = requests.get(full_url)
    
    # Save the resulting image
    if response.status_code == 200:
        with open("uml_diagram.png", "wb") as file:
            file.write(response.content)
        print("Image generated and saved as uml_diagram.png")
    else:
        print(f"Error generating diagram: {response.status_code}")

generate_uml_image(encoded_text)
