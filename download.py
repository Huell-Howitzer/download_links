import re
import urllib.request
import argparse
from tqdm import tqdm
from rich.console import Console
from rich.progress import Progress
from rich import print


def download_file(url, destination):
    try:
        urllib.request.urlretrieve(url, destination)
        return True
    except Exception as e:
        print(f"Failed to download: {url}\nError: {e}")
        return False


def download_links_from_file(file_path, output_dir, file_suffixes):
    with open(file_path, 'r') as file:
        links = file.readlines()

    downloadable_links = []
    total_file_size = 0

    for link in links:
        link_data = link.strip().split('\t')
        if len(link_data) == 2:
            link, name = link_data
            for suffix in file_suffixes:
                if link.endswith(suffix):
                    file_size = get_file_size(link)
                    total_file_size += file_size
                    downloadable_links.append((link, name + suffix, file_size))

    total_links = len(downloadable_links)
    if total_links == 0:
        print("No downloadable links found in the input file.")
    else:
        print(f"Found [green]{total_links}[/green] downloadable link(s).\n")

        if total_links > 0 and total_file_size > 0:
            if total_file_size > total_links:
                task_description = "Downloading..."
                total_tasks = total_file_size
            else:
                task_description = "Processing links..."
                total_tasks = total_links

            with Progress() as progress:
                task = progress.add_task(
                    f"[cyan]{task_description}[/cyan]", total=total_tasks)
                for link, file_name, file_size in downloadable_links:
                    destination = f"{output_dir}/{file_name}"
                    success = download_file(link, destination)
                    if success:
                        progress.update(task, advance=file_size)
                    progress.refresh()

    print("\nDownload completed.")


def get_file_size(url):
    response = urllib.request.urlopen(url)
    size = int(response.headers.get("Content-Length", 0))
    return size


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

    console = Console()
    with console.status("[bold green]Processing...", spinner="point") as status:
        download_links_from_file(input_file, output_dir, file_suffixes)
        console.print("\nDownload completed.", style="bold green")

    print("\n[bold]Help Menu:[/bold]\n")
    console.print(parser.format_help())
