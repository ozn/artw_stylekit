"""Command-line interface."""
import click
from pathlib import Path
from rich.console import Console
from ..config import Config
from ..logger import logger
import json

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """ARTW StyleKit - Academic writing assistant."""
    Config.ensure_dirs()

@cli.command()
@click.option('--src', type=click.Path(exists=True), required=True, help='Source directory')
@click.option('--out', type=click.Path(), default='data/corpus.jsonl', help='Output JSONL file')
@click.option('--sample', type=int, default=None, help='Limit to N files')
@click.option('--workers', type=int, default=None, help='Parallel workers')
def ingest(src, out, sample, workers):
    """Ingest PDF corpus."""
    from ..ingest.parallel_ingest import ingest_corpus
    
    src_path = Path(src)
    out_path = Path(out)
    
    console.print(f"[bold blue]Ingesting corpus from {src_path}[/]")
    processed = ingest_corpus(src_path, out_path, sample, workers)
    console.print(f"[bold green]✓ Processed {processed} documents → {out_path}[/]")

@cli.command()
@click.option('--corpus', type=click.Path(exists=True), required=True, help='Corpus JSONL file')
@click.option('--out', type=click.Path(), default='data/style_profile.json', help='Output JSON file')
def profile(corpus, out):
    """Generate style profile."""
    from ..analysis.style_profile import StyleProfiler
    
    profiler = StyleProfiler()
    profiler.load_corpus(Path(corpus))
    
    console.print("[bold blue]Analyzing style...[/]")
    profile_data = profiler.analyze()
    
    out_path = Path(out)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(profile_data, f, indent=2, ensure_ascii=False)
    
    console.print(f"[bold green]✓ Profile saved → {out_path}[/]")
    console.print(f"  Documents: {profile_data['document_count']}")
    console.print(f"  Avg length: {profile_data['avg_doc_length']:.0f} words")

@cli.command()
@click.option('--profile', type=click.Path(exists=True), required=True, help='Profile JSON file')
def inspect(profile):
    """Inspect style profile."""
    from rich.table import Table
    
    with open(profile, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    console.print("[bold]Style Profile Summary[/]\n")
    console.print(f"Documents: {data['document_count']}")
    console.print(f"Avg doc length: {data['avg_doc_length']:.0f} words")
    console.print(f"Vocabulary size: {data['vocabulary']['unique_tokens']:,}")
    console.print(f"Lexical diversity: {data['vocabulary']['lexical_diversity']:.3f}")
    console.print(f"Avg sentence: {data['sentence_structure']['avg_sentence_length']:.1f} words\n")
    
    table = Table(title="Top 20 Terms")
    table.add_column("Term", style="cyan")
    table.add_column("Frequency", style="green")
    
    for term, freq in list(data['vocabulary']['top_50_words'].items())[:20]:
        table.add_row(term, str(freq))
    
    console.print(table)

@cli.command()
@click.option('--profile', type=click.Path(exists=True), required=True, help='Style profile JSON')
@click.option('--topic', required=True, help='Article topic')
@click.option('--model', default='mock', help='LLM model (gpt-4, gemini-pro, claude-3, mock)')
@click.option('--out', type=click.Path(), default='out/outline.json', help='Output file')
def generate_outline(profile, topic, model, out):
    """Generate article outline using LLM."""
    from ..prompts.templates import PromptTemplates
    from ..llm.adapter import LLMAdapter
    
    # Load profile
    with open(profile, 'r', encoding='utf-8') as f:
        profile_data = json.load(f)
    
    console.print(f"[bold blue]Generating outline for: {topic}[/]")
    console.print(f"Model: {model}")
    
    # Generate prompt
    prompt = PromptTemplates.get_outline_prompt(topic, profile_data)
    
    # Get LLM response
    llm = LLMAdapter(model=model)
    response = llm.generate(prompt, max_tokens=3000, json_mode=True)
    
    # Save
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        outline = json.loads(response)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(outline, f, indent=2, ensure_ascii=False)
        
        console.print(f"[bold green]✓ Outline saved → {out_path}[/]")
        console.print(f"  Title: {outline.get('title', 'N/A')}")
        console.print(f"  Sections: {len(outline.get('sections', []))}")
    except json.JSONDecodeError:
        # Fallback: save raw response
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(response)
        console.print(f"[yellow]⚠ Response not JSON, saved raw → {out_path}[/]")

@cli.command()
@click.option('--profile', type=click.Path(exists=True), required=True)
@click.option('--topic', required=True)
@click.option('--out', type=click.Path(), default='out/prompts.txt')
def save_prompts(profile, topic, out):
    """Save generated prompts to file (no LLM call)."""
    from ..prompts.templates import PromptTemplates
    
    with open(profile, 'r', encoding='utf-8') as f:
        profile_data = json.load(f)
    
    outline_prompt = PromptTemplates.get_outline_prompt(topic, profile_data)
    citation_prompt = PromptTemplates.get_citation_prompt(profile_data, topic)
    
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("OUTLINE PROMPT\n")
        f.write("=" * 80 + "\n\n")
        f.write(outline_prompt)
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("CITATION PROMPT\n")
        f.write("=" * 80 + "\n\n")
        f.write(citation_prompt)
    
    console.print(f"[bold green]✓ Prompts saved → {out_path}[/]")

@cli.command()
@click.option('--outline', type=click.Path(exists=True), required=True, help='Outline JSON file')
@click.option('--out', type=click.Path(), default='out/article_draft.docx', help='Output DOCX file')
def export_docx(outline, out):
    """Export outline to DOCX document."""
    from ..export.docx_builder import DocxBuilder
    
    # Load outline
    with open(outline, 'r', encoding='utf-8') as f:
        outline_data = json.load(f)
    
    console.print(f"[bold blue]Building DOCX from outline...[/]")
    
    # Build document
    builder = DocxBuilder()
    doc = builder.build_from_outline(outline_data)
    
    # Save
    out_path = Path(out)
    builder.save(out_path)
    
    console.print(f"[bold green]✓ Document saved → {out_path}[/]")
    console.print(f"  Title: {outline_data.get('title', 'N/A')}")

if __name__ == "__main__":
    cli()
