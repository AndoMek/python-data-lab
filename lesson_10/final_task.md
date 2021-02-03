# Final Task

## Generate mock data and load into RDBMS
1. Generate data by using `Faker` framework:
    * `customer_id`: unique value, Sequence started from 1. (bigint)
    * `first_name`: Customer first name. Non-empty. (string)
    * `last_name`: Customer first name. Non-empty. (string)
    * `date_of_birth`: Date of birth. Could be empty, 10-20% of empty. (string)
    * `email`: Customer email. Non-empty (string)
    * `last_login_dt`: Last login datetime. Could be empty, 5-15% of empty. (datetime)
    * `last_login_ip`: Last login IPv4. Could be empty if `last_login_dt` is empty than also empty (string)
    * `country_origin`: Customer's country of origin. Could be empty, 10-20% of empty.
    * `home_country`: Customer home country. Non-empty. (string)
    * `home_city`: Customer home city. Non-empty. (string)
    * `home_street`: Customer home street. Non-empty. (string)
    * `home_building_number`: Customer home street. Non-empty. (string)
    * `work_country`: Customer work country. Non-empty. (string)
    * `work_city`: Customer work city. Non-empty. (string)
    * `work_street`: Customer work street. Non-empty. (string)
    * `work_building_number`: Customer work street. Non-empty. (string)
    * `mobile_phone`: Customer phone could be empty, 5-15% of empty. (string)
    * `home_phone`: Customer landline phone could be empty, 50-65% of empty. (string)
    * `work_phone`: Customer work could be empty, 20-25% of empty. (string)
2. Load data into any RDBMS to table customers minimum 10000 records. Recommends to use docker container of PostgreSQL from lesson-9.
   Data could load by any way (not only from SQLAlchemy or psycopg2)
3. Provide source code of data generator


## Create Mock application which provide Rest-API
1. Use `flask-restx`, `flask-restful`, `flask-restplus` or any other framework for create RESTfull API
2. Create endpoints:
    * __/customers__ `POST`: return JSON which contain an array of customers objects from RDMS table `customers`.
      Datetime format "YYYY-MM-DD HH24:MI:SS.sss", Date format: "YYYY-MM-DD". Arguments:
        * `previous_id`: start return data which greater than this id. Mandatory
        * `records`: maximum returned values. Optional, default value 100. If less than 1 and greater than 1000 than return 400 error
    * __/customer/<customer_id:integer>__ `GET`: Return single customer information from RDMS table `customers`. If not exists than return 404 error.
3. All endpoints are private and should auth for some keys in the header, like "X-CUTSOM-AUTH"
4. Dockerized application. Application Arguments:
    * `connection_url`: RDBMS connection url-string. Positional. Mandatory.
5. Provide source code of application


## Create script which read data from Rest-API
1. Read all data from Rest-API's endpoint __/customers__
2. Save data to CSV file
3. Provide source code of script


## Additional
1. You can work in teams however it is not mandatory
2. You can increase difficulty if you want just ask Andrey Anshin of additional requirements
