# Space Asset Store

## Description

This is a simple REST API to allow the cataloging of satellites and antennas. They must fall in to certain types and classes to be considered valid.

Satellites: dove, rapideye, or skysat
Antennas: dish or yagi

Endpoints:
```
List of all assets -> GET /api/v1/assets/
Individual asset -> GET /api/v1/assets/<name>
Create asset -> POST /api/v1/assets/ json example: {"asset_class":"dove", "asset_type":"satellite", "name":"sat_name"}
```

Names are only valid if they are between 4 and 64 characters long inclusive, globally unique, contain only alphanumeric characters plus '-' and '\_', and they cannot start with '-' or '\_'.

Assets cannot be created or deleted.

## Setup

To run the express setup it is assumed you are on a MacBook Pro with python 3.8.5 installed, with python scripts being ran with 'python'. I've tested on multiple setups and it works, so hopefully it's not a case of "works on my machine".

To setup the app and database and begin running locally run the following

```
source ./setup.sh
```

To run the flask app afterward at any point run the following (will need to also reactivate your virtual env and reset FLASK_APP var if you close the terminal)

```
flask run
```

## Considerations and Compromises

* Setting up Flask with sqlalchemy as an ORM and alembic to run migrations was fun, but basically every file except the /alembic directory had to be created from scratch, which took longer than expected. Using something overpowered like Django for this simple app would have saved time, although not been as fun as doing it all from scratch.

* The database schema played a big role in this app. While my current solution allows a lot more satellites/antennas/something new to be added easily, it is overkill for the current iteration. An easier method would be to not worry about normalizing the data and just store the class and type in the asset table and then just add validations before saving the data, such as to check if "asset class in valid types for class". This would require manual work, but with 5 total classes this would be trivial. This would simplify the schema and calls for create and get from the database.

* Using SQLite. I hadn't used SQLite in a project but I've randomly heard some cool use cases for it lately, such as https://github.com/simonw/datasette, so I thought I'd test it out, plus it made it extremely easy to download and run since it has no external dependencies. However there was a little learning curve on basic things, such as the sqlite3 command line tool and connecting to alembic/sqlalchemy, so it added some time. I'm used to Postgres.

* No CI/CD, deployment on the cloud, OpenAPI spec, branching, etc. due to trying to time box this app and keeping things simple.

* Data structure for the API is basic. In a more developed app it should include things like asset count, pagination, etc.
