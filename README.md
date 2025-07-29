# PDF Intelligence System
## Adobe Hackathon 2025 - Round 1B Solution

A backend document intelligence system that analyzes PDF collections and extracts the most relevant sections based on user persona and specific tasks.

## 🎯 Features

- **Offline Processing**: No internet required, fully containerized
- **CPU Optimized**: Runs efficiently on CPU-only hardware
- **Fast Analysis**: Processes 3-10 documents in under 60 seconds
- **Intelligent Ranking**: Combines semantic similarity with keyword relevance
- **Structured Output**: Clean JSON format with metadata and rankings

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Build the container
docker build -t pdf-intelligence .

# Create input directory and add your PDFs
mkdir -p data/input
# Copy your 3-10 PDF files to data/input/

# Run analysis
docker run -v $(pwd)/data:/app/data pdf-intelligence \
  python main.py \
  --persona "Investment Analyst with expertise in technology sector" \
  --job-to-be-done "Analyze revenue trends and competitive positioning"
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python main.py \
  --input-dir data/input \
  --persona "Your role description" \
  --job-to-be-done "Your specific task"
```

## 📊 Input Requirements

- **PDFs**: 3-10 related documents
- **Persona**: Role and expertise description
- **Task**: Specific job-to-be-done

## 📋 Output Format

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Investment Analyst...",
    "job_to_be_done": "Analyze revenue trends...",
    "processing_timestamp": "2025-01-27T10:30:00"
  },
  "extracted_sections": [
    {
      "document": "annual_report.pdf",
      "page": 12,
      "section_title": "Revenue Performance Analysis",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "annual_report.pdf",
      "page_number": 12,
      "refined_text": "Detailed analysis of revenue trends..."
    }
  ]
}
```

## 🔧 Configuration

Edit `config/default.json` for customization:
- Model parameters
- Processing thresholds
- Output formatting
- Logging settings

## 🧪 Examples

```bash
# Investment analysis
python run_example.py --persona investment_analyst

# Academic research
python run_example.py --persona phd_researcher

# Business consulting
python run_example.py --persona business_consultant
```

## 📈 Performance

- **Model Size**: <100MB (all-MiniLM-L6-v2)
- **Processing Time**: <60s for 3-5 documents
- **Memory Usage**: <2GB RAM
- **CPU Requirements**: Standard x86_64

## 🏗️ Architecture

- **PDF Processor**: Text extraction with PyMuPDF
- **Intelligence Engine**: Semantic analysis with sentence transformers
- **Ranking System**: Hybrid semantic + keyword scoring
- **Output Generator**: Structured JSON formatting

## 📝 Technical Details
🔍 Logic for Round 1B: Policy-Aware PDF Content Extractor
This solution intelligently extracts relevant policy-related content (e.g., GDPR, privacy, confidentiality) from PDF documents using semantic similarity between the document and the user’s intent (persona + task).

📌 Input to the System
PDF document (uploaded by user)

Persona (e.g., "Legal Analyst with expertise in GDPR and privacy")

Job-to-be-done (e.g., "Extract all GDPR and confidentiality-related clauses")

🧠 Core Extraction Logic
1. Text Extraction from PDF (via PyMuPDF)
Each PDF page is parsed to extract:

Full text

Block-wise or paragraph-level chunks

Unicode control characters are removed, and empty lines are filtered out.

Each paragraph is stored along with its corresponding page number.

2. Sentence Embedding (via sentence-transformers)
A semantic vector (embedding) is generated for:

The persona + task input → forms the query embedding

Each paragraph/chunk from the PDF → forms the document embeddings

3. Semantic Similarity Scoring
Cosine similarity is calculated between the query embedding and each paragraph embedding.

Paragraphs with similarity scores above a configurable threshold (e.g., 0.45–0.65) are marked as relevant.

4. Relevance Filtering
Top-N or all relevant matches are extracted.

Each matched paragraph is returned with:

page number

text content

similarity score

5. API Response Construction (FastAPI)
The response JSON includes:

json
Copy
Edit
{
  "persona": "Legal Analyst with expertise in GDPR and privacy",
  "job": "Extract clauses...",
  "matches": [
    {
      "page": 4,
      "score": 0.74,
      "text": "All personal data collected under this agreement shall comply with GDPR regulations..."
    },
    ...
  ]
}
⚙️ Summary of Key Logic Components
Step	Tool/Method	Description
Text Extraction	PyMuPDF (fitz)	Reads PDF page-wise text
Semantic Encoding	sentence-transformers	Converts persona, job, and paragraphs to embeddings
Matching	cosine similarity	Measures alignment between intent and content
Filtering & Ranking	Threshold-based scoring	Filters only meaningful matches
Output	JSON (via FastAPI)	Returns relevant text and page info
See `approach_explanation.md` for detailed technical approach and implementation details.
