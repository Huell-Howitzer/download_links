import re
import urllib.request
import argparse
from tqdm import tqdm
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn


def download_file(url: str, destination: str) -> None:
    """
    Download a file from the specified URL and save it to the given destination.

    Args:
        url (str): The URL of the file to download.
        destination (str): The path where the downloaded file should be saved.

    Raises:
        Exception: If there is an error during the download process.

    Returns:
        None
    """
    try:
        urllib.request.urlretrieve(url, destination)
    except Exception as e:
        print(f"Failed to download: {url}\nError: {e}")


def download_links_from_file(file_path: str, output_dir: str, file_suffixes: list[str]) -> None:
    """
    Download files from a list of links specified in a file.

    This function reads the input file line by line, extracts the links with matching suffixes, and downloads
    each file to the specified output directory.

    Args:
        file_path (str): The path to the input file containing the links.
        output_dir (str): The path to the output directory to save the downloaded files.
        file_suffixes (list[str]): List of file suffixes to download.

    Raises:
        FileNotFoundError: If the input file is not found.

    Prints:
        Information about the progress of the download.

    Returns:
        None
    """
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

        # Initialize the progress bar
        with Progress(
            BarColumn(),
            TextColumn(
                "[progress.description]{task.description}", justify="left"),
            TimeElapsedColumn(),
            console=Console(),
        ) as progress:
            task = progress.add_task("[cyan]Downloading...", total=total_links)
            for link, file_name in downloadable_links:
                destination = f"{output_dir}/{file_name}"
                download_file(link, destination)
                progress.update(task, advance=1)

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

