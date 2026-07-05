"""
Builds a merged retriever across all three Chroma collections:
  - faq     : FAQ entries (no chunking — 1 row = 1 doc)
  - tickets : resolved support tickets (no chunking — 1 ticket = 1 doc)
  - guides  : PDF guide chunks (RecursiveCharacterTextSplitter applied at ingest)
"""
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document

CHROMA_DIR  = "chroma_store"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# now we must convert query text into embeddings to compare with the stored embeddings. We use the same model for this as we did for the documents, to ensure that the embeddings are in the same vector space and can be meaningfully compared.


def build_retriever(
    k_faq: int = 3,
    k_tickets: int = 3,
    k_guides: int = 3,
    # this retrieves top 3 faqs, top 3 tickets, and top 3 guide chunks by default. These values can be adjusted based on how many results you want to return from each collection.
) -> RunnableLambda:
    # used RunnableLambda because my retrieval logic was written as a normal Python function. LangChain pipelines expect components to be Runnables so they all work in the same way using .invoke()
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    faq_store = Chroma(
        collection_name="faq",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    tickets_store = Chroma(
        collection_name="tickets",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    guides_store = Chroma(
        collection_name="guides",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    faq_retriever     = faq_store.as_retriever(search_kwargs={"k": k_faq})
    tickets_retriever = tickets_store.as_retriever(search_kwargs={"k": k_tickets})
    guides_retriever  = guides_store.as_retriever(search_kwargs={"k": k_guides})
    # I open the three existing Chroma collections—FAQ, tickets, and guides—from the local chroma_store directory. At this point, they are just vector databases. Next, I convert each database into a retriever using as_retriever(). A retriever is simply a search interface over the vector database. I configure each retriever to return the top k most similar documents, where k is 3 by default.

    def retrieve(query: str) -> list[Document]:
        return (
            faq_retriever.invoke(query)
            + tickets_retriever.invoke(query)
            + guides_retriever.invoke(query)
        )
    # The retrieve() function takes a query string, invokes each of the three retrievers with that query, and concatenates the results into a single list of Document objects. This allows me to search across all three collections at once and return a unified set of results.

    return RunnableLambda(retrieve)
