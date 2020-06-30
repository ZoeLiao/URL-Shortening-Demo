# URL-Shortening-Demo
This respository is a URL shortening demo website.

## Backend

### Set Up
- Create virtual environment: `python3 -v venv venv`
- Activate virtual environment:
    - Mac: `. venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Migrate Database: `python manage.py migrate`
- Start project: `python3 manage.py runserver`
- Local URL: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### How to use
- You can create a short URL by POST [/shortener/](http://localhost:8000/shortener/).
- After getting the short URL, you can request it and get the website.
![./images/demo.gif](./images/demo.gif)

## Test
- Run test scripts: `python manage.py test`

## Results

Results       | Code  | Message         | Error Detail
--------------|:-----:|----------------:| -----------:
Success       | 0000  |  Success        |  None       
Database Error| 1000  |  Database Error |  \<String\>   
Request Error | 2000  |  Request Error  |  \<String\>   
