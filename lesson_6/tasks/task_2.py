""" Task 2: Implement custom requests auth class

Requirements:
    1. This class should take two mandatory arguments:
        a. key_id: string
        b. secret_key: string
    2. If http method one of: POST, PUT, PATCH than add to json data additional keys:
        {'key_id': key_id, 'secret_key': secret_key}
       Otherwise raise some exception with text that this method not allowed

Hints:
    1. For sending requests you can use httpbin.org (remote or local) endpoint /anything
    2. For local httpbin.org you could use docker containers
        a. In terminal go to lesson_6 directory
        b. execute: docker-compose up
        c. server will available on http://127.0.0.1:8000
"""
