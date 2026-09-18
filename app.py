import tempfile

import streamlit as st

from src.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="Technical Documentation Assistant",
    page_icon="📚"
)

st.title("📚 Technical Documentation Assistant")

st.write(
    "Upload a PDF document and ask questions about its content."
)

st.divider()


# Upload PDF
uploaded_file = st.file_uploader(
    "📤 Upload your PDF",
    type=["pdf"]
)


if uploaded_file is None:

    st.info("Please upload a PDF document to get started.")

else:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    # Process a new PDF
    if (
        "rag_pipeline" not in st.session_state
        or st.session_state.get("file_name") != uploaded_file.name
    ):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(
                uploaded_file.getvalue()
            )

            pdf_path = temp_file.name

        with st.spinner(
            "Processing PDF... Please wait."
        ):

            try:

                rag = RAGPipeline(pdf_path)

                st.session_state.rag_pipeline = rag
                st.session_state.file_name = uploaded_file.name

            except Exception as e:

                st.error(
                    f"Error processing PDF: {e}"
                )

                st.stop()


    rag = st.session_state.rag_pipeline

    st.success("✅ PDF processed successfully!")


    # Document information
    st.subheader("📄 Document Information")

    col1, col2 = st.columns(2)

    col1.metric(
        "Pages",
        len(rag.pages)
    )

    col2.metric(
        "Text Chunks",
        len(rag.documents)
    )


    st.divider()


    # Question
    st.subheader("💬 Ask a Question")

    question = st.text_input(
        "Enter your question:",
        placeholder="Example: What is Artificial Intelligence?"
    )


    if st.button("🔍 Ask", type="primary"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching document and generating answer..."
            ):

                try:

                    answer, results = rag.ask(question)

                    st.subheader("🤖 Answer")

                    st.write(answer)

                    st.subheader("📚 Retrieved Sources")

                    for i, result in enumerate(
                        results,
                        start=1
                    ):

                        with st.expander(
                            f"Source {i} — Page {result['page']}"
                        ):

                            st.write(
                                f"**Document:** {result['source']}"
                            )

                            st.write(
                                f"**Page:** {result['page']}"
                            )

                            st.write(
                                f"**Similarity Score:** "
                                f"{result['score']:.4f}"
                            )

                            st.write(
                                result["text"]
                            )

                except Exception as e:

                    st.error(
                        f"Error generating answer: {e}"
                    )