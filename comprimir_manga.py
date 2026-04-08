import os
import shutil

carpeta = input("Pega la ruta de la carpeta del manga (la que contiene todas las Cap_XXX): ").strip()
if os.path.exists(carpeta):
    nombre_zip = os.path.basename(carpeta.rstrip("\\/"))
    print("🗜️  Comprimiendo...")
    shutil.make_archive(nombre_zip, 'zip', carpeta)
    print(f"✅ ZIP creado: {nombre_zip}.zip")
else:
    print("❌ Carpeta no encontrada.")