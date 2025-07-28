#!/usr/bin/env python3
"""
PDF Intelligence System - Main Entry Point
Adobe Hackathon 2025 Round 1B Solution
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any
import argparse

from src.pdf_processor import PDFProcessor
from src.intelligence_engine import IntelligenceEngine
from src.utils.logger import setup_logger
from src.models.schemas import AnalysisInput, AnalysisOutput

def main():
    """Main entry point for the PDF Intelligence System"""
    parser = argparse.ArgumentParser(description='PDF Intelligence System')
    parser.add_argument('--input-dir', type=str, default='data/input', 
                       help='Directory containing PDF files')
    parser.add_argument('--output-file', type=str, default='data/output/analysis_results.json',
                       help='Output JSON file path')
    parser.add_argument('--persona', type=str, required=True,
                       help='Persona description (role and expertise)')
    parser.add_argument('--job-to-be-done', type=str, required=True,
                       help='Specific task to be accomplished')
    parser.add_argument('--config', type=str, default='config/default.json',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger()
    logger.info("Starting PDF Intelligence System")
    
    try:
        # Initialize components
        pdf_processor = PDFProcessor()
        intelligence_engine = IntelligenceEngine()
        
        # Load PDFs from input directory
        input_dir = Path(args.input_dir)
        pdf_files = list(input_dir.glob("*.pdf"))
        
        if len(pdf_files) < 3:
            raise ValueError(f"Need at least 3 PDF files, found {len(pdf_files)}")
        if len(pdf_files) > 10:
            raise ValueError(f"Maximum 10 PDF files allowed, found {len(pdf_files)}")
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Create analysis input
        analysis_input = AnalysisInput(
            pdf_paths=[str(path) for path in pdf_files],
            persona=args.persona,
            job_to_be_done=args.job_to_be_done
        )
        
        # Process documents
        start_time = time.time()
        
        # Extract text from PDFs
        logger.info("Extracting text from PDFs...")
        documents = []
        for pdf_path in pdf_files:
            doc_data = pdf_processor.extract_text_with_structure(pdf_path)
            documents.append(doc_data)
        
        # Analyze with intelligence engine
        logger.info("Analyzing content relevance...")
        analysis_result = intelligence_engine.analyze(documents, analysis_input)
        
        processing_time = time.time() - start_time
        logger.info(f"Processing completed in {processing_time:.2f} seconds")
        
        # Save results
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result.dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {output_path}")
        
        # Print summary
        print(f"\n=== ANALYSIS COMPLETE ===")
        print(f"Documents processed: {len(pdf_files)}")
        print(f"Processing time: {processing_time:.2f}s")
        print(f"Relevant sections found: {len(analysis_result.extracted_sections)}")
        print(f"Subsections analyzed: {len(analysis_result.subsection_analysis)}")
        print(f"Results saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()