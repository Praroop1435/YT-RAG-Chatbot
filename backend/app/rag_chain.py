from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough
)
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv

load_dotenv()


def build_rag_chain(retriever):
    llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-V3.2",
        task="text-generation",
        temperature=0.2
    ) # type: ignore
    model = ChatHuggingFace(llm = llm)

    prompt = PromptTemplate(
        template="""
        You are a careful and helpful assistant.

        You are given transcript excerpts from a YouTube lecture.
        The transcript may be conversational, fragmented, or example-driven.

        Your task:
        - Answer the question using ONLY the information present in the transcript.
        - You MAY synthesize, summarize, or group ideas that appear across multiple excerpts.
        - You MUST NOT introduce topics, problems, or concepts that are not evidenced in the transcript.
        - If the transcript provides partial or implicit information, give a best-effort summary based on what is clearly discussed.
        - If the transcript truly contains no relevant information, say "I don't know".

        Transcript Context:
        {context}

        Question:
        {question}

        Answer (be concise, factual, and grounded in the transcript):
        """,
        input_variables=["context", "question"]
    )


    def format_docs(docs: List[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)
        

    parallel = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    

    return parallel | prompt | model | StrOutputParser()
