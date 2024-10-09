# Lesson 2: Data Input and Wrangling

## Introduction

In this lesson we will will learn to download a csv file from a website, modify it, and then use the file to download more files.

In this mini-lesson you will learn:
- Load a CSV file from local source
- Download a CSV file from a remote source
- Standard data cleaning practices
  


```python
import pandas as pd
```

## 1 Getting Data

The most basic step in any data science project is actually getting the data. The pandas library makes this very easy if you are working with tabular data. Generally, you will be working with csv files and will be able to use the `read_csv` file.

We know from Gutenberg documentation that Gutenberg keeps a list of all of the books in its catalog a the following address: https://www.gutenberg.org/cache/epub/feeds/

From here we can download the `pg_catalog.csv.gz` file and unzip it.

This step has already been done for you, and the `pg_catalog.csv` file should be in the files you downloaded.


### 1.1 Loading a local file

To load the csv file locally, we only need to add run the command `pd.read_csv(<FILENAME>)`


```python
pd.read_csv("pg_catalog.csv")
```

**Note** all we did here is load the file into the output screen of Jupyter Notebook, we have not actually stored it as a variable we can work with.

We can store it by having the result of the function equal a variable.


```python
df = pd.read_csv("pg_catalog.csv")
```

The csv file has now been stored as a `DataFrame`. A dataframe is a lot like a spreadsheet with columns and rows, but it has some features to optimize it for data science analysis.

We can show the content of the data frame by type `df`. </br>**Note** you do not have to use the name `df`, this is just a convention.

### 1.2 Loading a Remote File

Loading files from a local copy is easy enough, but it does involve extra steps of going to the website and downloading the file. Pandas allows you to skip this file by simply entering the url of the file you want to download. As entering the url can lead to cluttered code, it is best practice to save that as a string variable first.


```python
gutenberg_csv_url = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv.gz"
```


```python
df_remote = pd.read_csv(gutenberg_csv_url)
```

A nice feature of Pandas is that it automatically recognizes common compressed file formats like the `.gz` extension and decompresses them.

#### Critical Thinking: local vs. remote?

When doing any data science project one of the key questions you will have to consider is how you are loading the data for your project. 

> Is it going to be a local copy or a remote connection?

The right answer depends on the use case, but generally what could be some pros and cons of local and remote data?

## 2 Cleaning the DataFrame

Before you start doing anything with your data, you want to make sure you get the DataFrame cleaned up. This will make working with the data easier. 


### 2.1 DataTypes

Part of the power of Pandas is that it assumes that each column of a dataframe is of the same type. It allows it to make calculations faster. When you import from a csv, Pandas is not always able to determine what type of variable is inside the dataframe. We can check how Pandas did by using the `dtypes()` function.


```python
df_remote.dtypes
```

Pandas was able to figure out that the first column was an integer, but it had trouble with the other columns. It saved these as generic `objects`, which means it can be a `string`, `number` , or other types of data formats. This can lead to problems down the road, and Pandas recommends converting these to their own special strings called `StringDType`. This makes for better storage and processing.

To change one column we can use the following logic:

```python
df_remote['Title']=df_remote['Title'].astype(pd.StringDtype())
```
This basically means this: Take the title column `df_remote['Title']` convert the type `.astype` , set the type to `pd.StringDtype`.


Converting each invidividual column is a bit tedious. Since we know that only the first column is correct and all the other columns need to be `StringDtype` we can create a list of column names and apply the changes to that entire range.

```python
cols = df_remote.columns[1:]
df_remote[cols] = df_remote[cols].astype(pd.StringDtype())
```



```python
#create the list of column names
cols = df_remote.columns[1:]
cols
```


```python
df_remote[cols] = df_remote[cols].astype(pd.StringDtype())
```

Now when I check the `dtypes` we should have all strings. 


```python
df_remote.dtypes
```

This is unfortunately a very tedious part of the process, but it can prevent a lot of irritation down the road.

### 2.2 Column Names

Another common issue is poorly formatted column names and making these consistent and usuable will reduce errors down the road.
- Pandas generally likes column names that **do not** include spaces or other special characters.
- use only one lower case for column names (this is purely my own preference!)

