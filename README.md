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

See `approach_explanation.md` for detailed technical approach and implementation details.