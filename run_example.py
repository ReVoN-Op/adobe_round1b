#!/usr/bin/env python3
"""
Example runner for the PDF Intelligence System
Demonstrates usage with sample data
"""

import json
import shutil
from pathlib import Path
import subprocess
import sys

def setup_example_data():
    """Setup example input data"""
    input_dir = Path("data/input")
    input_dir.mkdir(parents=True, exist_ok=True)
    
    # Create example persona and job descriptions
    examples = {
        "investment_analyst": {
            "persona": "Investment Analyst with 5 years experience in technology sector analysis, specialized in revenue trends and competitive positioning",
            "job_to_be_done": "Analyze revenue growth patterns, market share trends, and competitive advantages across technology companies from their annual reports"
        },
        "phd_researcher": {
            "persona": "PhD researcher in Computer Science focusing on machine learning and artificial intelligence applications",
            "job_to_be_done": "Extract methodological approaches, experimental results, and key findings for literature review on AI/ML techniques"
        },
        "business_consultant": {
            "persona": "Senior business strategy consultant with expertise in digital transformation and operational efficiency",
            "job_to_be_done": "Identify strategic initiatives, digital transformation efforts, and operational improvements from corporate strategy documents"
        }
    }
    
    return examples

def run_example(persona_type: str = "investment_analyst"):
    """Run example analysis"""
    examples = setup_example_data()
    
    if persona_type not in examples:
        print(f"Unknown persona type: {persona_type}")
        print(f"Available types: {list(examples.keys())}")
        return
    
    example = examples[persona_type]
    
    # Check if PDFs exist
    input_dir = Path("data/input")
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if len(pdf_files) < 3:
        print(f"Error: Need at least 3 PDF files in {input_dir}")
        print("Please add your PDF documents to the data/input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")
    
    # Run analysis
    cmd = [
        sys.executable, "main.py",
        "--input-dir", "data/input",
        "--output-file", f"data/output/analysis_{persona_type}.json",
        "--persona", example["persona"],
        "--job-to-be-done", example["job_to_be_done"]
    ]
    
    print(f"\nRunning analysis for {persona_type}...")
    print(f"Persona: {example['persona'][:80]}...")
    print(f"Task: {example['job_to_be_done'][:80]}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("\n✅ Analysis completed successfully!")
            print(result.stdout)
            
            # Display results summary
            output_file = f"data/output/analysis_{persona_type}.json"
            if Path(output_file).exists():
                with open(output_file, 'r') as f:
                    results = json.load(f)
                
                print(f"\n📊 Results Summary:")
                print(f"Documents analyzed: {len(results['metadata']['input_documents'])}")
                print(f"Relevant sections found: {len(results['extracted_sections'])}")
                print(f"Detailed subsections: {len(results['subsection_analysis'])}")
                
                print(f"\n🔍 Top 3 Most Relevant Sections:")
                for i, section in enumerate(results['extracted_sections'][:3]):
                    print(f"  {i+1}. {section['section_title']} (Page {section['page']})")
        else:
            print(f"\n❌ Analysis failed!")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("\n⏰ Analysis timed out (120s limit exceeded)")
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run PDF Intelligence System example')
    parser.add_argument('--persona', type=str, default='investment_analyst',
                       choices=['investment_analyst', 'phd_researcher', 'business_consultant'],
                       help='Example persona type to use')
    
    args = parser.parse_args()
    run_example(args.persona)