import altair as alt  # Agrega esta importación arriba con las demás

# Función para crear visualizaciones usando Altair
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    
    # Visualización de sentimiento y subjetividad
    with col1:
        st.subheader("Análisis de Sentimiento y Subjetividad")
        
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        
        st.write("**Sentimiento:**")
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")
        
        st.write("**Subjetividad:**")
        st.progress(resultados["subjetividad"])
        
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")
    
    # Palabras más frecuentes usando Altair
    with col2:
        st.subheader("Palabras más frecuentes")
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            df_palabras = pd.DataFrame(list(palabras_top.items()), columns=["Palabra", "Frecuencia"])
            
            chart = alt.Chart(df_palabras).mark_bar(
                color='#FF69B4'  # Rosado
            ).encode(
                x=alt.X('Palabra:N', sort='-y'),
                y='Frecuencia:Q',
                tooltip=['Palabra', 'Frecuencia']
            ).properties(
                width=400,
                height=300
            ).configure_axis(
                labelColor='pink',
                titleColor='pink'
            ).configure_view(
                strokeWidth=0
            )
            st.altair_chart(chart, use_container_width=True)
    
    # Mostrar texto traducido
    st.subheader("Texto Traducido")
    with st.expander("Ver traducción completa"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Texto Original (Español):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**Texto Traducido (Inglés):**")
            st.text(resultados["texto_traducido"])
    
    # Análisis de frases
    st.subheader("Frases detectadas")
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]
            
            try:
                blob_frase = TextBlob(frase_traducida)
                sentimiento = blob_frase.sentiment.polarity
                
                if sentimiento > 0.05:
                    emoji = "😊"
                elif sentimiento < -0.05:
                    emoji = "😟"
                else:
                    emoji = "😐"
                
                st.write(f"{i}. {emoji} **Original:** *\"{frase_original}\"*")
                st.write(f"   **Traducción:** *\"{frase_traducida}\"* (Sentimiento: {sentimiento:.2f})")
                st.write("---")
            except:
                st.write(f"{i}. **Original:** *\"{frase_original}\"*")
                st.write(f"   **Traducción:** *\"{frase_traducida}\"*")
                st.write("---")
    else:
        st.write("No se detectaron frases.")
