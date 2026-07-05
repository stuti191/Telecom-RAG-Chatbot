"""
Builds the RAG chain:
  merged retriever → prompt → Qwen3-32B on Groq → string output
"""
from langchain_core.prompts import ChatPromptTemplate
# ChatPromptTemplate is used to create a structured prompt for the LLM. It allows me to define a system message (instructions for the model) and a human message (the user's question), which are combined into a single prompt that the model can understand.
from langchain_core.output_parsers import StrOutputParser
# StrOutputParser is used to convert the model's output into a simple string. This is because LLMs ususally return objects, not plain strings.
from langchain_core.runnables import RunnablePassthrough
# This passes the input unchanged.No modification.
# Its job is simply to forward the user's question.
from langchain_core.documents import Document
from langchain_groq import ChatGroq

from retriever import build_retriever

SYSTEM_PROMPT = """You are a helpful and professional telecom customer care assistant.
Your job is to help customers resolve technical issues with their mobile service.

Use ONLY the context below to answer the customer's question.
The context comes from two sources:
- FAQ entries (general policy and how-to information)
- Past support tickets (real resolved cases with step-by-step resolutions)

If the context does not contain enough information to answer confidently, say so clearly \
and suggest the customer call 611 or use the MyTelecom app.

Context:
{context}
"""
# context gets replaced with the retrieved documents from the merged retriever. The model is instructed to use only this context to answer the user's question, and to indicate if the context is insufficient for a confident answer.

def _format_docs(docs: list[Document]) -> str:
    sections = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown").upper()
        sections.append(f"[{source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(sections)
# _format_docs() takes a list of Document objects and formats them into a single string. Each document is prefixed with its source (FAQ, ticket, or guide) and separated by "---" to clearly differentiate the different sections of context for the model.

def build_chain():
    retriever = build_retriever()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    llm = ChatGroq(
        model="qwen/qwen3-32b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )
    # I use the Qwen3-32B model on Groq for the LLM. The temperature is set to 0 for deterministic responses, and max_tokens is None to allow the model to generate as much text as needed. The reasoning_format is set to "parsed" to get structured output, and I allow up to 2 retries in case of errors.

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    # The chain is constructed as follows:
    # 1. The merged retriever retrieves relevant documents based on the user's question.
    # 2. The retrieved documents are formatted into a single string using _format_docs().
    # 3. The user's question is passed through unchanged.
    # 4. The prompt is constructed using the system and human messages.
    # 5. The prompt is sent to the LLM for processing.
    # 6. The output from the LLM is parsed into a simple string using StrOutputParser().
# Explanation of the chain:
# When a user asks a question, the first step is retrieval. The retriever searches both the FAQ database and the past resolved support tickets to find the most relevant information.

# These retrieved documents are then formatted into a single context string, where each document is labeled with its source, such as FAQ or Ticket.

# Next, this context and the user's question are inserted into a prompt template. The system prompt instructs the model to answer only using the retrieved context and not to make up information.

# This prompt is then sent to the Qwen3-32B model running on Groq, which generates the answer based on the provided context.

# Finally, the output is passed through StrOutputParser, which extracts the plain text from the model's response, so the application receives a simple string that can be returned to the user
    return chain
