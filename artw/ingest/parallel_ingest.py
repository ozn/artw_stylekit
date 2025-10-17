"""Parallel corpus ingestion."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional
import jsonlines
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from .pdf_parser import extract_text_from_pdf
from ..config import Config
from ..logger import logger

def ingest_corpus(
    src_dir: Path,
    out_file: Path,
    sample: Optional[int] = None,
    workers: Optional[int] = None
) -> int:
    """
    Ingest PDF corpus in parallel.
    
    Args:
        src_dir: Source directory with PDFs
        out_file: Output JSONL file
        sample: Limit to N files (for testing)
        workers: Number of parallel workers
        
    Returns:
        Number of successfully processed files
    """
    workers = workers or Config.MAX_WORKERS
    
    # Find all PDFs
    pdf_files = list(src_dir.rglob("*.pdf"))
    if sample:
        pdf_files = pdf_files[:sample]
    
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    processed = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("Processing PDFs...", total=len(pdf_files))
        
        with jsonlines.open(out_file, mode='w') as writer:
            with ProcessPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(extract_text_from_pdf, pdf): pdf for pdf in pdf_files}
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        writer.write(result)
                        processed += 1
                    progress.update(task, advance=1)
    
    logger.info(f"Successfully processed {processed}/{len(pdf_files)} files")
    return processed
