import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

def get_text_from_pdf(pdf_docs):
    raw_text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
    return raw_text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_chunks = text_splitter.split_text(raw_text)
    return text_chunks

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Create proper prompt template for combining docs
    system_template = """
    You are a helpful AI assistant having a conversation with a human about documents they've uploaded.
    The human is asking questions about these documents, and you have access to information to help answer them.

    Use the following pieces of retrieved context to answer the question at the end. 
    If you don't know the answer based on the context, just say "I don't have enough information to answer that." 
    Don't try to make up an answer.

    When answering, provide a thoughtful, comprehensive response and use markdown formatting to make your response readable.

    Retrieved context:
    {context}
    """
    
    human_template = "{question}"
    
    # Create the chat prompt template
    prompt_messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ]
    qa_prompt = ChatPromptTemplate.from_messages(prompt_messages)
    
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True,
        output_key="answer"
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )
    
    return conversation_chain

def handle_user_input(user_question):
    if st.session_state.conversation is not None:
        with st.chat_message("user"):
            st.write(user_question)
        
        # Display a typing indicator while generating the response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.markdown("⟳ _Thinking..._")
            
            try:
                response = st.session_state.conversation({"question": user_question})
                answer = response["answer"]
                
                # Add the current exchange to chat history
                st.session_state.messages.append({"role": "user", "content": user_question})
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # Replace typing indicator with the actual response
                response_placeholder.markdown(answer)
                
                # Optional: Display source documents
                if "source_documents" in response and response["source_documents"]:
                    with st.expander("Source Documents"):
                        for i, doc in enumerate(response["source_documents"]):
                            st.markdown(f"**Document {i+1}**")
                            st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                            st.divider()
            
            except Exception as e:
                response_placeholder.error(f"Error generating response: {str(e)}")
                st.error(f"Full error: {str(e)}")

def main():
    load_dotenv()
    st.set_page_config(
        page_title="Chat with Multiple PDFs",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS for better appearance
    st.markdown("""
    <style>
    .chat-container {
        border-radius: 10px;
        margin-bottom: 10px;
        padding: 15px;
    }
    .user-message {
        background-color: #e6f7ff;
        border-left: 5px solid #1890ff;
    }
    .assistant-message {
        background-color: #f6f6f6;
        border-left: 5px solid #52c41a;
    }
    .stAlert {
        border-radius: 8px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.header("📄 Chat with Multiple PDFs")
    
    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processing_done" not in st.session_state:
        st.session_state.processing_done = False
    
    with st.sidebar:
        st.subheader("📁 Your Documents")
        pdf_docs = st.file_uploader(
            "Upload PDF files", 
            type="pdf", 
            accept_multiple_files=True,
            help="Select one or more PDF files to chat with"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            process_button = st.button("Process Documents", type="primary", use_container_width=True)
        with col2:
            clear_button = st.button("Clear Chat", type="secondary", use_container_width=True)
        
        if clear_button:
            st.session_state.messages = []
            st.session_state.conversation = None
            st.session_state.processing_done = False
            st.rerun()  # Fixed: using st.rerun() instead of st.experimental_rerun()
        
        if process_button:
            if pdf_docs:
                with st.spinner("🔄 Processing your documents..."):
                    # Clear previous conversation
                    st.session_state.messages = []
                    
                    try:
                        # Process the PDFs
                        raw_text = get_text_from_pdf(pdf_docs)
                        
                        # Get text chunks
                        text_chunks = get_text_chunks(raw_text)
                        
                        # Create vector store
                        vector_store = get_vector_store(text_chunks)
                        
                        # Create conversation chain
                        st.session_state.conversation = get_conversation_chain(vector_store)
                        st.session_state.processing_done = True
                        
                        # Add system welcome message
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": "✅ Documents processed successfully! I'm ready to answer questions about your PDFs."
                        })
                        
                        st.success(f"✅ Processed {len(pdf_docs)} document(s) with {len(text_chunks)} chunks!")
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")
            else:
                st.error("Please upload at least one PDF document.")
        
        # Add some helpful info for the user
        with st.expander("ℹ️ About this App"):
            st.write("""
            **Chat with PDF** allows you to have natural conversations with your document content.
            
            **How to use:**
            1. Upload one or more PDF files
            2. Click 'Process Documents' to analyze them
            3. Start asking questions in the chat interface
            
            The app uses AI to understand your questions and retrieve relevant information from your documents.
            """)
    
    # Chat interface
    chat_container = st.container()
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
        # Show instructions or welcome message if no conversation yet
        if not st.session_state.processing_done and not st.session_state.messages:
            st.info("👈 Please upload your PDFs and click 'Process Documents' to get started!")
    
    # Chat input for user questions
    if user_question := st.chat_input(
        placeholder="Ask a question about your PDFs...",
        disabled=not st.session_state.processing_done
    ):
        handle_user_input(user_question)

if __name__ == '__main__':
    main()