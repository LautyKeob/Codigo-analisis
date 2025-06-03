import requests
import os
import time # Importa la librería time para añadir pausas

def descargar_pagina(url, nombre_archivo, max_intentos=3, retardo_reintento=5):
    """
    Descarga el contenido de una URL y lo guarda en un archivo, con reintentos.

    Args:
        url (str): La URL de la página a descargar.
        nombre_archivo (str): El nombre del archivo donde se guardará el contenido.
        max_intentos (int): Número máximo de intentos para descargar la página.
        retardo_reintento (int): Segundos de espera entre reintentos.
    """
    for intento in range(1, max_intentos + 1):
        try:
            # Añadir un User-Agent para simular una petición de navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10) # Añadir un timeout
            response.raise_for_status()  # Lanza una excepción para códigos de estado de error HTTP

            # Verifica el Content-Type para advertir si no es XML
            content_type = response.headers.get('Content-Type', '')
            if 'xml' not in content_type.lower() and 'html' in content_type.lower():
                print(f"Advertencia: La URL '{url}' parece devolver contenido HTML. Content-Type: {content_type}. Se guardará de todas formas como '{nombre_archivo}'.")
            elif 'xml' not in content_type.lower():
                print(f"Advertencia: La URL '{url}' puede no devolver contenido XML. Content-Type: {content_type}. Se guardará de todas formas como '{nombre_archivo}'.")
            else:
                print(f"La URL '{url}' parece devolver contenido XML. Content-Type: {content_type}.")

            # Abre el archivo en modo de escritura binaria y guarda el contenido
            with open(nombre_archivo, 'wb') as f:
                f.write(response.content)
            print(f"Página descargada exitosamente como '{nombre_archivo}' en el intento {intento}.")
            return # Si la descarga es exitosa, sale de la función

        except requests.exceptions.Timeout:
            print(f"Intento {intento}/{max_intentos}: Tiempo de espera agotado al descargar '{url}'. Reintentando en {retardo_reintento} segundos...")
        except requests.exceptions.ConnectionError as e:
            print(f"Intento {intento}/{max_intentos}: Error de conexión al descargar '{url}': {e}. Reintentando en {retardo_reintento} segundos...")
        except requests.exceptions.RequestException as e:
            print(f"Intento {intento}/{max_intentos}: Error al descargar la página '{url}': {e}. Reintentando en {retardo_reintento} segundos...")
        except IOError as e:
            print(f"Intento {intento}/{max_intentos}: Error al escribir en el archivo '{nombre_archivo}': {e}.")
            break # Si hay un error de escritura, no tiene sentido reintentar la descarga

        # Esperar antes de reintentar
        if intento < max_intentos:
            time.sleep(retardo_reintento)

    print(f"Fallo al descargar '{url}' después de {max_intentos} intentos.")


