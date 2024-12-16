import streamlit as st
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
import io
import re  # Para substituições com expressões regulares


# Função para extrair texto do PDF, mantendo quebras de linha
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# Função para realizar a substituição de palavras ignorando maiúsculas e minúsculas
def replace_text(input_text, word_to_replace, replacement_word):
    pattern = re.compile(re.escape(word_to_replace), re.IGNORECASE)
    return pattern.sub(replacement_word, input_text)


# Função para criar um novo PDF com o texto editado, mantendo a formatação simples
def create_pdf_with_text(edited_text):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    # Configuração de texto no PDF
    c.setFont("Helvetica", 12)

    # Dividindo o texto em linhas e criando um PDF com formatação simples
    lines = edited_text.split("\n")

    # Posiciona o texto linha por linha
    y = 800  # Posição inicial vertical
    for line in lines:
        c.drawString(50, y, line)
        y -= 15  # Ajusta o espaçamento entre linhas
        if y < 50:  # Cria nova página se necessário
            c.showPage()
            y = 800

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer


# Interface Streamlit
st.title("Editor de PDFs: Substituir Palavras")
st.write("Carregue um arquivo PDF e forneça as palavras para substituição.")

# Upload do PDF
uploaded_pdf = st.file_uploader("Carregar PDF", type="pdf")

if uploaded_pdf:
    # Extrair texto
    st.info("Extraindo texto do PDF...")
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.text_area("Texto extraído:", pdf_text, height=200)

    # Instruções de substituição
    word_to_replace = st.text_input("Palavra para substituir:", placeholder="Exemplo: café")
    replacement_word = st.text_input("Palavra de substituição:", placeholder="Exemplo: chá")

    # Botão de substituição
    if st.button("Substituir e Gerar PDF"):
        st.info(f"Substituindo '{word_to_replace}' por '{replacement_word}' (ignorando maiúsculas/minúsculas)...")

        # Substitui o texto
        edited_text = replace_text(pdf_text, word_to_replace, replacement_word)
        st.text_area("Texto editado:", edited_text, height=200)

        # Criar novo PDF com o texto editado
        st.info("Gerando o PDF editado...")
        output_pdf = create_pdf_with_text(edited_text)

        # Botão para baixar o PDF editado
        st.download_button(
            label="Baixar PDF Editado",
            data=output_pdf,
            file_name="pdf_editado.pdf",
            mime="application/pdf"
        )
