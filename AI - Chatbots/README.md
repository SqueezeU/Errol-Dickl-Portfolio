## 🤖 Chatbots

This folder contains examples of chatbots, conversational flows, and tests using large language models (LLMs).

---

### 💬 Chatbots – Conversational AI Applications

This section presents two chatbot examples developed during my practical exercises.  
One uses a cloud connection (GPT-4 + Gradio), the other applies local information retrieval (RAG) with llama-index.

---

### 🤖 Chatbot Cloud with GPT-4 (Gradio)

This bot simulates a customer service assistant using **Gradio** as the web interface and **GPT-4** as the response engine.

🔍 **Components:**

- Defined prompts  
- Gradio user interface  
- Direct implementation in Python

📘 **Notebook:** [`Bot_Cloud_Gradio_+_GPT4.ipynb`](https://github.com/SqueezeU/Portfolio-AI-DS/blob/main/Chatbots/Bot%20Cloud%20Gradio%20%2B%20GPT4.ipynb)

---

### 🧠 Chatbot with Local Retrieval (RAG)

A second version implements a **Retrieval-Augmented Generation (RAG)** approach.  
It uses local documents combined with GPT-4 response generation.

🛠️ **Tools used:**

- `llama-index` for indexing local documents (`.txt`, `.csv`, `.pdf`)  
- `OpenAI` as response engine  
- `Gradio` as conversational interface

📘 **Notebook:** [`RAG_llama_index_Errol_BEREINIGT.ipynb`](https://github.com/SqueezeU/Portfolio-AI-DS/blob/main/Chatbots/RAG_llama_index_Errol_BEREINIGT.ipynb)  
📄 📄 **Additional explanation:** [`Bot_Cliente_Codigo_y_Explicacion_ES.docx`](https://github.com/SqueezeU/Portfolio-AI-DS/blob/main/Chatbots/Bot_Cliente_Codigo_y_Explicacion_ES.docx)

---

### 🔐 How to Use the OpenAI API Locally

The file [`API_Key_OpenAI.md`](https://github.com/SqueezeU/Portfolio-AI-DS/blob/main/Chatbots/API_Key_OpenAI.md) explains how to add your OpenAI API key as a local environment variable without writing it in the code.

⚠️ API keys should never be uploaded to GitHub.


...


