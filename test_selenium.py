# ===================== TEST DE IMPORTS =====================
print("🔍 Probando imports...")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import os
    import requests
    from tqdm import tqdm
    import time
    print("✅ ¡TODOS los imports funcionan correctamente!")
except Exception as e:
    print("❌ Error en los imports:")
    print(e)
# ========================================================