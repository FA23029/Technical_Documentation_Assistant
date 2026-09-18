import os
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()


class GeminiGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"

    def generate(self, question, retrieved_documents):

        context = ""

        for i, document in enumerate(retrieved_documents, start=1):
            context += f"""
SOURCE {i}
Document: {document['source']}
Page: {document['page']}

Content:
{document['text']}

--------------------
"""

        prompt = f"""
You are a Technical Documentation Assistant.

Answer the user's question ONLY using the
provided documentation.

Do not use outside knowledge.
Do not guess.
Do not invent information.

If the answer cannot be found in the provided
documentation, say:

"I could not find this information in the
provided documentation."

USER QUESTION:
{question}

DOCUMENTATION:
{context}

Give a clear and concise answer.

At the end, provide the documentation references.
"""

        for attempt in range(3):

            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                if attempt < 2:
                    wait_time = 5 * (2 ** attempt)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    return (
                        "Gemini is temporarily unavailable. "
                        "Please click Ask again in a few seconds."
                    )