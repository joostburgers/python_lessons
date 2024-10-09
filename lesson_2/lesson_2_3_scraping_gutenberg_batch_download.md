# Lesson 2_3: Scraping Gutenberg: Batch Download



## 1 Introduction

Up to this point, we have only downloaded and modified a data table we found on Gutenberg. This table is important because it contains the `ID` numbers for every Gutenberg text. With these numbers we can scrape and access virtually every text because the naming conventions for each individual site are consistent.

For example, the `txt` file for *Huckleberry Finn* by Mark Twain is stored here:

https://www.gutenberg.org/cache/epub/76/pg76.txt

Meanwhile the `txt` file for *Tom Sawyer* by Mark Twain is stored here:

https://www.gutenberg.org/cache/epub/74/pg74.txt

The only difference is that one is stored at `76` and the other is stored at `74`. Consequently, if we want to download a batch of specific files, we only really need their ID numbers, since this is the only thing that changes in the web address.

Indeed, we could simply make a list of ID's we want to download and loop through it. We can write this out as pseudo-code as something like this.

```python
df_texts = []
list1 = [74, 75, 76]
for x in list1:
    new_text = download_text('https://www.gutenberg.org/cache/epub/' +x)
    df_texts.append(new_text)
```
The above code won't work but this is the core principle.

## 2 Problems

There are a number of technical issues with simply looping through a whole bunch of Gutenberg sites and downloading these texts. Explaining these technical issues in full is not very interesting and beyond the scope of this course. Briefly they include:
- Gutenberg doesn't like robots, so we have to use specific servers
- Not all texts are on the same servers so we have to switch servers
- The web address is not always 100% the same
- The text still has metadata