#### 2.2.1 Remove special characters

One potential issue is that the first column is called `Text#`, the `#` symbol is a special character that could cause confusion. We want to get rid of it. We can use the `.rename()` method to do so. This works in the following way:

```python
df.rename(columns={"Old Column Name":"New Column Name"})
```


```python
df_remote = df_remote.rename(columns={"Text#": "Text_ID"})
```


```python
df_remote
```

#### 2.2.2 Make all column names lower case

We can also rename the column names as a group by passing a function into the rename method and indicating what axis we want to change. In this case, we are going to convert them all to lower case. This prevents you from having to remember to press shift every time you enter the title of a column.

```python
df.rename(str.lower, axis='columns')
```


```python
df_remote = df_remote.rename(str.lower, axis='columns')
```


```python
df_remote
```

## 3 Cleaning the Data

Once the dataframe is in order you will want to clean up some of the data. This is usually a recursive process. That is, you usually only figure out that there is an issue with the data when you start working on it. As you keep finding issues, you want to clean these issues earlier in your code, rather than when you run into them.

### 3.1 Removing formatting codes

When working with string data one common problem is that sometimes formatting codes or special characters are left in the text. For example, the code `\n` is used to indicate a new line in a text. The title for the *Bill of Rights* in this dataframe has a a subtitle. We can see this by getting the value for that cell. We can use the same list access technique we learned in lesson one to access the fourth column and the second value. The only difference is that we have to provide the column name first.


```python
df_remote['title'][1]
# remember [1] is the second value because the first value is [0]
```

**Note** In the result above the title includes `\r` and `\n`. In theory, we could manually remove this by changing that specific cell. As there are thousands of rows, going through and manually fixing all this would be extremely tedious. Instead, we'll simply tell Pandas to remove all instances of either `\r` or `\n\` in the column.</br>
There are a couple of ways to do this, but we will simply go through and drop the new line or return character and everything that follows it. We do not need the subtitle.

The code for this is:
```python
df_remote['title'] = df_remote['title'].str.replace(r'[\n\r]', ' ', regex=True)
```
This means take the column `title` (`df_remote['title']`) and replace `\n` or an `\r` with a space. 


```python
df_remote['title'] = df_remote['title'].str.replace(r'[\n\r]', ' ', regex=True)
```


```python
df_remote
```

As you work with a DataFrame there are always other formatting quirks in the date you will want to take care of. It makes little sense to try to clean everything in advance and hope for the best. Likely, you'll find problems as you go and then make the fixes part of the cleaning process.

### Creating New Columns/Feature Engineering

The way data is stored in a spreadsheet "in the wild" can vary drastically. The Gutenberg spreadsheet is pretty well organized, but it stores the author name and vital data (birth and death year) all in the same column. This can be difficult to work with. For example, if I want to order the authors by birth year that data is locked into the author names. We want to get that data out and also follow the standard naming convention of having a column for first name and last name, which makes sorting and searching a lot faster.

Since the names all follow a regular pattern: Last Name, First Name, Years, we can split the column into three different columns using the same `str.split` function used above. By default, `expand` is set to `False`. If we set it to `True`, the result will not be a list, but instead more columns. We can determine the total number of splits by using `n=2`. That is, do this for two commas.

Before we actually change the table we want to test out the result.




```python
df_remote['authors'].str.split(', ', n=2, expand=True)
```

This looked liked it worked, but it created an issue for row 74252. Since there multiple authors for this text the function splits the string by `,` but then lumps all the years together. Although this secondary author is not very interesting, we also don't want to delete it just yet in case we need it later. Instead, we'll save this for now by using the same `str.split` function, but applying it to authors for semi-colons `;` and set the number to `n=1` for one column.

Let's test it out before we change the DataFrame.


```python
df_remote['authors'].str.split('; ', n=1, expand=True)
```

This looks good. Let's create a new column called `'second_author'` and store it there.


```python
df_remote
```


```python
df_remote[['first_author','second_author']]=df_remote['authors'].str.split('; ', n=1, expand=True)
```


```python
df_remote
```

Now that that the authors have been split, we can split up the first author name by 'first_name','last_name'.


