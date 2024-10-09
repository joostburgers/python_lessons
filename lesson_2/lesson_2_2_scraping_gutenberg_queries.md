# Lesson 2.2: Scraping Gutenberg: Filtering Queries

So far none of the work we have done on the Gutenberg catalog has not actually gotten us any texts. Instead we did the following:
- Downloaded a CSV file
- Converted it to a dataframe
- Cleaned the dataframe
- Exported as `.pickle` file

We did all this because the dataframe will used to retrieve actual texts from Gutenberg, and we want to be sure everything is clean before we modify it.

In the following lesson you will learn how to filter the dataframe for the specific values you want by running queries. Since we don't want to download all of Gutenberg, we will want to create a subset of data to download before we do the actual webscraping.

#### Load libraries

Libraries need to be reloaded for each new notebook.


```python
import pandas as pd
```

## 1.1 Import `pg_catalog_clean.pickle`


You will need to import the `.pickle` file and save it as a dataframe file.


```python
df_pg_catalog = pd.read_pickle('pg_catalog_clean.pickle')
```


```python
df_pg_catalog
```

## 2 Exploring dataframe content

### 2.1 unique()

Before you start filtering a dataframe you might want to know what's actually inside it. It doesn't make a whole lot of sense to start filtering for values if you don't know what values are possible. Pandas dataframes have a built in `.unique()` method that allows you to view all unique values. Let's start by looking at `type`.


```python
df_pg_catalog['type'].unique()
```

We can see that the type column classifies this has having 7 different types of information. We are only interested in `Text`.

### 2.2 Dot Notation

We can try to see how many languages there are as well. To speed up our typing we can actually use a little trick called "dot notation". As long as the column titles do not contain special characters and are lower case, we do not have to write brackets and the string around the name of the column, but can just put it in lower case after the name of the dataframe. So `df_pg_catalog.language` will give us the `language` column.


```python
df_pg_catalog.language
```

If we want to know the unique values we can simply add `.unique()` after `language`.



```python
df_pg_catalog.language.unique()
```

This is pretty interesting. There are 118 different languages here. Now we know we can limit our search results by simply eliminating everything that is not a text and eliminating everything that is not in english or `en`. Filtering down will be important because some columns may have a very large number of unique values.


```python

```


```python
df_pg_catalog.subjects.unique()
```

There are over 40,000 unique strings in subjects. Figuring out what we want to look at is going to be tricky.

## 3 Filtering the dataframe

### 3.1 Simple Filtering with `==` (Equal to)

Filtering data in pandas is pretty intuitive. You access the column and then retrieve the value(s) that are interesting to you. For strings, the simplest operation is the - **`==` (Equal to)** operator. This:
  - Checks if values in a column are equal to a certain value.
  - Returns **True** where the condition is met.

For example: 

```python
df_pg_catalog.language=='en'
```

Will give us a list of all of the cases where this is `True` or `False`.
    


```python
df_pg_catalog.language=='en'
```

This is a bit confusing because now have lost our table. In order to get it back, we have to wrap `df_pg_catalog.language=='en'` in the dataframe:

```python
df_pg_catalog[df_pg_catalog.language=='en']
```
This will return the dataframe, but only in cases where `langauge=='en'` is `True`


```python
df_pg_catalog[df_pg_catalog.language=='en']
```

We see that the number of rows is now down to 59485. This means we've eliminated about 10k texts.

We can do the same thing for type. Since we only want `Text` we can filter for that.



```python
df_pg_catalog[df_pg_catalog.type=='Text']
```

Something strange happened. We are back to 73k rows, meaning that the number has gone back up. This is confusing. The reason for this is that we did not save the last query and are therefore starting from scratch. We have to run both queries and save the result when we do so.

### 3.2 Combining Queries with `&`


We want to save both queries and eliminate things that are not in English and things that are not texts. We in theory we could do the following:

```python
df_pg_catalog_english = df_pg_catalog[df_pg_catalog.language=='en']
df_pg_catalog_english_texts = df_pg_catalog_english[df_pg_catalog_english.type=='Text']
```

This first saves one copy of English works and then another copy of English texts.


```python
df_pg_catalog_english = df_pg_catalog[df_pg_catalog.language=='en']
df_pg_catalog_english_texts = df_pg_catalog_english[df_pg_catalog_english.type=='Text']
df_pg_catalog_english_texts
```

This gets us the result we want, but it's pretty cumbersome because we have two separate queries. We can also simply combine queries using the `&` `and` operator. 

- **`&` (Logical AND)**
  - Combines two conditions.
  - Both conditions must be **True** for the result to be **True**.
  

```python
df_pg_catalog[(df_pg_catalog.language=='en') & 
                (df_pg_catalog.type=='Text')
]
```

We are returning a dataframe `df_pg_catalog[]` where both `(df_pg_catalog.language=='en')` AND  `(df_pg_catalog.type=='Text')` are true.



```python
df_pg_catalog[(df_pg_catalog.language=='en') & 
                (df_pg_catalog.type=='Text')
]

```

### 3.3 Looking for keywords with `str.contains()`

So far we have looked at columns that have pretty regular set of values: 7 media types and 128 languages. Yet, using a literal search string for subjects will not work because there are too many types of strings.


