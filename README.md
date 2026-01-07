# 🤖 RAG Chat-Bot

A conversational AI chatbot with Retrieval-Augmented Generation (RAG) capabilities, built with LangChain, Google Gemini, and Streamlit.

## 📋 Overview

This application allows users to upload documents and have intelligent conversations about their content. The chatbot uses RAG to retrieve relevant information from uploaded documents and provides accurate, context-aware responses.

## 🚀 Features

- **Document Upload**: Support for PDF and TXT file uploads
- **RAG-Powered Responses**: Retrieves relevant context from uploaded documents
- **Conversation Memory**: Maintains chat history for contextual conversations
- **ReAct Agent**: Uses a reasoning and acting pattern for intelligent responses
- **Modern UI**: Clean Streamlit interface with custom chat bubbles

## 🏗️ Architecture

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Document       │
│  Processing     │
│  (RAG.py)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Store   │
│  (ChromaDB)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ReAct Agent    │
│  (LLM.py)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Response      │
└─────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- A Google API key for Gemini

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project_2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your API keys
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
project_2/
├── app.py          # Main Streamlit application
├── LLM.py          # LLM configuration and ReAct agent
├── RAG.py          # Document processing and vector store
├── .env            # Environment variables (not committed)
├── .env.example    # Example environment variables
├── .gitignore      # Git ignore rules
├── db/             # Vector store database (auto-created)
└── README.md       # This file
```

## 🔧 Configuration

| Variable                   | Description                  | Default  |
|----------------------------|------------------------------|----------|
| `GOOGLE_API_KEY`           | Google Gemini API key        | Required |
| `HF_TOKEN`                 | HuggingFace token (optional) | Optional |
| `HUGGINGFACEHUB_API_TOKEN` | HuggingFace Hub token        | Optional |

## 🛡️ Security Features

This application implements several security measures:

### File Upload Security
- **File Type Validation**: Only PDF and TXT files are allowed
- **File Size Limits**: Maximum 10MB per file
- **File Count Limits**: Maximum 10 files per upload
- **Filename Sanitization**: Prevents path traversal attacks
- **Temporary File Cleanup**: Uploaded files are securely deleted after processing

### XSS Protection
- All user-generated content is HTML-escaped before rendering
- Chat messages are sanitized to prevent script injection

### Data Protection
- Sensitive API keys stored in environment variables
- `.gitignore` prevents accidental commit of sensitive files
- Uploaded documents are processed in temporary storage

## 📖 Usage

### Uploading Documents

1. Click on "Upload your documents here" in the sidebar
2. Select PDF or TXT files (max 10MB each)
3. Click "Process Documents" to index them

### Chatting

1. Type your question in the chat input
2. The bot will search the uploaded documents for relevant context
3. If no documents are uploaded, the bot uses its general knowledge

### Example Questions

- "What is the main topic of the document?"
- "Summarize the key points"
- "What does the document say about [specific topic]?"
- "Can you explain [concept] from the document?"

## 🧪 Technical Details

### Document Processing

- **Chunking**: Documents are split into 1000-character chunks with 100-character overlap
- **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings
- **Vector Store**: ChromaDB for efficient similarity search
- **Retrieval**: MMR (Maximal Marginal Relevance) for diverse results

### LLM Configuration

- **Model**: Google Gemini 2.5 Pro
- **Agent Type**: ReAct (Reasoning + Acting)
- **Memory**: Conversation buffer for context
- **Max Iterations**: 6 reasoning steps

## 📚 Dependencies

- `streamlit` - Web UI framework
- `langchain` - LLM framework
- `langchain-google-genai` - Google Gemini integration
- `langchain-chroma` - ChromaDB vector store
- `langchain-huggingface` - HuggingFace embeddings
- `langchain-community` - Document loaders
- `pymupdf` - PDF processing
- `python-dotenv` - Environment variable management

## ⚠️ Important Notes

1. **Never commit your `.env` file** - It contains sensitive API keys
2. **Document Processing** - Large documents may take time to process
3. **Rate Limits** - Be aware of Google API rate limits
4. **Storage** - Vector store persists locally in the `db/` folder

## 🔒 Supported File Types

| Type | Extension | MIME Type |
|------|-----------|-----------|
| PDF | `.pdf` | `application/pdf` |
| Text | `.txt` | `text/plain` |

## 🐛 Troubleshooting

### "No documents have been processed yet"
- Upload and process documents using the sidebar

### "File type not allowed"
- Only PDF and TXT files are supported

### API Rate Limit Errors
- Wait a few minutes and try again
- Consider using a paid API tier

### Memory Issues
- Process fewer documents at once
- Reduce chunk size in RAG.py

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - LLM framework
- [Streamlit](https://streamlit.io/) - Web UI framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [HuggingFace](https://huggingface.co/) - Embeddings model
