import os
import tempfile
import urllib.error
import pytest

from download_links import download_file, download_links_from_file, get_downloadable_links_from_file


@pytest.fixture
def output_dir(tmpdir):
    return tmpdir.strpath


@pytest.fixture
def file_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'test_links.txt')


def test_download_file_success(output_dir):
    url = 'http://example.com/file.pdf'
    destination = os.path.join(output_dir, 'file.pdf')
    download_file(url, destination)
    assert os.path.isfile(destination)


def test_download_file_failure(output_dir):
    url = 'http://example.com/nonexistent.pdf'
    destination = os.path.join(output_dir, 'nonexistent.pdf')
    with pytest.raises(urllib.error.URLError):
        download_file(url, destination)


def test_download_links_from_file(output_dir, file_path):
    file_suffixes = ['.pdf', '.txt']
    download_links_from_file(file_path, output_dir, file_suffixes)
    assert os.path.isfile(os.path.join(output_dir, 'file1.pdf'))
    assert os.path.isfile(os.path.join(output_dir, 'file2.txt'))
    assert not os.path.isfile(os.path.join(output_dir, 'file3.jpg'))


def test_download_links_from_file_no_matching_suffix(output_dir, file_path):
    file_suffixes = ['.doc', '.jpg']
    download_links_from_file(file_path, output_dir, file_suffixes)
    assert not os.path.isfile(os.path.join(output_dir, 'file1.pdf'))
    assert not os.path.isfile(os.path.join(output_dir, 'file2.txt'))
    assert not os.path.isfile(os.path.join(output_dir, 'file3.jpg'))


def test_get_downloadable_links_from_file(file_path):
    expected_links = [
        'http://example.com/file1.pdf',
        'http://example.com/file2.txt',
        'http://example.com/file3.jpg'
    ]
    downloadable_links = get_downloadable_links_from_file(file_path)
    assert downloadable_links == expected_links
