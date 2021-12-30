import os, re, argparse, shutil
from bs4 import BeautifulSoup
import requests
import logging

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files", nargs='+', required=True, help = "Provide .htm or .html files to download books from")
parser.add_argument("-t", "--types", nargs='+', default=["pdf"], help="Input the versions of the bundle you'd like to download. Ex. -t pdf epub mobi. Default is pdf")
parser.add_argument("--force", action='store_true', default=False, help="Re-download files that already exist. Default is False, supply flag to force download.")
parser.add_argument("-r", "--remove", action='store_true', default=False, help="Delete html and webpage files once complete. Default is False.")
parser.add_argument("-v", action='store_true', default=False, help="Verbose logging.")
args = parser.parse_args()

if args.v:
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(level=level, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def make_bundle_dirs(bundle, type):
    if not os.path.exists(bundle):
        os.makedirs(bundle)
    
    path = f'./{bundle}/{type}'
    if not os.path.exists(path):
        os.makedirs(path)
        
def get_file_links(html_file, file_type):
    links = []
    with open(html_file, 'r', encoding='utf8') as f:
        for line in f:
            if re.search(f"\.{file_type}",line):
                soup = BeautifulSoup(line.strip(), 'html.parser')
                links.append(soup.a['href'])

    return links

def get_filename(url):
    query_string_removed = url.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    return os.path.basename(scheme_removed)

def download_file(bundle, type, link, force):
    fn = get_filename(link)
    path = f'./{bundle}/{type}/{fn}'
    files_downloaded = []
    if not os.path.isfile(path) or force:
        logging.debug(f'Downloading {fn} to {path}')
        r = requests.get(link, allow_redirects=True)
        open(path, 'wb').write(r.content)
        return fn
    else:
       logging.debug(f'{path} already exists and force not set.')

def delete_downloaded_webpage_files(file):
    if os.path.isfile(file):
        os.remove(file) 
        logging.debug(f"Removed {file}.")
    if os.path.isdir(f"{os.path.splitext(file)[0]}_files"):
        shutil.rmtree(f"{os.path.splitext(file)[0]}_files")
        logging.debug(f"Removed {os.path.splitext(file)[0]}_files")

def main():
    for file in args.files:
        if not os.path.isfile(file):
            logging.info(f"{file} doesn't seem to exist, moving to next bundle.")
            continue
        bundle = os.path.splitext(file)[0]
        
        for type in args.types:
            links = get_file_links(file, type)
            if len(links) >= 1:
                logging.info(f"{len(links)} {type}s found.")
                make_bundle_dirs(bundle, type)
                files_downloaded = []
                for link in links:
                    fn = download_file(bundle, type, link, args.force)
                    [files_downloaded.append(fn) if fn != None else True]      
                logging.info(f"{len(files_downloaded)} {type}s downloaded.")
            else:
                logging.info(f"No {type} links found in {file}.")
        
        if args.remove:
            delete_downloaded_webpage_files(file)
            
            

if __name__ == "__main__":
    main()