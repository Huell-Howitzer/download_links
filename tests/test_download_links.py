import os
import tempfile
import urllib.error
import pytest

from download_links import download_file, download_links_from_file


@pytest.fixture
def output_dir(tmpdir):
    return tmpdir.strpath


@pytest.fixture
def file_path():
    return os.path.join(os.path.dirname(__file__), '..', 'list.txt')


def test_download_file_success(output_dir):
    """
    Test successful file download.

    This test verifies that the download_file function successfully downloads a file from a given URL.
    """
    url = 'http://example.com/file.pdf'
    destination = os.path.join(output_dir, 'file.pdf')
    download_file(url, destination)
    assert os.path.isfile(destination)


def test_download_file_failure(output_dir):
    """
    Test failed file download.

    This test verifies that the download_file function raises an URLError when the file download fails.
    """
    url = 'http://example.com/nonexistent.pdf'
    destination = os.path.join(output_dir, 'nonexistent.pdf')
    with pytest.raises(urllib.error.URLError):
        download_file(url, destination)


def test_download_links_from_file(output_dir, file_path):
    """
    Test downloading links from file.

    This test verifies that the download_links_from_file function correctly downloads files based on the links
    provided in a file.
    """
    file_suffixes = ['.pdf', '.txt']
    download_links_from_file(file_path, output_dir, file_suffixes)
    assert os.path.isfile(os.path.join(output_dir, 'file1.pdf'))
    assert os.path.isfile(os.path.join(output_dir, 'file2.txt'))
    assert not os.path.isfile(os.path.join(output_dir, 'file3.jpg'))


def test_download_links_from_file_no_matching_suffix(output_dir, file_path):
    """
    Test downloading links with no matching suffix.

    This test verifies that the download_links_from_file function does not download any files when there are no
    matching suffixes specified.
    """
    file_suffixes = ['.doc', '.jpg']
    download_links_from_file(file_path, output_dir, file_suffixes)
    assert not os.path.isfile(os.path.join(output_dir, 'file1.pdf'))
    assert not os.path.isfile(os.path.join(output_dir, 'file2.txt'))
    assert not os.path.isfile(os.path.join(output_dir, 'file3.jpg'))


def test_get_downloadable_links_from_file(file_path):
    """
    Test getting downloadable links from file.

    This test verifies that the get_downloadable_links_from_file function correctly extracts the downloadable links
    from a file.
    """
    expected_links = [
        'http://example.com/file1.pdf',
        'http://example.com/file2.txt',
        'http://example.com/file3.jpg'
    ]
    downloadable_links = get_downloadable_links_from_file(file_path)
    assert downloadable_links == expected_links

