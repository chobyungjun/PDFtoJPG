import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

# PDF 파일 업로드
st.title("PDF to JPG Converter")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # PDF 파일 열기
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    # 각 페이지를 순회하며 JPG로 변환
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # 페이지 로드
        pix = page.get_pixmap()  # 페이지를 이미지로 변환

        # 이미지 객체를 Pillow로 변환
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 이미지 표시
        st.image(img, caption=f"Page {page_num + 1}", use_column_width=True)

        # 이미지 저장을 위한 버튼
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.download_button(
            label=f"Download Page {page_num + 1} as JPG",
            data=byte_im,
            file_name=f"page_{page_num + 1}.jpg",
            mime="image/jpeg"
        )