```python
df_remote[['last_name', 'first_name']] = df_remote['first_author'].str.split(', ', n=1, expand=True)
```


```python
df_remote
```

We now have a `first_name` column and a `last_name` column. We notice there's still a bit of data in the `first_name` column, namely the first name and the birth and death years(i.e. Thomas, 1743-1826). Let's split this again using a comma as our delimeter and creating a column called years.


```python
df_remote[['first_name','years']]=df_remote['first_name'].str.split(',', n=1, expand=True)
```


```python
df_remote
```

We need to split the `years` column into `birth` and `death` years. While it's tempting to use `str.split()` again, this can cause issues with `<NA>` values (i.e., missing values). If the value is `<NA>`, `str.split()` will get confused and throw an error. A better solution is to use `str.extract()`, which allows us to look for specific patterns in the string and pull them out.

In this case, we want to extract four-digit years. Here's how:
  
  - `\d`: This matches any digit character (0, 1, 2, 3, etc.).
  
  - `{4}`: This indicates we are looking for **four digits** in a row.
  
  - `()` (parentheses): These group the four digits together so we can capture them as one unit.

- We also look for another group of four digits on the other side of the hyphen (`-`).

  - For example, in the string `1869-1952`, `str.extract()` will grab `1869` and `1952` and place them in separate columns.

- After extraction, we convert these columns to `Int64`.

  - `Int64` allows us to treat the values as integers while still handling `<NA>` values gracefully.
  
  - Using `Int64` avoids issues that could arise if `<NA>` values are encountered.










```python
df_remote[['birth', 'death']] = df_remote['years'].str.extract(r'(\d{4})-(\d{4})').astype('Int64')
```


```python
df_remote
```

All of these changes leave us with several columns that contain old data, `authors`, `first_author`, `years`. We can remove these using the `.drop()` method on the dataframe. We have to specify the columns we want to drop using `columns=`.


```python
df_remote.drop(columns=['authors','first_author','years'])
```

The above previous shows the desired result. We can make these changes permanent by saving this into df_remote dataframe.


```python
df_remote = df_remote.drop(columns=['authors','first_author','years'])
```

## 4 Saving Progress

For now, we have a DataFrame we can work with although undoubtedly we'll run into unforeseen issues down the road. It is a good practice to save the dataframe. This prevents us from having to run the above code everytime. There are a couple of ways we can save this. We can use the pandas function `to_csv()`, which converts this to a csv file. The advantage of a CSV file is that any computer can read them.
</br> 
There are several issues with CSV files:
- They tend to be big
- Read and write times can be slow
- Will add an empty index column if you are not careful
- Unless you specifically indicate the column types, the dtype will get lost. This is a huge pain.

Alternatively, we can also save this to a `.pickle` file.

**Advantages**

- Smaller
- Faster
- Keeps dtypes

**Disadvantages**

- Requires Python to open
  
  

Saving to pickle file is incredibly simple. 


```python
df_remote.to_pickle('pg_catalog_clean.pickle')
```

The code below should place the file in your working directory.

### 4.1 Testing the Different File Types (optional)

If you are really curious about the difference between `.csv` files and `.pickle` files. The code below shows you both the difference in load time and file size for each. You will also see that the CSV file import caused an extra column to appear `Unnamed:0` and convert all the dtypes back to object and changed the special `Int64` to `float64` which effectively means that 1776 now becomes 1776.0.


```python
df_remote.to_csv('pg_catalog_clean.csv')
```


```python
%timeit df_clean_pg_csv = pd.read_csv('pg_catalog_clean.csv')
```


```python
df_clean_pg_csv = pd.read_csv('pg_catalog_clean.csv')
```


```python
df_clean_pg_csv.dtypes
```


```python
%timeit df_clean_pg_pickle = pd.read_pickle('pg_catalog_clean.pickle')
```


```python
df_clean_pg_pickle = pd.read_pickle('pg_catalog_clean.pickle')
df_clean_pg_pickle.dtypes
```

We can also check how large those files are in memory by calling up the info on the current working directory. We'll note the `csv` files are around 20mb and the `pickle` file is around 15mb.


```python
%ls -Gflash *
```


```python

```
