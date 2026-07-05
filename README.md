# 📡 Telecom RAG Chatbot

An AI-powered Telecom Customer Support Chatbot built with **Python**, **Streamlit**, and **Retrieval-Augmented Generation (RAG)**. The application provides an interactive web interface where users can ask telecom-related questions and receive accurate, context-aware answers retrieved from telecom documentation, FAQs, and historical customer support tickets.

---

## 🚀 Features

- 🤖 AI-powered customer support chatbot
- 💬 Interactive web interface built with Streamlit
- 📄 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search using ChromaDB
- 📚 Knowledge retrieval from telecom documentation (PDF)
- ❓ FAQ-based question answering
- 🎫 Customer ticket history retrieval
- ⚡ Fast and context-aware responses

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- ChromaDB
- SQLite
- Pandas

---

## 📁 Project Structure

```text
Telecom-RAG-Chatbot/
│
├── app.py                    # Streamlit application
├── rag_chain.py              # RAG pipeline
├── retriever.py              # Retrieval logic
├── ingest_pdf.py             # PDF ingestion
├── ingest_faq.py             # FAQ ingestion
├── ingest_tickets.py         # Ticket ingestion
│
├── data/
│   ├── telecom_guide.pdf
│   ├── faq.csv
│   └── tickets.db
│
├── chroma_store/             # Vector database (generated)
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/stuti191/Telecom-RAG-Chatbot.git
```

### 2. Navigate to the project directory

```bash
cd Telecom-RAG-Chatbot
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Build the vector database

Run the ingestion scripts to populate the knowledge base:

```bash
python ingest_pdf.py
python ingest_faq.py
python ingest_tickets.py
```

### 5. Launch the application

```bash
streamlit run app.py
```

---

## 📂 Knowledge Sources

The chatbot retrieves information from multiple sources:

- 📄 Telecom documentation (PDF)
- ❓ Frequently Asked Questions (CSV)
- 🎫 Historical customer support tickets (SQLite)

---

## 🌱 Future Improvements

- Multi-turn conversation memory
- Voice-based interaction
- Multi-language support
- Authentication and user profiles
- Live LLM integration
- Cloud deployment

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome. Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 👩‍💻 Author

**Stuti Mishra**