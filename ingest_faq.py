"""
Ingests data/faq.csv into the 'faq' Chroma collection.
Run once (or whenever the CSV changes): python ingest_faq.py
"""
import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
# Suppresses warnings and unnecessary logs from the transformers library and shows only errors.This makes terminal cleaner.
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "chroma_store"
# Where Chroma saves its database.
COLLECTION  = "faq"
# Collection is like table in SQL.
CSV_PATH    = os.path.join("data", "faq.csv")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_faq_documents(csv_path: str) -> list[Document]:
    df = pd.read_csv(csv_path)
    docs = []
    for _, row in df.iterrows():
# if faq.csv has 3 rows then this loopwill run 3 times.iterrows() returns (index,row).
        content = f"Q: {row['question']}\nA: {row['answer']}"
        docs.append(Document(
            page_content=content,
            metadata={"source": "faq", "category": row["category"], "faq_id": str(row["id"])},
        ))
    return docs
# A Document is a class provided by LangChain.It has 2 parts page_content and metadeta.page_content is the actual text that will be embedded.Metadata is extra information about the document.It is NOT the text that gets embedded.
# The function reads the CSV.
# It creates one Document object for each row.
# It stores all those Document objects in the docs list.
# return docs hands that list back to the caller.

def main():
    print("Loading FAQ documents...")
    docs = load_faq_documents(CSV_PATH)
    print(f"  {len(docs)} FAQ entries loaded.")

    print("Initialising embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    print(f"Embedding and storing in Chroma collection '{COLLECTION}'...")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
    )
    print(f"  Done. {vectorstore._collection.count()} vectors stored.")


if __name__ == "__main__":
    main()