if __name__ == "__main__":
    # Lista de URLs a descargar
    urls_a_descargar = [
         
       "https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-b4_d_core_auto_145_kw_197_cv/ocasion/59715573-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_plus_dark_auto_155_kw_211_cv/ocasion/59367432-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_recharge_phev_core_auto_155_kw_211_cv/ocasion/59367426-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b4_g_core_auto_145_kw_197_cv/ocasion/59166474-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/59129925-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_recharge_phev_core_auto_155_kw_211_cv/ocasion/58476555-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc90-t8_recharge_inscription_expression_awd_auto_335_kw_455_cv/ocasion/57954666-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t8_recharge_r_design_awd_auto_287_kw_390_cv/ocasion/56384412-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/56047410-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_plus_dark_auto_155_kw_211_cv/ocasion/56047392-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_plus_bright_auto_155_kw_211_cv/ocasion/56047386-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t5_recharge_plus_bright_auto_193_kw_262_cv/ocasion/55969566-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-s60-b4_g_core_fwd_auto_145_kw_197_cv/ocasion/55712343-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t2_core_auto_95_kw_129_cv/ocasion/55712319-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_192_kw_261_cv/ocasion/55158577-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_twin_recharge_r_design_expression_auto_155_kw_211_cv/ocasion/54763408-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-t6_recharge_inscription_core_awd_auto_257_kw_350_cv/ocasion/54762958-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-s60-t8_recharge_ultimate_dark_auto_335_kw_455_cv/ocasion/54762928-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_plus_bright_auto_155_kw_211_cv/ocasion/54762916-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-b4_d_plus_dark_auto_145_kw_197_cv/ocasion/54762835-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-b4_d_plus_dark_auto_145_kw_197_cv/ocasion/54762832-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-b4_d_plus_dark_auto_145_kw_197_cv/ocasion/54762817-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_recharge_phev_essential_auto_155_kw_211_cv/ocasion/54762814-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_core_auto_155_kw_211_cv/ocasion/54762250-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_d_plus_dark_auto_145_kw_197_cv/ocasion/54762130-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-d4_momentum_awd_auto_140_kw_190_cv/ocasion/54761929-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_inscription_awd_auto_257_kw_350_cv/ocasion/54761896-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-t6_recharge_r_design_awd_auto_250_kw_340_cv/ocasion/54761875-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_ultimate_dark_auto_155_kw_211_cv/ocasion/54761815-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_recharge_phev_core_auto_155_kw_211_cv/ocasion/54761809-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-s60-t8_reccharge_core_auto_335_kw_455_cv/ocasion/54761803-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-b4_d_plus_dark_auto_145_kw_197_cv/ocasion/54761797-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t2_essential_auto_95_kw_129_cv/ocasion/54761674-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t2_core_auto_95_kw_129_cv/ocasion/54761500-es/",
"https://www.motorflash.com/coche-de_segunda_mano/peugeot-508-bluehdi_130_sands_allure_eat8_96_kw_130_cv/ocasion/54761497-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_d_essential_auto_145_kw_197_cv/ocasion/54761473-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t2_core_auto_95_kw_129_cv/ocasion/54761434-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_g_essential_auto_145_kw_197_cv/ocasion/54761422-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_core_awd_auto_257_kw_350_cv/ocasion/73972904-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_core_awd_auto_257_kw_350_cv/ocasion/73780801-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/73562314-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-c40-recharge_single_plus_auto_175_kw_238_cv/ocasion/73496443-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-ex30-single_motor_extended_range_core_auto_200_kw_272_cv/ocasion/73496440-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/73118492-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_192_kw_261_cv/ocasion/73118480-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/73118462-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/73118402-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/73118399-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t2_essential_auto_95_kw_129_cv/ocasion/72397085-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/72397055-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/71133901-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc90-t8_core_recharge_awd_auto_335_kw_455_cv/ocasion/69937502-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_core_awd_auto_257_kw_350_cv/ocasion/69725594-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_plus_dark_awd_auto_257_kw_350_cv/ocasion/69169400-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-c40-electrico_recharge_extended_plus_auto_185_kw_252_cv/ocasion/69169397-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/69169391-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_plus_dark_awd_auto_257_kw_350_cv/ocasion/69169382-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_core_awd_auto_257_kw_350_cv/ocasion/69169379-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-t6_recharge_inscription_core_awd_auto_257_kw_350_cv/ocasion/69169376-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_g_essential_auto_145_kw_197_cv/ocasion/69169373-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-s60-b4_g_core_fwd_auto_145_kw_197_cv/ocasion/69169367-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-single_recharge_core_auto_175_kw_238_cv/ocasion/69148180-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_plus_bright_auto_155_kw_211_cv/ocasion/69148177-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-single_recharge_core_auto_175_kw_238_cv/ocasion/69148171-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_plus_dark_auto_155_kw_211_cv/ocasion/69148168-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/69148165-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-single_recharge_plus_auto_175_kw_238_cv/ocasion/69148162-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/68820689-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_g_essential_auto_145_kw_197_cv/ocasion/68727866-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-c40-electrico_recharge_extended_plus_auto_185_kw_252_cv/ocasion/68670475-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_d_ultimate_dark_auto_145_kw_197_cv/ocasion/68572166-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_core_awd_auto_257_kw_350_cv/ocasion/68324330-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-recharge_single_extended_core_auto_185_kw_252_cv/ocasion/68227261-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t2_core_auto_95_kw_129_cv/ocasion/68227249-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/67943932-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/67943917-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/67943908-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_d_ultimate_dark_awd_auto_145_kw_197_cv/ocasion/67861486-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_core_awd_auto_257_kw_350_cv/ocasion/67825280-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_plus_dark_awd_auto_257_kw_350_cv/ocasion/67251836-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/67251830-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-b4_d_essential_auto_145_kw_197_cv/ocasion/67251812-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_plus_dark_awd_auto_257_kw_350_cv/ocasion/66782482-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-ex30-twin_motor_ultra_awd_auto_315_kw_428_cv/ocasion/66750596-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/66750590-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/66712925-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_phev_recharge_plus_bright_auto_155_kw_211_cv/ocasion/65889822-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_d_plus_dark_auto_145_kw_197_cv/ocasion/65350044-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t5_recharge_phev_plus_dark_auto_193_kw_262_cv/ocasion/65100249-es/",
"https://www.motorflash.com/coche-de_segunda_mano/lynk_and_co-01-1_5_phev_6_6kw_192_kw_261_cv/ocasion/64896495-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_plus_dark_awd_auto_257_kw_350_cv/ocasion/64585803-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-c40-electrico_recharge_core_auto_175_kw_238_cv/ocasion/64585794-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_d_ultimate_dark_awd_auto_145_kw_197_cv/ocasion/64585791-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-s90-t8_twin_recharge_core_bright_awd_at_335_kw_455_cv/ocasion/64512342-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-b3_g_core_auto_120_kw_163_cv/ocasion/64117201-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-s60-b4_g_core_fwd_auto_145_kw_197_cv/ocasion/63658732-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-v60-d3_momentum_110_kw_150_cv/ocasion/63354829-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t4_recharge_phev_core_auto_155_kw_211_cv/ocasion/62580073-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-t5_phev_recharge_plus_dark_auto_193_kw_262_cv/ocasion/62580070-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc40-recharge_ultimate_electrico_auto_185_kw_252_cv/ocasion/62580025-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-t6_recharge_core_awd_auto_257_kw_350_cv/ocasion/62001435-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-ex30-single_motor_extended_range_core_auto_200_kw_272_cv/ocasion/61679181-es/",
"https://www.motorflash.com/coche-de_segunda_mano/volvo-xc60-b4_d_core_auto_145_kw_197_cv/ocasion/59715618-es/",

    ]

    # Directorio actual donde se ejecutará el script
    directorio_actual = os.getcwd()
    print(f"Los archivos se guardarán en: {directorio_actual}")

    # Itera sobre las URLs y descarga cada una
    for i, url in enumerate(urls_a_descargar):
        # Genera un nombre de archivo único para cada página
        nombre_archivo_salida = f"coches_elia_{i+1}.xml"
        descargar_pagina(url, nombre_archivo_salida)
        # Añade una pausa entre la descarga de cada página para ser más "amigable" con el servidor
        time.sleep(2) # Pausa de 2 segundos entre cada URL
        print("-" * 30) # Separador para mejor legibilidad en la consola
