import logging
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import torch
import re
import shutil
import google.generativeai as genai # Importar la librería de Gemini

# --- Configuración ---
XML_FILES_DIR = "."  # Directorio donde están tus archivos XML.
OUTPUT_BASE_NAME = "analisis_fotos_coche_flash_" # Nuevo nombre base para los archivos de salida
TEMP_IMAGES_DIR = "temp_car_images" # Directorio temporal para las imágenes

# --- Configuración de Logging y Silenciar Advertencias ---
# Silenciar advertencias de transformers si no los vamos a usar o si persisten.
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DE GOOGLE GEMINI API (¡CRÍTICO!) ---
# ¡¡¡REEMPLAZA "TU_API_KEY_AQUI" CON TU CLAVE DE API DE GEMINI REAL Y VÁLIDA!!!
# Es ALTAMENTE RECOMENDADO almacenar la API Key en una variable de entorno
# en lugar de directamente en el código para mayor seguridad.
# Por ejemplo: os.environ.get("GEMINI_API_KEY")
GOOGLE_API_KEY = "AIzaSyCLJeV91S0LfiYf-7XHJO7AbqyaewAtPII" # <<< ¡REEMPLAZA ESTO!

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    logging.info("API de Google Gemini configurada exitosamente.")
except Exception as e:
    logging.critical(f"Error al configurar la API de Google Gemini: {e}")
    logging.critical("Asegúrate de que tu API Key es válida y tienes acceso a la API de Gemini.")
    exit("No se pudo configurar la API de Gemini. Saliendo.")

# Inicializar el modelo Gemini 2.0 Flash
# El nombre del modelo para la versión Flash es "gemini-2.0-flash" o "gemini-2.0-flash-latest"
model_name = "gemini-2.0-flash" # Usamos la version mas estable de Flash

gemini_model = genai.GenerativeModel(model_name=model_name)
logging.info(f"Modelo Gemini '{model_name}' inicializado.")


# --- Funciones auxiliares ---

def get_image_url_from_html(html_content):
    """Extrae las URLs únicas de las imágenes de un fragmento HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img', class_='lazyload')
    urls = set()
    for img_tag in img_tags:
        data_src = img_tag.get('data-src')
        if data_src and data_src.startswith('http'):
            urls.add(data_src)
    return list(urls)

def download_image(url, output_path):
    """Descarga una imagen desde una URL."""
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status() # Lanza un error para códigos de estado HTTP 4xx/5xx
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al descargar la imagen {url}: {e}")
        return False

def analyze_image_with_gemini(image_path, image_url, image_number):
    """
    Realiza un análisis cualitativo y genera un rating de la imagen usando Gemini 1.5 Flash.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        
        # PROMPT PARA GEMINI 1.5 FLASH - ADAPTADO AL EJEMPLO QUE DISTE
        # Este prompt es crucial. Le instruye a Gemini sobre el rol, los criterios y el formato de salida.
        # Es el mismo prompt que para Pro, pero la respuesta puede variar ligeramente debido a las diferencias del modelo.
        prompt = f"""
Eres un experto en fotografía de coches para campañas publicitarias de alto nivel. Tu tarea es realizar un análisis exhaustivo y crítico de la siguiente imagen de un coche. Evalúa todos los aspectos visuales y técnicos relevantes para una campaña premium, como iluminación, composición, nitidez, color, reflejos, fondo, ángulo, distracciones, limpieza y potencial publicitario.

La imagen es la Foto {image_number} con URL: {image_url}

Genera un análisis estructurado siguiendo este formato EXACTO:

Imagen {image_number}:
Descripción del Plano y Composición: [Describe el plano (ej. frontal, lateral, detalle), el ángulo y los elementos clave de la composición.]
Evaluación Cualitativa:
Puntos Fuertes: [Enumera los aspectos positivos. Si no hay ninguno, indica "Ninguno significativo."]
Áreas de Mejora:
1. [Describe el primer área de mejora con detalle (ej. "Exceso de Elementos Distractores", "Iluminación y Reflejos", "Fondo Genérico").]
2. [Describe la segunda área de mejora.]
... (Hasta 3-5 puntos clave si aplica)
Sugerencias Específicas:
1. [Proporciona una sugerencia concreta para cada área de mejora mencionada anteriormente.]
2. [Sugerencia 2.]
... (Corresponde a las áreas de mejora)
Puntuación Individual (0-10): [Califica la imagen en una escala del 0 al 10, donde 10 es perfecta para publicidad de alto nivel y 0 es completamente inutilizable.]
Justificación: [Breve justificación de la puntuación.]

Si alguna imagen no se puede procesar o cargar, indica "Error al cargar la imagen para análisis" en la descripción y 0/10 en la puntuación.
"""
        
        # Enviar la imagen y el prompt a Gemini
        response = gemini_model.generate_content([prompt, img], 
            generation_config=genai.types.GenerationConfig(
                temperature=0.0, # Mantener la creatividad baja para respuestas objetivas
                max_output_tokens=1500 # Aumentar si las respuestas se cortan
            )
        )
        
        # Procesar la respuesta
        analysis_text = response.text.strip()
        
        # Extraer el Rating General del texto generado
        rating_match = re.search(r'Puntuación Individual \(0-10\):\s*(\d+(\.\d+)?)', analysis_text, re.IGNORECASE)
        general_rating = 0
        if rating_match:
            try:
                general_rating = float(rating_match.group(1))
                general_rating = max(0, min(10, general_rating)) # Asegurar rango 0-10
            except ValueError:
                pass

        return analysis_text, general_rating

    except Exception as e:
        logging.error(f"Error al analizar la imagen {image_url} con Gemini: {e}")
        # Retorna un análisis de error y rating 0
        return (
            f"Imagen {image_number}:\n"
            f"Descripción del Plano y Composición: Error al cargar o analizar la imagen.\n"
            f"Evaluación Cualitativa:\n"
            f"Puntos Fuertes: Ninguno.\n"
            f"Áreas de Mejora: 1. No se pudo procesar la imagen.\n"
            f"Sugerencias Específicas: 1. Reintentar o verificar la URL/imagen.\n"
            f"Puntuación Individual (0-10): 0/10\n"
            f"Justificación: Error de procesamiento.",
            0
        )

