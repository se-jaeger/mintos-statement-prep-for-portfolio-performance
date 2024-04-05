# Prepare [Mintos](https://www.mintos.com/) Statements for [Portfolio Performance](https://www.portfolio-performance.info/) Import

Simple CLI that 
1. reads all CSV files in the current working directory
2. concatenates them
3. processes the statements
   1. map Mintos types to Portfolio Performance types
   2. sums all statements for each day and type to minimize rounding inaccuracies ([see here](https://github.com/portfolio-performance/portfolio/issues/1682#issuecomment-667650637))
4. export processed data as CSV to import into Portfolio Performance

## Some Notes
Simple tool implemented to make my personal workflow more convenient. However, maybe it also helps you.

**Tested for:**
- German Mintos exports and Portfolio Performance
- MacOS
- Python 3.10/3.12
- Poetry installed package

I don't see a reason why it shouldn't work for another technical setup. Only `pandas` is a requirement. PR's are welcome to make the code more generic regarding language settings.

## Usage
1. clone repo: `git clone git@github.com:se-jaeger/mintos-statement-prep-for-portfolio-performance.git`
2. install package: `poetry install`
3. download statements form Mintos and add to `data` directory
4. run the tool and follow instructions
    ```python
    ➜ $ prep-mintos-statements
    Using the following files: ['2023-12-09.csv', '2022-account-statement.csv', '2021-36326852-eur-de-statement.csv', '2020-36326852-eur-de-statement.csv', '2023-account-statement.csv']
    OK (Y/N)? y

    Using the following output file: 2023-12-09.csv
    OK (Y/N)? y
    ```
5. import the output file into Portfolio Performance (it should detect duplicates and not reimport them)