```python
df_pg_catalog[df_pg_catalog.subjects=="Virginia"]
```

There is no text that uses the word `Virginia` as its subject. Nevertheless, there are many texts that have the word `Virginia` in its subject string of words. This is where the method `str.contains` is extremely useful. It will look through the string and find any match for the word we are looking for. We can even have it be case sensetive and ignore `na` values.

```python
df_pg_catalog.subjects.str.contains('Virginia', case=False, na=False)
```

`case` indicates that the search is case sensitive. Since it doesn't matter if Virginia is capitalized or not, we can leave this as `false`. `na=False` means that it will return `False` if the value for that particular record equals `na`.


```python

```


```python
df_pg_catalog[df_pg_catalog.subjects.str.contains('Virginia', case=False, na=False)]
```

This table is much more manageable! Only 177 results.

### 3.4 Eliminating results with ~ NOT

The result from the query for texts where the subject contains `Virginia` is a lot more manageable, but it also includes texts that may not be interesting. For example, it contains *The Red Badge of Courage* by Stephen Crane, which is `fiction`. We may remember that `fiction` gave Moretti a lot of headaches, so perhaps we simply eliminate that. If want to exclude fiction from our search we can use the `~` operator to indicate NOT. That is, return the row as long as the subject does **not** contain fiction.
```python
df_pg_catalog[~df_pg_catalog.subjects.str.contains('fiction', case=False, na=False)]
```
We simply put the `~` to indicate **not**.


```python
df_pg_catalog[~df_pg_catalog.subjects.str.contains('fiction', case=False, na=False)]
```

Again, we are back to more results because we did not combine the queries.


```python
df_pg_catalog[(df_pg_catalog.subjects.str.contains('Virginia', case=False, na=False)) &
                (~df_pg_catalog.subjects.str.contains('fiction', case=False, na=False))
]
```

This elimimated another 70 texts. Great!

### 3.4 Broadening a search with `|` **or** and `*` **Wildcard**

We notice in the results above that there are still texts that might not be that interesting for example *Give Me Liberty or Give Me Death* is a speech. We also want to eliminate this from the results. Intuitively, we could create a new search string:

```python
~df_pg_catalog.subjects.str.contains('speeches', case=False, na=False)
```

This creates two problems. 
1. We are generating another line of code that can become cumbersome to read.
2. Since we are looking specifically for subjects that contain `speeches` it might still return any subject that contains `speech`.

We can fix the first problem by using the `|` **or** operator.

```python
~df_pg_catalog.subjects.str.contains('fiction'|'speeches', case=False, na=False)
```

Now we actually look for `fiction` or `speeches` in the subject.

We can fix the second problem by using a wildcard `*` at the end of `speech.*`. This will give us both `speech` and `speeches`. Specifically, it gives us `speech` and all possible variants.




```python
df_pg_catalog[(df_pg_catalog.subjects.str.contains('Virginia', case=False, na=False)) &
                (~df_pg_catalog.subjects.str.contains('fiction|speech.*', case=False, na=False))
]
```

This eliminated two more results that were speeches.

### 3.5 Combining it all

Now that we have the logic in place we can create one long search string:

```python
df_pg_catalog[
   (df_pg_catalog.language == 'en') & 
    (df_pg_catalog.type == 'Text') &
    (df_pg_catalog.subjects.str.contains('Virginia', case=False, na=False)) & 
    (~df_pg_catalog.subjects.str.contains('fiction|speech.*', case=False, na=False)) 
] 
```


```python
df_pg_catalog[
    (df_pg_catalog.language == 'en') & 
    (df_pg_catalog.type == 'Text') &
    (df_pg_catalog.subjects.str.contains('Virginia', case=False, na=False)) & 
    (~df_pg_catalog.subjects.str.contains('fiction|speech.*', case=False, na=False)) 
] 
```

Great that gave us 96 results. We can now save this into a new dataframe.

## 4 Saving to a new Dataframe with `.copy()`

So far none of the queries we made were permanent. All we did was write out the query and test the result. As you get more experienced, you will likely not separate this out into different test queries, but will run one query all at once.<br> 

We can save the filtered dataframe in two way **shallow copy** and **deep copy**.

When we use the `=` operator pandas creates a **shallow copy** of the query results and puts them in a new dataframe called `df_virginia_history`. This means that there are still links between `df_virginia_history` and `df_pg_catalog`. This can sometimes have unexpected results where you modify one dataframe and it also changes the other one. We can prevent this by using the method `.copy()` at the end of the query chain to make a **deep copy**. This is an entirely seperate dataframe.


```python
df_virginia_history = df_pg_catalog[
    (df_pg_catalog.language == 'en') & 
    (df_pg_catalog.type == 'Text') &
    (df_pg_catalog.subjects.str.contains('Virginia', case=False, na=False)) & 
    (~df_pg_catalog.subjects.str.contains('fiction|speech.*', case=False, na=False)) 
].copy()
```


```python
df_virginia_history
```

We can use our `.pickle()` function to export this and not have to worry about doing all this again.


```python
df_virginia_history.to_pickle('virginia_history.pickle')
```


```python

```
