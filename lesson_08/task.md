# Create application which get data from currency NBRB API and save into multiline-json / csv

1. Create new project on gitlab
    * Project should contain .gitignore file which exclude all non-project files
    * Project should contain README.md with simple documentation
        * Name of project/application
        * Supported Python Interpreters
        * How to install application
        * How to use application
    * (Optional): Makefile
1. Application have ability to run into console with parameters
    * (Mandatory) ISO Code (3 Letters) or ISO Number (3 Digits). [ISO:4217](https://en.wikipedia.org/wiki/ISO_4217)
    * (Optional) Date from. If not set than set `today - 7 day`
    * (Optional) Date to. If not set than set `today`
    * (Optional) Output file. If set than output to file, otherwise send to stdout (console)
    * (Optional) Output Format. Possible values CSV, JSON (multiline, every new line separate json). Default: CSV
    * (Optional) Verbose level. 3 levels.
        * Level 0: Only errors and warnings
        * Level 1: Only errors, warnings and info
        * Level 2: Errors, warnings, info and debug
    * (Optional) Number of workers. __If you wanted you can use implementation from lesson 7, task 3 otherwise ignore 
      and use sequential implementation and ignore parameters__ 
1. Application should build into python package:
    * Source package (tar.gz)
    * Wheel package for each supported version Python Interpreters
    * Installed CLI scripts:
        * (Mandatory) For POSIX/UNIX/MacOS
        * (Optional) For Windows
1. Application should test:
    1. Coverage at least 60%
    2. Lint check passed
    3. (Optional) Test on all Python Interpreters versions
