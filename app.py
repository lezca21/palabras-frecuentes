import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="✨ Analizador de Texto Mágico ✨",
    page_icon="📝",
    layout="wide"
)

# Título principal
st.title("🌸 Analizador de Texto con TextBlob 🌸")
st.markdown("""
¡Bienvenido! 🎉 Esta app te ayudará a explorar tus textos de una manera sencilla y amigable:
- 📈 Análisis de sentimiento y subjetividad
- 🔎 Extracción de palabras clave
- 📊 Análisis de frecuencia de palabras
""")

# Barra lateral de opciones
st.sidebar.title("⚙️ Opciones mágicas")
modo = st.sidebar.selectbox(
    "Elige cómo quieres ingresar tu texto ✨:",
    ["✍️ Escribir directamente", "📂 Subir un archivo"]
)

# Función para contar palabras
def contar_palabras(texto):
    stop_words = set([...])  # (Tu lista larga de stopwords va aquí sin cambios)

    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    return contador_ordenado, palabras_filtradas

# Traductor
translator = Translator()

def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"🚨 Error al traducir: {e}")
        return texto

# Procesamiento del texto
def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)

    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity

    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]

    frases_combinadas = [
        {"original": frases_originales[i], "traducido": frases_traducidas[i]}
        for i in range(min(len(frases_originales), len(frases_traducidas)))
    ]

    contador_palabras, palabras = contar_palabras(texto_ingles)

    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# Visualizaciones
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Resultados de Sentimiento y Subjetividad")

        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.write("**🌟 Sentimiento:**")
        st.progress(sentimiento_norm)

        if resultados["sentimiento"] > 0.05:
            st.success(f"😊 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"😟 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"😐 Neutral ({resultados['sentimiento']:.2f})")

        st.write("**💭 Subjetividad:**")
        st.progress(resultados["subjetividad"])

        if resultados["subjetividad"] > 0.5:
            st.warning(f"✨ Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")

    with col2:
        st.subheader("🔠 Palabras más frecuentes")
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            st.bar_chart(palabras_top)

    st.subheader("🌐 Texto Traducido")
    with st.expander("🔍 Ver traducción completa"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Texto Original (Español):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**Texto en Inglés:**")
            st.text(resultados["texto_traducido"])

    st.subheader("📝 Frases Analizadas")
    if resultados["frases"]:
        for i, frase in enumerate(resultados["frases"][:10], 1):
            try:
                blob_frase = TextBlob(frase["traducido"])
                sentimiento = blob_frase.sentiment.polarity

                if sentimiento > 0.05:
                    emoji = "😊"
                elif sentimiento < -0.05:
                    emoji = "😟"
                else:
                    emoji = "😐"

                st.write(f"{i}. {emoji} **Original:** *{frase['original']}*")
                st.write(f"   **Traducción:** *{frase['traducido']}* (Sentimiento: {sentimiento:.2f})")
                st.write("---")
            except:
                st.write(f"{i}. **Original:** *{frase['original']}*")
                st.write(f"   **Traducción:** *{frase['traducido']}*")
                st.write("---")
    else:
        st.write("❌ No se detectaron frases importantes.")

# Lógica principal
if modo == "✍️ Escribir directamente":
    st.subheader("🖋️ Escribe tu texto aquí")
    texto = st.text_area("Tu historia, tu idea, tu inspiración...", height=200)

    if st.button("✨ Analizar texto"):
        if texto.strip():
            with st.spinner("🔮 Analizando..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("⚡ ¡Por favor escribe algo bonito primero!")

elif modo == "📂 Subir un archivo":
    st.subheader("📤 Sube tu archivo de texto")
    archivo = st.file_uploader("", type=["txt", "csv", "md"])

    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander("📖 Ver el contenido del archivo"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))

            if st.button("✨ Analizar archivo"):
                with st.spinner("🔮 Analizando archivo..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"🚨 Error al procesar el archivo: {e}")

# Información extra
with st.expander("📚 Más sobre esta aplicación"):
    st.markdown("""
    Esta app mágica utiliza:
    - **Sentimiento**: De -1 (muy negativo) a +1 (muy positivo) 📈
    - **Subjetividad**: De 0 (muy objetivo) a 1 (muy subjetivo) 💭

    Construido solo con:
    ```
    streamlit
    textblob
    pandas
    googletrans
    ```
    """)

# Footer
st.markdown("---")
st.markdown("Desarrollado con mucho 💖 usando Streamlit y TextBlob")
