import re
import urllib.request
import argparse
from tqdm import tqdm
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn


def download_file(url, destination):
    try:
        urllib.request.urlretrieve(url, destination)
    except Exception as e:
        print(f"Failed to download: {url}\nError: {e}")


def download_links_from_file(file_path, output_dir, file_suffixes):
    with open(file_path, 'r') as file:
        links = file.readlines()

    downloadable_links = []
    for link in links:
        link_data = link.strip().split('\t')
        if len(link_data) == 2:
            link, name = link_data
            for suffix in file_suffixes:
                if link.endswith(suffix):
                    downloadable_links.append((link, name + suffix))

    total_links = len(downloadable_links)
    if total_links == 0:
        print("No downloadable links found in the input file.")
    else:
        print(f"Found [green]{total_links}[/green] downloadable link(s).\n")

        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading...", total=total_links)
            for link, file_name in downloadable_links:
                destination = f"{output_dir}/{file_name}"
                download_file(link, destination)
                progress.update(task, advance=1)
                progress.refresh()
    print("\nDownload completed.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download files from a list of links')
    parser.add_argument('--input-file', dest='input_file', required=True,
                        help='Path to the input file containing the links')
    parser.add_argument('--output-dir', dest='output_dir', required=True,
                        help='Path to the output directory to save the downloaded files')
    parser.add_argument('--suffixes', nargs='+', required=True,
                        help='File suffix(es) to download')

    args = parser.parse_args()
    input_file = args.input_file
    output_dir = args.output_dir
    file_suffixes = [
        '.' + suffix if not suffix.startswith('.') else suffix for suffix in args.suffixes]

    download_links_from_file(input_file, output_dir, file_suffixes)
    print("\nDownload completed.")

    help_text = f"\n[bold]Help Menu:[/bold]\n\n{parser.format_help()}"

    console = Console()
    console.rule("[bold blue]Help Menu[/bold blue]")
    console.print(help_text, style="bold blue")
