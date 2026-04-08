from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
from tqdm import tqdm
import time
import re
import shutil

def limpiar_nombre(texto):
    texto = texto.replace("| Olympus Scanlation", "").strip()
    texto = re.sub(r'[^a-zA-Z0-9áéíóúñÁÉÍÓÚÑ\s-]', '', texto)
    texto = re.sub(r'\s+', '_', texto)
    return texto

def extraer_numero_capitulo(texto):
    match = re.search(r'(\d+)', texto)
    return int(match.group(1)) if match else 0

def descargar_manga_completo():
    url_serie = input("\n🔗 Pega la URL de la SERIE completa: ").strip()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    print("🚀 Iniciando navegador...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url_serie)
        print("⏳ Cargando lista completa de capítulos...")
        time.sleep(6)
        
        # Scroll dinámico en página de serie
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollBy(0, 2500)")
            time.sleep(1.0)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Extraer capítulos
        links = driver.find_elements("tag name", "a")
        capitulos = []
        for link in links:
            href = link.get_attribute("href") or ""
            texto = link.text.strip()
            if "/capitulo/" in href:
                num = extraer_numero_capitulo(texto or href)
                if num > 0 and not any(x in texto.lower() for x in [".5", ".1", ".2", "extra", "especial", "omake", "pausa"]):
                    capitulos.append((num, href, texto or f"Capítulo {num}"))
        
        capitulos = sorted(set(capitulos), key=lambda x: x[0])
        
        if not capitulos:
            print("❌ No se encontraron capítulos.")
            return
        
        min_cap = capitulos[0][0]
        max_cap = capitulos[-1][0]
        print(f"✅ Se encontraron {len(capitulos)} capítulos reales (del {min_cap} al {max_cap})")
        
        # ==================== SELECCIÓN DE RANGO ====================
        descargar_todos = input("\n¿Quieres descargar TODOS los capítulos? (s/n): ").strip().lower()
        
        if descargar_todos == "s":
            capitulos_a_descargar = capitulos[:]
        else:
            desde = int(input(f"Desde capítulo [{min_cap}]: ") or min_cap)
            hasta = int(input(f"Hasta capítulo [{max_cap}]: ") or max_cap)
            capitulos_a_descargar = [c for c in capitulos if desde <= c[0] <= hasta]
            
            if not capitulos_a_descargar:
                print("❌ No hay capítulos en ese rango.")
                return
        
        print(f"📌 Se van a descargar {len(capitulos_a_descargar)} capítulos.")
        
        # ==================== CONFIRMACIÓN CON TIEMPO ====================
        tiempo_estimado = len(capitulos_a_descargar) * 55
        horas = tiempo_estimado // 3600
        minutos = (tiempo_estimado % 3600) // 60
        print(f"⏱️  Tiempo estimado ≈ {horas}h {minutos}m")
        confirmar = input("¿Confirmas la descarga? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Operación cancelada.")
            return
        
        # ==================== DESCARGA ====================
        carpeta_manga = limpiar_nombre(driver.title)
        os.makedirs(carpeta_manga, exist_ok=True)
        
        for i, (num, url_cap, titulo_cap) in enumerate(capitulos_a_descargar, 1):
            print(f"\n📖 [{i}/{len(capitulos_a_descargar)}] Capítulo {num}")
            try:
                driver.get(url_cap)
                time.sleep(6)
                
                last_h = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollBy(0, 2200)")
                    time.sleep(0.9)
                    new_h = driver.execute_script("return document.body.scrollHeight")
                    if new_h == last_h:
                        break
                    last_h = new_h
                
                imgs = driver.find_elements("tag name", "img")
                count = 0
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                
                carpeta_cap = os.path.join(carpeta_manga, f"Cap_{num:03d}")
                os.makedirs(carpeta_cap, exist_ok=True)
                
                for img in tqdm(imgs, desc=f"Cap {num}", leave=False):
                    src = img.get_attribute("src") or img.get_attribute("data-src")
                    if not src or not (src.startswith("http") or src.startswith("/")):
                        continue
                    if src.startswith("/"):
                        src = "https://olympusbiblioteca.com" + src
                    
                    try:
                        r = requests.get(src, headers=headers, timeout=15)
                        if r.status_code == 200:
                            count += 1
                            with open(os.path.join(carpeta_cap, f"{count:03d}.jpg"), "wb") as f:
                                f.write(r.content)
                    except:
                        pass
                
                print(f"   ✅ {count} páginas")
                
            except Exception as e:
                print(f"   ❌ Falló Capítulo {num} → saltando")
                continue
        
        # ZIP final + borrar temporales
        zip_path = f"{carpeta_manga}.zip"
        print("\n🗜️ Creando ZIP final...")
        shutil.make_archive(carpeta_manga, 'zip', carpeta_manga)
        print(f"✅ ZIP creado: {zip_path}")
        shutil.rmtree(carpeta_manga)
        print("🗑️ Carpetas temporales borradas.")
        
    finally:
        driver.quit()
    
    print("\n🎉 ¡Proceso terminado!")

if __name__ == "__main__":
    descargar_manga_completo()