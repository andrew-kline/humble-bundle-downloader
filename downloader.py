import argparse
import logging
import os
import re
import shutil

from bs4 import BeautifulSoup
import requests


parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--files",
    nargs="+",
    required=True,
    help="Provide .htm or .html files to download books from. Space separated. Ex -f bundle1.html bundle2.html",
)
parser.add_argument(
    "-d",
    "--destination",
    help="Destination directory for output files. Default will be the directory where the html file lives.",
)
parser.add_argument(
    "-t",
    "--types",
    nargs="+",
    default=["pdf"],
    help="Input the versions of the bundle you'd like to download. Space separated. Ex. -t pdf epub mobi. Default is pdf",
)
parser.add_argument(
    "--force",
    action="store_true",
    default=False,
    help="Re-download files that already exist. Default is False, supply flag to force download.",
)
parser.add_argument(
    "-r",
    "--remove",
    action="store_true",
    default=False,
    help="Delete html and webpage files once complete. Default is False.",
)
parser.add_argument("-v", action="store_true", default=False, help="Verbose logging.")
args = parser.parse_args()

if args.v:
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(
    level=level, format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)
logger = logging.getLogger()
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

def make_bundle_dirs(destination, type):
    if not os.path.exists(destination):
        os.makedirs(destination)

    path = f"{destination}/{type}"
    if not os.path.exists(path):
        os.makedirs(path)


def get_file_links(html_file, file_type):
    links = []
    with open(html_file, "r", encoding="utf8") as f:
        for line in f:
            if re.search(f"\.{file_type}", line):
                soup = BeautifulSoup(line.strip(), "html.parser")
                links.append(soup.a["href"])

    return links


def get_filename(url):
    query_string_removed = url.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]

    return os.path.basename(scheme_removed)


def download_file(destination, type, link, force):
    fn = get_filename(link)
    path = f"{destination}/{type}/{fn}"
    if not os.path.isfile(path) or force:
        logger.debug(f"Downloading {fn} to {path}")
        r = requests.get(link, allow_redirects=True)
        open(path, "wb").write(r.content)
    else:
        logger.debug(f"{path} already exists and force not set")

    return fn


def delete_downloaded_webpage_files(file):
    if os.path.isfile(file):
        os.remove(file)
        logger.debug(f"Removed {file}.")
    if os.path.isdir(f"{os.path.splitext(file)[0]}_files"):
        shutil.rmtree(f"{os.path.splitext(file)[0]}_files")
        logger.debug(f"Removed {os.path.splitext(file)[0]}_files")


def main():
    for file in args.files:
        if not os.path.isfile(file):
            logger.info(f"{file} doesn't seem to exist, moving to next bundle.")
            continue
        else:
            logger.debug(f"{file} exists, continuing.")

        if not args.destination:
            destination = os.path.splitext(file)[0]
        else:
            destination = os.path.normpath(args.destination)

        for type in args.types:
            links = get_file_links(file, type)
            if links:
                logger.info(f"{len(links)} {type}s found.")
                make_bundle_dirs(destination, type)
                files_downloaded = []
                for link in links:
                    fn = download_file(destination, type, link, args.force)
                    [files_downloaded.append(fn) if fn else True]
                logger.info(f"{len(files_downloaded)} {type}s downloaded.")
            else:
                logger.info(f"No {type} links found in {file}.")

        if args.remove:
            delete_downloaded_webpage_files(file)


if __name__ == "__main__":
    main()
