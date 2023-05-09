#!/usr/bin/python
import os
import sys
import requests
from urllib.parse import urlparse
import argparse
import gzip


def download(mirror=None, arch=None, file_path="", retries=2):
    """
    Downloads the URL content into the file.
    :param mirror: Debian mirror to download file
    :param url: URL to download file
    :param file_path: Local file name to contain the file downloaded
    :return: New file path. None if the download is failed.
    """
    if not mirror:
        # default mirror link
        mirror = ("http://ftp.uk.debian.org/debian/dists/stable/main/")

    if not arch:
        arch = "amd64"  # default architecture

    if not mirror.endswith("/"):
        mirror = mirror + "/"

    url = mirror + f"Contents-{arch}.gz"

    if not file_path:
        file_path = os.path.realpath(os.path.basename(url))

    print(f"Downloading {url} content to {file_path}")

    url_sections = urlparse(url)
    if not url_sections.scheme:
        print("The given url is missing a scheme. Adding https scheme")
        url = f"http://{url}"
        print(f"New url: {url}")

    for retry in range(1, retries + 1):
        try:
            if retry > 1:
                print("Waiting 5 seconds...")
                # Waiting 5 seconds between dowloads if its failed
                time.sleep(5)
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(file_path, "wb") as output:
                    for chunk in response.iter_content(
                        chunk_size=1024 * 1024 * 2
                    ):  # 2MB chunks for reading file
                        output.write(chunk)
                print("Download finished successfully")
                return file_path
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
        ) as e:
            print(e.args)
            sys.exit(0)

    return None


def run_statistics(content_file=None, top=10):
    """
    Find the statistics of the top 10 packages that have the most files associated with them.
    :param contents: File object to run statistics
    :param top: Value that selects top n packages
    :return: tuples of list with location and count
    """
    statistics = {}
    if not content_file:
        print("Downloaded file content is empty!!!")
        sys.exit(0)

    for content_index in content_file:
        contents = content_index.split(" ")
        locations = contents[-1].strip()
        package_names = locations.split(",")
        for package_name in package_names:
            if package_name in statistics:
                statistics[package_name] += 1
            else:
                statistics[package_name] = 1
    sorted_packages_by_count = sorted(
        statistics.items(), key=lambda p: p[1], reverse=True
    )
    return sorted_packages_by_count[:top]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a",
                        "--arch",
                        help="Architecture - amd64, arm64, mips etc",
                        type=str,
                        required=True,
                        )
    parser.add_argument(
        "-m",
        "--mirror",
        help="Debian mirror to download content indices",
        required=False,
    )
    parser.add_argument(
        "-t",
        "--top",
        help="Set the value to find top n packages",
        required=False,
        type=int,
        default=10,
    )

    args = parser.parse_args()
    arch = args.arch
    mirror = args.mirror
    top = args.top
    local_content_path = download(mirror=mirror, arch=arch)

    if not local_content_path:
        print(f"Something is happened during file download.")

    try:
        # Reading compressed file as text mode
        with gzip.open(local_content_path, "rt", encoding="utf-8") as file:
            sorted_packages = run_statistics(content_file=file, top=top)
            for idx, (package_name, count) in enumerate(sorted_packages):
                print(f"{idx+1}. {package_name} {count}")
    except FileNotFoundError as e:
        print(f"{local_content_path} is not found!!!")
        print(e)
        sys.exit(0)
