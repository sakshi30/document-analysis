# RAG-Based Question & Answer System

A Retrieval-Augmented Generation (RAG) system that combines document retrieval with generative AI to provide accurate, context-aware answers to user questions.

## Description

This project implements a RAG-based Q&A system that enhances large language model responses by retrieving relevant information from a knowledge base before generating answers. The system splits documents into chunks, creates embeddings, stores them in a vector database, and retrieves the most relevant context to answer user queries.

## Features

- **Document Processing**: Supports multiple document formats (PDF, TXT, DOCX, etc.)
- **Intelligent Chunking**: Splits documents into semantically meaningful chunks
- **Vector Embeddings**: Creates high-quality embeddings for efficient similarity search
- **Semantic Search**: Retrieves most relevant context using cosine similarity
- **Context-Aware Responses**: Generates answers based on retrieved context
- **Source Attribution**: Provides references to source documents
- **Scalable Architecture**: Handles large document collections efficiently

## Architecture

```
User Query → Query Embedding → Vector Search → Context Retrieval → LLM Generation → Response
```

## Technologies Used

- **Python 3.8+**
- **Ollama API**: For embeddings and text generation
- **Chroma**: Vector database for storing embeddings
- **astAPI**: Web interface (optional)
- **PyPDF2/python-docx**: Document processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sakshi30/document-analysis.git
cd document-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your API keys and configuration
```

## Configuration

Create a `.env` file with the following variables:

```env
VECTOR_DB_PATH=./vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RESULTS=5
```

## Usage



### Command Line Interface

```bash
# Process documents
python main.py --add-docs "path/to/documents/"

# Start interactive Q&A
python main.py --interactive

# Query directly
python main.py --query "Your question here"
```

### Web Interface

```bash
# Start Streamlit app
streamlit run app.py

# Or start FastAPI server
uvicorn api:app --reload
```

## Project Structure

```
document-analysis/
├── requirements.txt
├── .env.example
├── main.py
├── TextProcessor.py
├── RagSystem.py
└── README.md
```

## Key Components

### Document Processor
- Handles multiple file formats
- Extracts text and metadata
- Implements intelligent chunking strategies

### Embedding System
- Creates vector representations of text chunks
- Supports various embedding models
- Optimizes for semantic similarity

### Vector Store
- Stores and indexes document embeddings
- Enables fast similarity search
- Supports metadata filtering

### Retrieval System
- Finds most relevant document chunks
- Implements advanced retrieval strategies
- Handles query expansion and reranking

### Generation System
- Combines retrieved context with user queries
- Generates coherent, factual responses
- Provides source attribution

## Performance Optimization

- **Batch Processing**: Process multiple documents simultaneously
- **Caching**: Cache embeddings and frequent queries
- **Indexing**: Use efficient vector indexing algorithms
- **Chunking Strategy**: Optimize chunk size for your use case

## Evaluation Metrics

- **Retrieval Accuracy**: Measures relevance of retrieved documents
- **Answer Quality**: Evaluates response accuracy and completeness
- **Response Time**: Tracks system performance
- **Source Attribution**: Verifies correct source linking

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Cloud Deployment

The system can be deployed on:
- AWS (using ECS, Lambda, or EC2)
- Google Cloud Platform
- Azure
- Heroku

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Implement retry logic and rate limiting
2. **Memory Issues**: Optimize chunk size and batch processing
3. **Slow Queries**: Check vector database indexing
4. **Poor Results**: Tune chunking strategy and retrieval parameters

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Ollama (Llama3.1) for the GPT models and embeddings
- The open-source community for various tools and libraries

## Roadmap

- [ ] Support for more document formats
- [ ] Advanced query understanding
- [ ] Multi-language support
- [ ] Real-time document updates
- [ ] Analytics dashboard
- [ ] API rate limiting and authentication

## Contact

Your Name - sakshidinesh@gmail.com

Project Link: [https://github.com/sakshi30/document-analysis]
