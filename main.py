import os
from threading import Thread
from flask import Flask
import discord
from discord import app_commands
from discord.ext import commands

# 1. Servidor web ligero con Flask para evitar que Render suspenda el servicio
app = Flask('')

@app.route('/')
def home():
    return "¡El bot de reclutamiento está activo!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# 2. Configuración del Bot de Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"¡Sincronizados {len(synced)} comandos! Conectado como {bot.user}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

@bot.tree.command(name="reclutar", description="Envía el mensaje oficial de reclutamiento de la UAGM.")
async def reclutar(interaction: discord.Interaction):
    nombre_imagen = "descarga (13).jpeg"

    # Verificar si la imagen está presente en el servidor
    if not os.path.exists(nombre_imagen):
        await interaction.response.send_message(
            f"❌ Error: No se encuentra el archivo '{nombre_imagen}' en el servidor.",
            ephemeral=True
        )
        return

    # Texto exacto solicitado con su decoración, enlace y formato original
    mensaje_publico = (
        "🇪🇸: 𝗘𝘀𝘁𝗲 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿 𝗵𝗮 𝘀𝗶𝗱𝗼 𝘀𝗲𝗹𝗲𝗰𝗰𝗶𝗼𝗻𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 𝗿𝗲𝗰𝗹𝘂𝘁𝗮𝗿 𝗺𝗶𝗲𝗺𝗯𝗿𝗼𝘀,𝗽𝗮𝗿𝗮 𝗹𝗮 𝗨𝗻𝗶ó𝗻 𝗔𝗻𝘁𝗶 𝗚𝗿𝘂𝗽𝗼𝘀 𝗠𝗮𝗹𝘃𝗮𝗱𝗼𝘀\n"
        "🇺🇸: 𝗧𝗵𝗶𝘀 𝘀𝗲𝗿𝘃𝗲𝗿 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝗲𝗹𝗲𝗰𝘁𝗲𝗱 𝘁𝗼 𝗿𝗲𝗰𝗿𝘂𝗶𝘁 𝗺𝗲𝗺𝗯𝗲𝗿𝘀 𝗳𝗼𝗿 𝘁𝗵𝗲 𝗔𝗻𝘁𝗶-𝗘𝘃𝗶𝗹 𝗚𝗿𝘂𝗽𝘀 𝗨𝗻𝗶𝗼𝗻.\n"
        "𝗟𝗜𝗡𝗞:\n"
        "https://discord.gg/xcdJRkhx7s"
    )

    archivo = discord.File(nombre_imagen)

    try:
        # Enviar el mensaje público directamente como respuesta a la interacción
        await interaction.response.send_message(
            content=mensaje_publico,
            file=archivo
        )
    except Exception as e:
        # Si algo falla, mandamos un aviso efímero solo para ti
        await interaction.followup.send(
            f"❌ Ocurrió un error al enviar el mensaje: {e}",
            ephemeral=True
        )

# 3. Arrancar Flask y el Bot simultáneamente
if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))
    
