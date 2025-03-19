# Chat with Multiple PDFs

An interactive web application that allows users to chat with and ask questions about the content of multiple PDF documents using AI technology.

![App Screenshot](https://via.placeholder.com/800x400?text=PDF+Chat+Application)

## 🌟 Features

- Upload and process multiple PDF files simultaneously
- Extract and analyze text content using natural language processing
- Chat interface to ask questions about the documents
- Retrieve relevant information with citation sources
- Clean, modern UI with an intuitive user experience
- Real-time response generation with typing indicators
- View source documents from which answers are derived

## 🔧 Technologies Used

- **Streamlit**: Frontend web interface
- **LangChain**: Framework for combining LLMs with external data
- **OpenAI**: GPT-3.5 Turbo for natural language understanding and generation
- **FAISS**: Vector database for efficient similarity search
- **PyPDF2**: PDF text extraction
- **Python**: Core programming language

## 🚀 Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd multi-chat
   ```

2. Create a virtual environment:

   ```bash
   python -m venv myenv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key
     HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
     ```

## 📋 Usage

1. Start the application:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the application:
   - Upload PDF files using the sidebar
   - Click "Process Documents" to analyze the content
   - Type your questions in the chat input
   - View the AI's responses and source references

## 💬 How It Works

1. **Document Processing**:

   - PDF files are uploaded and text is extracted
   - Text is split into manageable chunks
   - Chunks are embedded using OpenAI's embedding model
   - Embeddings are stored in a FAISS vector database

2. **Question Answering**:
   - User asks a question through the chat interface
   - LangChain retrieves relevant document chunks
   - The AI model generates a comprehensive answer
   - Sources are cited for transparency

## 📖 Example Questions

After uploading your documents, try asking questions like:

- "What are the main points in these documents?"
- "Can you summarize the key findings?"
- "What information is available about [specific topic]?"
- "Compare the different approaches mentioned in the documents."

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- OpenAI for providing the language model API
- LangChain for the framework to build LLM applications
- Streamlit for making web app development simple with Python