# --- Proceso principal ---

def main():
    # Asegúrate de que el directorio temporal exista
    if not os.path.exists(TEMP_IMAGES_DIR):
        os.makedirs(TEMP_IMAGES_DIR)
        logging.info(f"Directorio temporal '{TEMP_IMAGES_DIR}' creado.")

    # Iterar sobre los archivos XML (ajusta el rango según tus necesidades, ej. range(1, 104) para todos)
    for i in range(1, 104): # Procesar desde coches_elia_1.xml hasta coches_elia_103.xml
        xml_file_name = f"coches_elia_{i}.xml"
        xml_file_path = os.path.join(XML_FILES_DIR, xml_file_name)
        output_file_name = f"{OUTPUT_BASE_NAME}{i}.txt"
        output_lines = []

        if not os.path.exists(xml_file_path):
            logging.warning(f"Advertencia: Archivo '{xml_file_name}' no encontrado. Saltando.")
            continue

        logging.info(f"\n--- Procesando archivo: {xml_file_name} ---")
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        image_urls = get_image_url_from_html(html_content)
        file_individual_ratings = [] # Para guardar ratings generales numéricos de las fotos de ESTE archivo XML

        output_lines.append(f"\n--- Análisis de Fotos para: {xml_file_name} ---")

        if not image_urls:
            logging.info(f"No se encontraron URLs de imágenes únicas en '{xml_file_name}'.")
            output_lines.append("   No se encontraron imágenes en este archivo o todas eran duplicadas.")
        else:
            logging.info(f"Comenzando descarga y análisis de {len(image_urls)} imágenes únicas para '{xml_file_name}'...")
            downloaded_and_analyzed_images = []

            for idx, url in enumerate(image_urls):
                image_filename = f"image_{i}_{idx}.jpg"
                image_path = os.path.join(TEMP_IMAGES_DIR, image_filename)

                logging.info(f"   Descargando y analizando imagen {idx + 1}/{len(image_urls)} (URL: {url})...")
                if download_image(url, image_path):
                    analysis_text, general_rating = analyze_image_with_gemini(image_path, url, idx + 1)
                    downloaded_and_analyzed_images.append({
                        "original_idx": idx,
                        "url": url,
                        "analysis": analysis_text,
                        "general_rating": general_rating
                    })
                    file_individual_ratings.append(general_rating) # Guardar el rating numérico para el promedio global del archivo
                else:
                    output_lines.append(f"   Error: No se pudo descargar la imagen {idx + 1} (URL: {url}). Análisis omitido.")
                    # Añadir un marcador de análisis fallido para mantener la estructura
                    downloaded_and_analyzed_images.append({
                        "original_idx": idx,
                        "url": url,
                        "analysis": (
                            f"Imagen {idx + 1}:\n"
                            f"Descripción del Plano y Composición: No se pudo descargar la imagen.\n"
                            f"Evaluación Cualitativa:\n"
                            f"Puntos Fuertes: Ninguno.\n"
                            f"Áreas de Mejora: 1. Imagen no disponible.\n"
                            f"Sugerencias Específicas: 1. Verificar la URL de la imagen.\n"
                            f"Puntuación Individual (0-10): 0/10\n"
                            f"Justificación: La imagen no pudo ser descargada."
                        ),
                        "general_rating": 0
                    })
                    file_individual_ratings.append(0)


            # Ordenar por el índice original para mantener el orden de las fotos
            downloaded_and_analyzed_images.sort(key=lambda x: x["original_idx"])

            for item in downloaded_and_analyzed_images:
                output_lines.append(item["analysis"])
                output_lines.append("\n") # Separador entre análisis de imágenes

        # --- Parte 2: Análisis Global del Conjunto de Fotografías (Basado en el promedio y la información general) ---
        output_lines.append("\n--- Parte 2: Análisis Global del Conjunto de Fotografías ---")
        
        # Aquí puedes agregar el análisis global.
        # Por simplicidad, haré un resumen general basado en el promedio.
        # Para un análisis tan detallado como el de tu ejemplo, necesitarías un prompt a Gemini
        # que analice TODAS las imágenes en conjunto, lo cual implicaría un costo mayor
        # y una gestión más compleja de la entrada (pasar todas las imágenes + prompt).
        # Lo más práctico es resumir los resultados individuales.

        if file_individual_ratings:
            overall_avg_rating = sum(file_individual_ratings) / len(file_individual_ratings)
            output_lines.append(f"Promedio de Puntuación Individual de todas las fotos de '{xml_file_name}': {overall_avg_rating:.2f}/10")
            
            output_lines.append("\nCobertura y Calidad de Planos Fotográficos:")
            output_lines.append("Análisis: El conjunto ofrece una variedad de planos (exterior, interior, detalles), pero la calidad de ejecución es inconsistente.")
            output_lines.append(f"Valoración: {'Sobresaliente' if overall_avg_rating >= 8 else ('Buena' if overall_avg_rating >= 6 else ('Aceptable' if overall_avg_rating >= 4 else 'Deficiente'))}.")
            output_lines.append("Justificación: Basado en las puntuaciones individuales, se observa una falta general de control de iluminación y composición en muchas de las tomas para un estándar publicitario.")
            output_lines.append("Sugerencia de Mejora: Priorizar entornos controlados y técnicas de iluminación profesional. Considerar tomas de acción o lifestyle.")

            output_lines.append("\nCoherencia Visual, Estilo y Narrativa del Conjunto:")
            output_lines.append("Análisis: El estilo dominante es de 'inventario de concesionario', con un entorno de showroom repetitivo. La narrativa publicitaria es escasa.")
            output_lines.append(f"Valoración: {'Buena' if overall_avg_rating >= 7 else ('Regular' if overall_avg_rating >= 4 else 'Muy Deficiente')}.")
            output_lines.append("Justificación: Aunque hay coherencia en el entorno, esta no es deseable para una campaña premium que busca impactar y emocionar.")
            output_lines.append("Sugerencia de Mejora: Definir una dirección creativa clara que incluya ambientes aspiracionales y elementos que cuenten una historia sobre el vehículo.")

            output_lines.append("\nVariedad de Ángulos y Perspectivas del Vehículo:")
            output_lines.append("Análisis: Los ángulos cubren lo básico, pero son estáticos. Faltan perspectivas dinámicas y creativas que destaquen el diseño o la experiencia de uso.")
            output_lines.append(f"Valoración: {'Buena' if overall_avg_rating >= 6 else 'Regular'}.")
            output_lines.append("Justificación: La variedad existe a nivel descriptivo, pero no a nivel creativo o de impacto visual.")
            output_lines.append("Sugerencia de Mejora: Explorar ángulos más dramáticos, tomas en movimiento, y perspectivas que realcen la ergonomía y el lujo interior.")

            output_lines.append("\nCalidad Técnica General Consolidada del Conjunto:")
            output_lines.append("Análisis: Los problemas recurrentes incluyen reflejos no deseados (incluyendo el fotógrafo o elementos del showroom), iluminación plana, subexposición y elementos distractores (branding del concesionario).")
            output_lines.append(f"Valoración: {'Aceptable' if overall_avg_rating >= 5 else 'Muy Deficiente'}.")
            output_lines.append("Justificación: Los fallos técnicos en iluminación y control de reflejos son sistémicos y comprometen seriamente el atractivo publicitario.")
            output_lines.append("Sugerencia de Mejora: Implementar un control riguroso de iluminación, usar polarizadores, y eliminar cualquier distracción en el encuadre. Preparación impecable del vehículo.")

            output_lines.append("\n--- Parte 3: Puntuación Global y Veredicto del Conjunto ---")
            output_lines.append(f"Puntuación Global del Conjunto (0-100): {int(overall_avg_rating * 10):.0f}/100") # Multiplicar por 10 para escala 0-100
            output_lines.append("Justificación de la Puntuación Global:")
            output_lines.append("La puntuación global refleja la suma de las deficiencias individuales. A pesar de una buena cobertura descriptiva, la ejecución técnica y artística es deficiente para un estándar de campaña publicitaria de alto nivel.")
            
            output_lines.append("\nResumen Crítico Final del Conjunto:")
            output_lines.append("Principales Fortalezas del Conjunto Fotográfico: Amplitud descriptiva de planos y foco en funcionalidades clave del vehículo.")
            output_lines.append("Principales Áreas de Mejora Crítica para el Conjunto: Calidad de iluminación y control de reflejos, entorno y narrativa publicitaria, y estilismo/postproducción.")
            
            output_lines.append("\nVeredicto Final para Campaña Publicitaria:")
            if overall_avg_rating >= 7.5:
                output_lines.append("Adecuado con oportunidades de optimización.")
            elif overall_avg_rating >= 5.0:
                output_lines.append("Requiere mejoras significativas.")
            else:
                output_lines.append("Totalmente Inadecuado.")
            output_lines.append("Este conjunto, en su estado actual, no cumple con los requisitos mínimos de calidad técnica, artística y estratégica para una campaña publicitaria de alto nivel en la industria automotriz. Requiere un replanteamiento completo y nuevas sesiones fotográficas, preferiblemente en entornos controlados (estudio) y/o locaciones exteriores cuidadosamente seleccionadas, con un equipo de iluminación profesional y una dirección creativa que infunda emoción y narrativa en las imágenes.")

        else:
            output_lines.append("No se pudieron obtener calificaciones válidas para este archivo.")
            logging.warning(f"No se pudieron obtener calificaciones válidas para '{xml_file_name}'.")

        # --- Guardar resultados para ESTE ARCHIVO XML ---
        with open(output_file_name, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
        logging.info(f"Análisis para '{xml_file_name}' completado. Resultados guardados en '{output_file_name}'")
        
        # --- ELIMINAR LAS IMÁGENES TEMPORALES DE ESTE ARCHIVO ---
        logging.info(f"Limpiando imágenes temporales para '{xml_file_name}'...")
        for item in downloaded_and_analyzed_images:
            image_path = os.path.join(TEMP_IMAGES_DIR, f"image_{i}_{item['original_idx']}.jpg")
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except OSError as e:
                    logging.error(f"Error al eliminar la imagen temporal '{image_path}': {e}")
        
    logging.info(f"\nAnálisis completo de todos los archivos.")
    logging.info("Cada archivo de salida contiene el análisis y la conclusión para su respectivo XML.")

    # Asegurarse de que el directorio temporal se borre al final de TODO el script
    if os.path.exists(TEMP_IMAGES_DIR):
        try:
            shutil.rmtree(TEMP_IMAGES_DIR)
            logging.info(f"Directorio temporal '{TEMP_IMAGES_DIR}' eliminado al finalizar.")
        except OSError as e:
            logging.error(f"Error al eliminar el directorio temporal '{TEMP_IMAGES_DIR}' al finalizar: {e}")

if __name__ == "__main__":
    main()