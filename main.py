import discord
from discord.ext import commands
import random
import sqlite3

conn = sqlite3.connect("reto.db")
cursor = conn.cursor()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix= "¡", intents=intents)

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    user_id INTEGER PRIMARY KEY,
    retos_cumplidos INTEGER DEFAULT 0,
    agua INTEGER DEFAULT 0,
    sol INTEGER DEFAULT 0,
    abono INTEGER DEFAULT 0,
    nivel_de_crecimiento INTEGER DEFAULT 0 
)
''')
conn.commit()

@bot.event
async def on_ready():
    print(f"hemos iniciado sesion como{bot.user}")


@bot.command()
async def hola(ctx):
    await ctx.send("hola, soy un bot ecologico!")


@bot.command()
async def info(ctx):
    await ctx.send(
        "el cambio climatico es el aumento de temperatura global debido"
        "a la acumulacion de gases de efecto invernadero, que atrapan el"
        "calor en la atmosfera, esto provoca que las temperaturas aumenten"
        "los combustibles fosiles como el carbon, el petroleo y el gas natural"
        "son las fuentes principales de estas emisiones. El uso de estas en"
        "energia, transporte e industrias es masivo"
    )


@bot.command()
async def huella(ctx):
    def check(m):
        return m.author == ctx.author
    await ctx.send("cuantos kilometros viajas en auto por semana?")
    auto_km = await bot.wait_for("message", check=check)

    await ctx.send("¿Cuántas veces comes carne a la semana?")
    carne = await bot.wait_for("message", check=check)

    await ctx.send("¿Cuál es tu consumo mensual de electricidad (en kWh)?")
    electricidad = await bot.wait_for("message", check=check)

    try:
        km = float(auto_km.content)
        carne = int(carne.content)
        kwh = float(electricidad.content)

        co2_auto = km * 0.21 * 4 
        co2_carne = carne * 7 * 4
        co2_luz = kwh * 0.4

        total = co2_auto + co2_carne + co2_luz

        await ctx.send(
            f"Tu huella de carbono estimada mensual es de **{total:.2f} kg de CO2**.\n"
            "Este cálculo es solo una aproximación."
        )
    except ValueError:
        await ctx.send("Por favor, responde solo con números válidos.")

@bot.command()
async def consejo(ctx):
    cons_eco = ["Usa bombillas LED para ahorrar energía y durar mas",
            "Apaga luces y aparatos cuando no los uses!",
            "Compra alimentos locales y de temporada",
            "Cierra la llave mientras te cepillas los dientes",
            "Separa y recicla la basura correctamente"
            ]

    elegir_cons = random.choice(cons_eco)
    await ctx.send(f"un consejo seria {elegir_cons}")

@bot.command()
async def mito(ctx):
    mitos = ["El clima cambia solo por causas naturales, no por humanos",
             "El sol es el único responsable del calentamiento global",
             "El hielo polar no está disminuyendo ni derritiéndose",
             "No hay forma de frenar el cambio climático hoy en día",
             "El cambio climático solo afecta a lugares lejanos del planeta"
             ]
    mito = random.choice(mitos)
    await ctx.send(f"El mito falso es: {mito}")


@bot.command()
async def reflexion(ctx):
    reflexiones = ["Seguir ignorando el cambio climático no lo va a detener",
        "Cada acción cuenta, aunque parezca pequeña",
        "El futuro se construye con lo que haces hoy",
        "No heredes un problema que puedes evitar ahora",
        "Pensar en el planeta es pensar en tu propia vida",
        "No hay planeta B, solo decisiones A",
        "Si no cambias tú, nada va a cambiar de verdad",
        "El tiempo no espera a que te intereses en la ciencia",
        "Tu rutina puede ser parte del problema o de la solución",
        "Hacer nada también es una elección"
    ]
    reflexion = random.choice(reflexiones)
    await ctx.send(reflexion)

@bot.command()
async def reto(ctx):
    retos = ["Hoy, rechaza cualquier bolsa de plástico que te ofrezcan",
        "Camina o usa bici al menos una parte del trayecto",
        "Revisa tu casa y apaga luces innecesarias esta noche",
        "Publica un dato real sobre el cambio climático en redes",
        "Dúchate en menos de 5 minutos",
        "Separa tu basura correctamente al menos por un día",
       "Habla con alguien sobre el reciclaje hoy",
        "Lleva tu propio recipiente si compras comida para llevar",
        "Hoy no comas carne, busca una alternativa vegetal",
        "Investiga cómo bajar tu consumo de electricidad en casa"
    ]
    reto = random.choice(retos)
    await ctx.send(f"el reto es:{reto}")

@bot.command()
async def cumpli_reto(ctx):
    cursor.execute("select * from usuarios where user_id = ?" , (ctx.author.id,))
    usuario = cursor.fetchone()
    if usuario is None:
        cursor.execute("INSERT INTO usuarios (user_id, retos_cumplidos) VALUES (?, ?)", (ctx.author.id, 1))
    else:
        cursor.execute("UPDATE usuarios SET retos_cumplidos = retos_cumplidos + 1 WHERE user_id = ?", (ctx.author.id,))
    conn.commit()
    await ctx.send("¡Reto registrado! ¡Sigue así!")

@bot.command()
async def puntaje(ctx):
    cursor.execute("SELECT retos_cumplidos FROM usuarios WHERE user_id = ?", (ctx.author.id,))
    resultado = cursor.fetchone()

    if resultado is None:
        await ctx.send("Aún no has completado ningún reto. ¡Empieza hoy!")
    else:
        await ctx.send(f"Has completado {resultado[0]} retos. ¡Sigue así!")

@bot.command()
async def historias_inspiradoras(ctx):
    historias = [
        "La ciudad de Buenos Aires ha implementado un programa de reciclaje que ha mejorado su tasa de reciclaje considerablemente. Para más información, visita: https://www.buenosaires.gob.ar",
        "En Costa Rica, el 25 porciento del territorio está protegido como parque nacional. Para más información, visita: https://www.visitcostarica.com",
        "La comunidad de Capannori en Italia ha aumentado su tasa de reciclaje al 65 porciento en dos años. Para más información, visita: https://www.comune.capannori.lu.it",
        "En Colombia, el programa 'Basura Cero' busca reducir los residuos y promover el reciclaje. Para más información, visita: https://www.bogota.gov.co",
        "El programa de reforestación de la Fundación Arbor Day ha plantado millones de árboles en todo el mundo. Para más información, visita: https://www.arborday.org"
    ]
    await ctx.send(random.choice(historias))

def chequear_crecimiento(userid):
    cursor.execute("SELECT nivel_de_crecimiento, agua, sol, abono FROM usuarios WHERE user_id = ?", (userid,))
    resultado = cursor.fetchone()
    if resultado is None:
        return
    nivel, agua, sol, abono = resultado

    requisitos = [
        (0, 0, 0),  
        (2, 2, 2), 
        (4, 4, 4),  
        (6, 6, 6), 
        (8, 8, 8), 
        (10, 10, 10)
    ]

    if nivel >= len(requisitos) - 1:
        return  

    req_agua, req_sol, req_abono = requisitos[nivel]

    if agua >= req_agua and sol >= req_sol and abono >= req_abono:
        nuevo_nivel = nivel + 1
        cursor.execute(
            "UPDATE usuarios SET nivel_de_crecimiento = ?, agua = 0, sol = 0, abono = 0 WHERE user_id = ?",
            (nuevo_nivel, userid)
        )
        conn.commit()
        return nuevo_nivel
    return nivel


@bot.command()
async def tener_planta(ctx):
    await ctx.send("¡Bienvenido al minijuego donde tendrás una planta virtual!")
    userid = ctx.author.id

    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (userid,))
    resultado = cursor.fetchone()
    print(f"resultado: {resultado}")

    if resultado is None:
        cursor.execute("INSERT INTO usuarios (user_id, nivel_de_crecimiento) VALUES (?, 1)", (userid,))
        conn.commit()
        await ctx.send("¡Tu planta virtual ha sido plantada!")
    else:
        nivel = resultado[5] 
        if nivel >= 1:
            await ctx.send("¡Ya tienes una planta en crecimiento, cuídala!")
        else:
            cursor.execute("UPDATE usuarios SET nivel_de_crecimiento = 1 WHERE user_id = ?", (userid,))
            conn.commit()
            await ctx.send("¡Tu planta ha sido restaurada!")

@bot.command()
async def regar(ctx):
    userid = ctx.author.id
    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (userid,))
    resultado = cursor.fetchone()

    if resultado is None:
        await ctx.send("🚫 Aún no tienes ninguna planta!")
        return
    
    cursor.execute("UPDATE usuarios SET agua = agua + 1 WHERE user_id = ?", (userid,))
    conn.commit()

    nuevo_nivel = chequear_crecimiento(userid)
    if nuevo_nivel is not None and nuevo_nivel > resultado[5]:
        await ctx.send(f"¡Regaste tu planta! 🌱 Ha subido a nivel {nuevo_nivel} 🎉")
    else:
        await ctx.send("¡Regaste tu planta! 💧")

@bot.command()
async def abonar(ctx):
    userid = ctx.author.id
    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (userid,))
    resultado = cursor.fetchone()

    if resultado is None:
        await ctx.send("🚫 Aún no tienes ninguna planta!")
        return
    
    cursor.execute("UPDATE usuarios SET abono = abono + 1 WHERE user_id = ?", (userid,))
    conn.commit()

    nuevo_nivel = chequear_crecimiento(userid)
    if nuevo_nivel is not None and nuevo_nivel > resultado[5]:
        await ctx.send(f"¡Abonaste tu planta! 🌿 Ha subido a nivel {nuevo_nivel} 🎉")
    else:
        await ctx.send("¡Abonaste tu planta! 🌾")

@bot.command()
async def colocar_al_sol(ctx):
    userid = ctx.author.id
    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (userid,))
    resultado = cursor.fetchone()

    if resultado is None:
        await ctx.send("🚫 Aún no tienes ninguna planta!")
        return
    
    cursor.execute("UPDATE usuarios SET sol = sol + 1 WHERE user_id = ?", (userid,))
    conn.commit()

    nuevo_nivel = chequear_crecimiento(userid)
    if nuevo_nivel is not None and nuevo_nivel > resultado[5]:
        await ctx.send(f"¡Colocaste al sol tu planta! ☀️ Ha subido a nivel {nuevo_nivel} 🎉")
    else:
        await ctx.send("¡Colocaste al sol tu planta! ☀️")


@bot.command()
async def estado(ctx):
    userid = ctx.author.id
    cursor.execute("SELECT nivel_de_crecimiento, agua, sol, abono FROM usuarios WHERE user_id = ?", (userid,))
    resultado = cursor.fetchone()

    if resultado is None:
        await ctx.send("🚫 Aún no tienes ninguna planta!")
        return
    nivel, agua, sol, abono = resultado
    etapas = [
        "Semilla",
        "Brote",
        "Plantita",
        "Árbol joven",
        "Árbol adulto",
        "Planta legendaria 🗿"
    ]
    estado = (
        f"Estado de la planta:\n"
        f"Nivel: {nivel} - {etapas[nivel] if nivel < len(etapas) else 'leyenda verde'}\n"
        f"💧 Agua: {agua}\n"
        f"☀️ Sol: {sol}\n"
        f"🌾 Abono: {abono}"
    )

    await ctx.send(estado)

@bot.command()
async def dato_interesante(ctx):
    datos = [
        "El reciclaje ayuda a conservar los recursos naturales y a reducir la contaminación.",
        "Cada tonelada de papel reciclado salva aproximadamente 17 árboles.",
        "El vidrio puede reciclarse infinitas veces sin perder calidad.",
        "El plástico reciclado reduce el uso de combustibles fósiles.",
        "El compostaje convierte residuos orgánicos en abono para plantas."
    ]
    await ctx.send(random.choice(datos))

@bot.command()
async def hecho_curioso(ctx):
    hechos = [
        "El 30 porciento de la comida producida en el mundo se desperdicia cada año.",
        "Los océanos absorben cerca del 30 porciento del dióxido de carbono producido por los humanos.",
        "Una sola persona puede generar hasta 1 kilogramo de basura al día.",
        "Las abejas son responsables de la polinización de aproximadamente el 70 porciento de los cultivos mundiales.",
        "Las energías renovables ya generan más electricidad que el carbón en varios países."
    ]
    await ctx.send(random.choice(hechos))

@bot.command()
async def ecologia(ctx):
    preguntas_eco = [
        ("¿Qué gas es el principal causante del efecto invernadero?", ["dióxido de carbono", "co2", "dioxido de carbono"]),
        ("¿Cuál es una forma efectiva de reducir la contaminación plástica?", ["reciclar", "reutilizar", "reducir"]),
        ("¿Qué acción ayuda a conservar el agua?", ["cerrar la llave", "no desperdiciar agua", "ahorrar agua"]),
        ("¿Qué energía es renovable y no contamina?", ["solar", "eólica", "viento", "hidroeléctrica"]),
        ("¿Qué puedes plantar para ayudar a combatir el cambio climático?", ["árboles", "plantas", "árbol"]),
        ("¿Cuál es un residuo que se debe separar para reciclar?", ["plástico", "vidrio", "papel", "cartón"]),
    ]

    pregunta, respuestas_correctas = random.choice(preguntas_eco)

    await ctx.send(f"Pregunta ecológica: {pregunta}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    mensaje = await bot.wait_for("message", check=check)

    if mensaje.content.strip().lower() in [r.lower() for r in respuestas_correctas]:
        await ctx.send("¡Correcto! 🌿")
    else:
        await ctx.send(f"No es correcto. La respuesta correcta era: {', '.join(respuestas_correctas)}.")


bot.run("")
