# gutenberg_scraper.py

import requests
import zipfile
from io import BytesIO
import chardet
import logging
import re
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

# Default Gutenberg mirror
gutenberg_mirror = "https://www.gutenberg.org/ebooks"

def gutenberg_text_urls(id: str, mirror=gutenberg_mirror, suffixes=("", "-8", "-0")) -> list[str]:
    """Generate URLs to download the Gutenberg book by ID."""
    id = str(id)  
    path = "/".join(id[:-1]) or "0"
    zip_urls = [f"{mirror}/{path}/{id}/{id}{suffix}.zip" for suffix in suffixes]
    txt_urls = [f"{mirror}/{path}/{id}/{id}{suffix}.txt" for suffix in suffixes]
    return zip_urls + txt_urls

import logging

def download_gutenberg(id: str) -> str:
    urls_to_try = gutenberg_text_urls(id) + [f"https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"]

    # Create a local logger for this function
    logger = logging.getLogger(__name__)
    previous_level = logger.getEffectiveLevel()
    logger.setLevel(logging.ERROR)  # Temporarily suppress warnings

    for url in urls_to_try:
        try:
            r = requests.get(url, allow_redirects=True)
            if r.status_code == 404:
                # Silence 404 warnings by not logging them at all or use debug as previously suggested
                logger.debug(f"404 for {url} - moving to next possible URL.")
                continue
            r.raise_for_status()

            if not r.text.strip():
                logger.debug(f"Empty content at {url} - moving to next possible URL.")
                continue
            break

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            continue
    else:
        logger.error(f"All attempts failed for Gutenberg ID {id}")
        # Restore previous logging level before returning
        logger.setLevel(previous_level)
        return "Unable to download file"

    # Restore the previous logging level after handling downloads
    logger.setLevel(previous_level)

    if 'application/zip' in r.headers.get('Content-Type', ''):
        z = zipfile.ZipFile(BytesIO(r.content))
        if len(z.namelist()) != 1:
            return "Unable to download file"
        file_content = z.read(z.namelist()[0])
        encoding = chardet.detect(file_content)['encoding']
        return file_content.decode(encoding)
    else:
        return r.text

def strip_headers(text: str) -> str:
    """Strips the Project Gutenberg header and footer from the text."""
    header_patterns = [
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"Project Gutenberg's .*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
    ]
    footer_patterns = [
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"End of Project Gutenberg's .*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
    ]

    header_found = False
    for pattern in header_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            text = re.split(pattern, text, maxsplit=1, flags=re.IGNORECASE)[-1]
            header_found = True
            logging.info("Header stripped using pattern: " + pattern)
            break
    if not header_found:
        logging.warning("No recognizable header found.")

    footer_found = False
    for pattern in footer_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            text = re.split(pattern, text, maxsplit=1, flags=re.IGNORECASE)[0]
            footer_found = True
            logging.info("Footer stripped using pattern: " + pattern)
            break
    if not footer_found:
        logging.warning("No recognizable footer found.")

    return text.strip()

def book_text(book_id):
    """Fetches and returns the text content of a book from Project Gutenberg using the book ID."""
    text = download_gutenberg(book_id)
    clean_text = strip_headers(text)
    return clean_text

def fetch_text_data(df):
    """Fetches text data for each book in the DataFrame and inserts it into the 'text_data' column."""
    # Check if 'text_data' column exists
    if 'text_data' in df.columns:
        overwrite = input("'text_data' column already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation aborted. No changes were made.")
            return df

    else:
        df['text_data'] = pd.Series(dtype=pd.StringDtype())

    # Define a function that fetches the text data for a single book ID
    def fetch_and_clean_text(book_id):
        return book_text(book_id)

    # Apply the fetch_and_clean_text function over the DataFrame with a progress bar
    df['text_data'] = df['text_id'].progress_apply(fetch_and_clean_text)

    return df
