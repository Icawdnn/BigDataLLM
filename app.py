import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO
import openai

# Setel kunci API OpenAI Anda di sini
openai.api_key = "AIzaSyDAU2ALRZsgMcKFlnxnWt9SR-Z8GVNxaV8"

# Fungsi ekstraksi informasi dari file PDF menggunakan PyMuPDF
def extract_information_from_pdf(pdf_content):
    pdf_file = BytesIO(pdf_content.read())

    information = {"title": "", "author": "", "text": ""}

    # Mendapatkan metadata file PDF
    with fitz.open(filetype="pdf", stream=pdf_file.getvalue()) as doc:
        info_dict = doc.metadata
        information["title"] = info_dict.get("title", "")
        information["author"] = info_dict.get("author", "")

        # Mendapatkan teks dari setiap halaman
        text = ""
        for page_number in range(doc.page_count):
            page = doc[page_number]
            text += page.get_text()

        information["text"] = text

    return information

# Fungsi untuk memanggil API OpenAI untuk mendapatkan hasil ekstraksi dari prompt
# def get_openai_extraction_result(prompt):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=200
#     )
#     return response.choices[0].text.strip()

# Fungsi utama aplikasi Streamlit
def main():
    # HTML untuk memberikan style pada halaman
    st.markdown("""
        <style>
            body {
                background-color: #f8f8f8; /* Ganti dengan warna abu-abu yang lebih terang */
                margin: 0;
                padding: 0;
                font-family: 'Times New Roman', sans-serif;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1, h2, h3 {
                color: #333;
            }
            subheader {
                font-size: 18px;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            p {
                color: #555;
            }
        </style>

    """, unsafe_allow_html=True)

    # Judul aplikasi
    st.title("PDF Information Extraction")

    # Upload file PDF
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        # Ekstraksi informasi dari file PDF
        pdf_information = extract_information_from_pdf(pdf_file)

        # Tampilkan informasi
        st.subheader("Document Information:")
        st.write(f"Title: {pdf_information['title']}")
        st.write(f"Author: {pdf_information['author']}")

        # Tampilkan teks asli
        st.subheader("Text Content:")
        st.text(pdf_information['text'])

        # # Tombol untuk ekstraksi file
        # if st.button("Extract Information"):
        #     # Mendapatkan prompt dari API OpenAI
        #     prompt = "Ekstrak informasi dari file PDF:"

        #     # Memanggil API OpenAI untuk ekstraksi
        #     hasil_ekstraksi = get_openai_extraction_result(prompt)

        #     st.write(hasil_ekstraksi)

if __name__ == "__main__":
    main()