Fortunately, a kind [coder](https://skeptric.com/gutenberg/) has already solved many of these problems. All I have done is modified some of their code for our purposes. We won't get bogged down with the details.

## 3 Solutions

We will be using the `tqdm` package to check our progress when we download the files.


```python
try:
    import tqdm  # Replace with the package you want to check
    print("tqdm is already installed.")
except ImportError:
    print("tqdm is not installed. Installing...")
    # Use magic command to install the package
    %pip install tqdm
```


```python
# Importing the necessary libraries
import re            # Use regular rexpressions
from io import BytesIO  # For handling byte streams (used for unzipping files)
from tqdm import tqdm  # For showing a progress bar when downloading multiple files
import requests  # This library helps us download web pages
import logging   # This library helps us print helpful messages to understand what the code is doing
import zipfile   # Helps unzip files that are compressed
import chardet   # Detects the encoding of text
import pandas as pd  # Pandas helps us work with tables of data

```

### 3.1 Get Web scraping server info

Get the page that has a list of all of the robot servers


```python
gutenberg_robot_url = "http://www.gutenberg.org/robot/harvest?filetypes[]=txt"
r = requests.get(gutenberg_robot_url)
```

Get the link for each individual mirror


```python
gutenberg_mirror = re.search('(https?://[^/]+)[^"]*.zip', r.text).group(1)
```

### 3.2 Loop through mirrors

Search through each mirror to see if it has the file we need


```python
def gutenberg_text_urls(id: str, mirror=gutenberg_mirror, suffixes=("", "-8", "-0")) -> list[str]:
    """
    Generate URLs to download the Gutenberg book by ID.
    
    Args:
        id (str): The book ID from Project Gutenberg.
        mirror (str): The mirror URL for Project Gutenberg.
        suffixes (tuple): Possible suffixes for the book file.
        
    Returns:
        list[str]: A list of possible URLs for downloading the book.
    """
    # Convert id to a string to ensure slicing works
    id = str(id)  
    
    # The path is created using all but the last character of the ID, or '0' if the ID is short
    path = "/".join(id[:-1]) or "0"
    
    # Generate URLs using the mirror, path, and suffixes for both .zip and .txt files
    zip_urls = [f"{mirror}/{path}/{id}/{id}{suffix}.zip" for suffix in suffixes]
    txt_urls = [f"{mirror}/{path}/{id}/{id}{suffix}.txt" for suffix in suffixes]
    
    return zip_urls + txt_urls  # Return both zip and text URLs


```

### 3.3 Create Download Function

Create a download function to get and extract each individual book


```python


def download_gutenberg(id: str) -> str:
    """
    Download the book from Project Gutenberg by its ID,
    and unzip the content if necessary.
    
    Args:
        id (str): Gutenberg book ID.
    
    Returns:
        str: The content of the book as a text string or an error message.
    """
    urls_to_try = gutenberg_text_urls(id) + [
        f"https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
    ]

    for url in urls_to_try:
        try:
            # Make the request and handle redirects
         #   print(f'Downloading {id} at {url}')

            r = requests.get(url, allow_redirects=True)
            
            # Check for any 404 errors
            if r.status_code == 404:
                logging.warning(f"404 for {url} - moving to next possible URL.")
                continue
            
            # Raise an HTTPError if the status is 4XX or 5XX
            r.raise_for_status()

            # Log the final URL after any redirection
            logging.info(f"Final URL after redirection: {r.url}")

            # Check if the content is empty
            if not r.text.strip():
                logging.warning(f"Empty content at {url} - moving to next possible URL.")
                continue
            
            # If content is valid, break and use it
            logging.info(f"Downloaded content from {r.url}")
            break

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            continue
    else:
        logging.error(f"All attempts failed for Gutenberg ID {id}")
        return "Unable to download file"

    # Handle .zip files or regular text files
    if 'application/zip' in r.headers.get('Content-Type', ''):
        z = zipfile.ZipFile(BytesIO(r.content))
        if len(z.namelist()) != 1:
            return "Unable to download file"  # Return error if unexpected file count
        
        # Read the file and detect encoding
        file_content = z.read(z.namelist()[0])
        encoding = chardet.detect(file_content)['encoding']
        return file_content.decode(encoding)  # Decode using detected encoding
    else:
        return r.text  # Return text content if it’s not a zip file


```

### 3.4 Strip Metadata

Use a small helper function to strip all of hte metadata from the text


```python
import re
import logging

def strip_headers(text: str) -> str:
    """
    Strips the Project Gutenberg header and footer from the text.
    
    Args:
        text (str): The full text of the book, potentially including headers and footers.
    
    Returns:
        str: The text of the book without the Project Gutenberg header and footer.
    """
    # Patterns to match the start and end of the main text in different versions
    header_patterns = [
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",  # Common header pattern
        r"Project Gutenberg's .*",  # Alternative header for older books
        r"START OF THE PROJECT GUTENBERG EBOOK",  # Some books may have this
    ]
    
    footer_patterns = [
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",  # Common footer pattern
        r"End of Project Gutenberg's .*",  # Alternative footer for older books
        r"END OF THE PROJECT GUTENBERG EBOOK",  # Some books may have this
    ]
    
    # Try matching headers
    header_found = False
    for pattern in header_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            text = re.split(pattern, text, maxsplit=1, flags=re.IGNORECASE)[-1]
            header_found = True
            logging.info("Header stripped using pattern: " + pattern)
            break

    # If no header was found, log a warning
    if not header_found:
        logging.warning("No recognizable header found.")

    # Try matching footers
    footer_found = False
    for pattern in footer_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            text = re.split(pattern, text, maxsplit=1, flags=re.IGNORECASE)[0]
            footer_found = True
            logging.info("Footer stripped using pattern: " + pattern)
            break

    # If no footer was found, log a warning
    if not footer_found:
        logging.warning("No recognizable footer found.")

    # Return the cleaned text, ensuring the entire text is not stripped
    return text.strip()

```

### 3.4 Download and Strip

Create a main function that runs the above two functions to download an individual book clean it and return it.


```python
def book_text(book_id):
    """
    Fetches and returns the text content of a book from Project Gutenberg using the book ID.
    
    Args:
        book_id (str): The Gutenberg book ID.
    
    Returns:
        str: The cleaned book text.
    """
    # download_gutenberg already returns the text content as a string
    text = download_gutenberg(book_id)
    
    # Clean the text by stripping the headers/footers (optional, depends on your implementation)
    clean_text = strip_headers(text)
    
    return clean_text

```

### 3.5 Create DataFrame column `text_data`

This function calls `book_text()` for each `text_id` in the supplied dataframe.


```python
def fetch_text_data(df):
    """
    Fetches text data for each book in the DataFrame and inserts it into the 'text_data' column.
    If 'text_data' already exists, prompts the user for confirmation before overwriting.
    
    Args:
        df (pd.DataFrame): A DataFrame that contains a column with book IDs (e.g., 'text#').
    
    Returns:
        pd.DataFrame: The DataFrame with an additional or updated 'text_data' column.
    """
    # Check if 'text_data' column exists
    if 'text_data' in df.columns:
        overwrite = input("'text_data' column already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation aborted. No changes were made.")
            return df  # Return the DataFrame unchanged

    else:
        # Initialize 'text_data' with string dtype if not present
        df['text_data'] = pd.Series(dtype=pd.StringDtype())

    # Iterate over rows with tqdm progress bar
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Fetching text data"):
        text_id = row['text_id']  # Assuming 'text_id' column has the book IDs
        text = book_text(text_id)  # Fetch the text data using book_text() function
        
        # Assign the fetched text directly to the 'text_data' column
        df.loc[index, 'text_data'] = text

    return df
```

## 4 All you really need to know!

Since most of the scraping has been setup in this file, you are safe to simply import your `.pickle` file and then run the function `fetch_text_data()` with the name of the dataframe inside the parenthesis.


```python
df_virginia = pd.read_pickle('virginia_history.pickle')
```


```python
df_virginia.head(15)

```


```python
fetch_text_data(df_virginia)
```

We can see in the result that a new column has been created and that the full-text of each text has been written into each cell.

Since it is hard to read the cells in the dataframe, by checking an individual cell. Since our column titles are lower case and do not have special characters or spaces, we can use dot notation to access the column: `df_virginia.text_data`. We can then use get the row of our choosing by using `.iloc[row_index]`. Finally, we can slice the string down to 1000 characters by using list slicing `[:1000]`.


```python
df_virginia.text_data.iloc[3][:1000]
```

### 4.1 Overwrite protection

The function has overwrite protection built in. If the `text_data` column already exists you can choose not to run the function.


```python
fetch_text_data(df_virginia)
```

### 4.2 Save result

Save the result as a pickle file for later use.


```python
df_virginia.to_pickle('df_virginia_text.pickle')
```


```python

```
