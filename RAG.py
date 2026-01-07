import os, tempfile
import logging
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

# Security constants
ALLOWED_EXTENSIONS = {'.pdf', '.txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size
MAX_FILES = 10  # Maximum number of files to process

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
current_directory = os.path.dirname(os.path.abspath(__file__))
persist_directory = os.path.join(current_directory, "db", "uploaded_docs_from_user")


def validate_file(file) -> tuple[bool, str]:
    """Validate uploaded file for security"""
    # Check file extension
    suffix = os.path.splitext(file.name)[1].lower()
    if suffix not in ALLOWED_EXTENSIONS:
        return False, f"File type {suffix} not allowed. Allowed types: {ALLOWED_EXTENSIONS}"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
    
    if file_size == 0:
        return False, "File is empty"
    
    # Sanitize filename to prevent path traversal
    safe_name = os.path.basename(file.name)
    if safe_name != file.name or '..' in file.name:
        return False, "Invalid filename"
    
    return True, ""


def process_documents(file_list):
    """Process uploaded documents with security validation"""
    if len(file_list) > MAX_FILES:
        raise ValueError(f"Too many files. Maximum allowed: {MAX_FILES}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100
    )

    documents = []
    logger.info("Processing uploaded files")
    
    for file in file_list:
        # Validate file before processing
        is_valid, error_msg = validate_file(file)
        if not is_valid:
            logger.warning(f"Skipping invalid file {file.name}: {error_msg}")
            continue
        
        suffix = os.path.splitext(file.name)[1].lower()
        
        # Create temp file securely
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            temp_path = tmp.name

        try:
            if file.type == "application/pdf":
                loader = PyMuPDFLoader(temp_path)
            elif file.type == "text/plain":
                loader = TextLoader(temp_path, encoding="utf-8")
            else:
                logger.warning(f"Unsupported file type: {file.type}")
                continue

            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            logger.error(f"Error processing file {file.name}: {e}")
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except Exception:
                pass

    if not documents:
        raise ValueError("No valid documents were processed")

    split_docs = text_splitter.split_documents(documents)

    db = Chroma.from_documents(
        split_docs,
        embedding_model,
        persist_directory=persist_directory,
    )

    return db, split_docs