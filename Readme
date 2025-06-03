Analizador y Evaluador de Fotos de Coches con IA (Google Gemini)
Este proyecto te permite analizar y evaluar automáticamente la calidad de las fotografías de coches extraídas de páginas web, utilizando el poder de la inteligencia artificial de Google Gemini. El script descarga las imágenes, las somete a un análisis detallado como si fueras un experto en fotografía publicitaria de coches, y genera informes con puntos fuertes, áreas de mejora, sugerencias y una puntuación para cada foto, además de un veredicto global para el conjunto de imágenes.
Características Principales
Extracción de URLs de Imágenes: Localiza y extrae las URLs de imágenes desde archivos XML/HTML previamente descargados.
Descarga Robusta de Imágenes: Descarga las imágenes con reintentos y manejo de errores.
Análisis Cualitativo con IA: Utiliza Google Gemini 2.0 Flash para realizar un análisis crítico y cualitativo de cada imagen, evaluando aspectos como iluminación, composición, nitidez, y potencial publicitario.
Generación de Puntuaciones: Asigna una puntuación individual a cada imagen y una puntuación global al conjunto.
Informes Detallados: Genera archivos de texto con análisis estructurados por imagen y un resumen crítico final del conjunto de fotografías.
Limpieza Automática: Elimina las imágenes temporales una vez finalizado el análisis.
Requisitos
Asegúrate de tener Python 3.x instalado en tu sistema.
Librerías de Python
Necesitas instalar las siguientes librerías de Python. Puedes hacerlo abriendo tu terminal o símbolo del sistema y ejecutando el siguiente comando:
pip install requests beautifulsoup4 Pillow google-generativeai


Configuración y Uso Detallado
1. Obtén tu Clave de API de Google Gemini
Este es el paso más crucial. Para usar la inteligencia artificial de Gemini, necesitas una clave de API.
Ve a Google AI Studio.
Inicia sesión con tu cuenta de Google.
Crea un nuevo proyecto o selecciona uno existente.
Haz clic en "Get API key in a new project" (o busca tus claves API existentes).
Copia tu clave de API.
2. Prepara tus Archivos XML/HTML
El script está diseñado para leer archivos XML/HTML que ya hayas descargado. Asegúrate de que estos archivos se llamen siguiendo el patrón coches_elia_X.xml (donde X es un número) y que estén en la misma carpeta donde vas a guardar el script, o especifica su ruta.
3. Guarda el Código del Analizador
Copia el código principal del analizador (el que comienza con import logging...) y guárdalo en un archivo llamado analizador_fotos.py (o el nombre que prefieras, pero con extensión .py) en la misma carpeta que tus archivos coches_elia_X.xml.
4. Edita el Código del Analizador
Abre analizador_fotos.py con un editor de texto (como VS Code, Notepad++, Sublime Text, o incluso el Bloc de Notas).
Inserta tu Clave de API:
Busca la línea GOOGLE_API_KEY = "AIzaSyCLJeV91S0LfiYf-7XHJO7AbqyaewAtPII" y reemplaza "AIzaSyCLJeV91S0LfiYf-7XHJO7AbqyaewAtPII" con la clave de API de Google Gemini que copiaste en el Paso 1.
# ¡¡¡REEMPLAZA "TU_API_KEY_AQUI" CON TU CLAVE DE API DE GEMINI REAL Y VÁLIDA!!!
GOOGLE_API_KEY = "TU_API_KEY_AQUI" # <<< ¡REEMPLAZA ESTO!


Ajusta el Rango de Archivos XML (Opcional):
Por defecto, el script busca archivos desde coches_elia_1.xml hasta coches_elia_103.xml. Si tienes un número diferente de archivos o si no comienzan desde 1, ajusta el rango en la función main():
# Iterar sobre los archivos XML (ajusta el rango según tus necesidades, ej. range(1, 104) para todos)
for i in range(1, 104): # Esto procesa desde coches_elia_1.xml hasta coches_elia_103.xml
    # Si tus archivos van de 5 a 50, sería: for i in range(5, 51):
    # Si solo tienes uno llamado "mi_coche.xml", tendrías que cambiar la lógica para un solo archivo.
    # Por ejemplo, para un solo archivo:
    # xml_file_name = "mi_coche.xml"
    # xml_file_path = os.path.join(XML_FILES_DIR, xml_file_name)
    # (y el resto del código iría sin el bucle for)


Cambia el Directorio de Entrada (Opcional):
Si tus archivos coches_elia_X.xml no están en la misma carpeta que el script, puedes especificar su ubicación:
XML_FILES_DIR = "."  # Esto significa el directorio actual.
# Para una ruta específica: XML_FILES_DIR = "C:/Users/TuUsuario/Documentos/MisXMLCoches"
# O en Linux/macOS: XML_FILES_DIR = "/home/tu_usuario/documentos/mis_xml_coches"


5. Ejecuta el Programa
Abre tu terminal o símbolo del sistema.
Navega a la carpeta donde guardaste analizador_fotos.py (y tus archivos XML). Puedes usar el comando cd:
cd C:\Ruta\Donde\Guardaste\Tu\Script
# Ejemplo en Windows: cd C:\Users\TuUsuario\Documentos\ProyectoCoches
# Ejemplo en Linux/macOS: cd ~/Documentos/ProyectoCoches


Ejecuta el script:
python analizador_fotos.py


Output Esperado
Mientras se ejecuta, verás mensajes en la terminal indicando el progreso:
Configuración de la API de Gemini.
Creación del directorio temporal para imágenes (temp_car_images).
Procesamiento de cada archivo XML/HTML (ej. coches_elia_1.xml).
Descarga y análisis de cada imagen individual.
Errores o advertencias si alguna imagen no se puede descargar o analizar.
Información sobre la limpieza de imágenes temporales.
Una vez finalizado, en la misma carpeta donde ejecutaste el script, encontrarás nuevos archivos de texto con nombres como analisis_fotos_coche_flash_1.txt, analisis_fotos_coche_flash_2.txt, etc. Cada uno de estos archivos contendrá:
Un encabezado indicando el archivo XML de origen.
El análisis detallado para cada imagen individual, incluyendo:
Descripción del Plano y Composición.
Evaluación Cualitativa (Puntos Fuertes, Áreas de Mejora, Sugerencias Específicas).
Puntuación Individual (0-10) y Justificación.
Una sección de Análisis Global del Conjunto de Fotografías de ese archivo XML, incluyendo:
Promedio de puntuación.
Análisis de Cobertura, Coherencia Visual, Variedad de Ángulos y Calidad Técnica General.
Valoraciones y Sugerencias de Mejora a nivel de conjunto.
Una sección de Puntuación Global y Veredicto del Conjunto, con una puntuación de 0-100 y una justificación crítica final.
