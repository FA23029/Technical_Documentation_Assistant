from src.pdf_loader import load_pdf
from src.chunker import create_chunks
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.generator import GeminiGenerator


class RAGPipeline:

    def __init__(self, pdf_path):

        print("Loading document...")

        pages = load_pdf(pdf_path)

        if not pages:
            raise ValueError("No readable text was found in the PDF.")

        self.pages = pages

        print(f"Pages loaded: {len(pages)}")

        self.documents = create_chunks(pages)

        if not self.documents:
            raise ValueError("No text chunks were created from the PDF.")

        print(f"Chunks created: {len(self.documents)}")

        print("Creating embeddings...")

        self.embedding_model = EmbeddingModel()

        texts = [
            document["text"]
            for document in self.documents
        ]

        embeddings = self.embedding_model.encode(texts)

        print(f"Embeddings created: {embeddings.shape}")

        print("Building FAISS vector store...")

        self.vector_store = VectorStore(
            embeddings.shape[1]
        )

        self.vector_store.add(
            embeddings,
            self.documents
        )

        print(f"Vectors stored: {len(self.documents)}")

        self.generator = GeminiGenerator()

        print("RAG pipeline ready!")

    def ask(self, question, top_k=5):

        query_embedding = self.embedding_model.encode(
            [question]
        )[0]

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        answer = self.generator.generate(
            question,
            results
        )

        return answer, results