
# Hydrogrid Evaluation - Fabio Galvagni




## Software Architect Task A - URL Shortener

### Overview

The entire software has been packaged in form of docker containers. In order for the containers to run, the following requirements must be met:
* The host machine must be Intel-based (**x86-64**) - _the containers won't run on a new M1-powered Apple Mac!_.
* The ports **8080** (web server) and **1433** (sql server) must be available on the host machine.
* A running [Docker Desktop](https://www.docker.com/products/docker-desktop) instance on the host machine is needed.

The solution must be started by **Docker Compose**. Docker-Compose builds and run two docker containers, and connects them to each other and to the host machine by a virtual network:
* **hydrogrid_db**: the container running the database instance (Microsoft SQL Server). The database data files are persisted in the host machine.
* **hydrogrid_urlshrtn**: the container hosting the python-based webserver software and a conda instance to run it

**!! PLEASE WAIT AT LEAST 5 minutes after having issued docker-composed, till the system is up and running!! The database needs time in order to get started and populated by the initialization script (init_db.sql).**


### Installation

Download from GitHub the the entire git repository:

`git clone https://github.com/fbglv/Hydrogrid.git`

Once in the repository root directory, run `docker-compose` in order to build and run the containers:

`docker-compose -p hydrogrid -f docker-compose.yml up`

The build phase takes several minutes.

> Note: during the building phase of the **hydrogrid_urlshrtn** container, an installation of **miniconda** is automatically downloaded and installed. However, the download of the Miniconda installer might fail due to network issues at the Miniconda website, breaking down in turn the container build phase. In this case, restart the docker-compose build by simply issuing: `docker-compose -p hydrogrid -f docker-compose.yml up --build`

To check if the containers are running:

`docker ps`

which should give an output similar to the follwing one:

```
CONTAINER ID   IMAGE                COMMAND                  CREATED        STATUS       PORTS                    NAMES
20be98116e2f   hydrogrid_urlshrtn   "conda run --no-capt…"   16 hours ago   Up 3 hours   0.0.0.0:8080->8080/tcp   hydrogrid_urlshrtn
dc119b7e8449   hydrogrid_db         "/bin/bash entrypoin…"   17 hours ago   Up 3 hours   0.0.0.0:1433->1433/tcp   hydrogrid_db
```

### Executing the URL Shortener

The URL Shortener is composed by a set of HTTP GET REST APIs. Once both the **hydrogrid_urlshrtn** and **hydrogrid_db** containers are running, the APIs can be accessed by any web browser or an utility such as curl, as specified in the requirements.

#### Adding an URL (generating a shortened URL)

The general format for getting a shortened URL is the following one:

`http://127.0.0.1:8080/addurlshrtn/<url_protocol>/<url_domain>/<expiration_days>`

whereas:
* `url_protocol` is the protocol section of the url (e.g. **https** if the complete url is https://www.derstandard.at)
* `url_domain` is the domain section of the url (e.g. **www.derstandard.at** in the previous example)
* `expiration_days` is the number of days starting from the current time in which the shortened url is active and cannot be used to redirect a request to the target website. _Note_: it can also be a _negative_ value (e.g. -2) - in this case the shortened url will be registered as already inactive.

For instance calling:

http://127.0.0.1:8080/addurlshrtn/https/www.derstandard.at/2

returns a similar response in JSON format:

```
{"status":"OK","url_shrtn":"http://127.0.0.1:8080/teleport/8056679214864864256","url_shrtn_code":"8056679214864864256"}
```

from which the shortened url (_http://127.0.0.1:8080/teleport/8056679214864864256_) can be taken.

#### Redirect

The shortened URL can be used to be automatically redirected to the target website. The format is the following:

`http://127.0.0.1:8080/teleport/<shortened_url_code>`

The shortened url of the previous example (`http://127.0.0.1:8080/teleport/963194304595476578`), for instance, automatically redirects the user to the `https://www.derstandard.at` website.

If the redirected url is expired, the user simply receives a JSON response with a `ERROR_URL_NOT_ACTIVE` status code:

```
{"status":"ERROR_URL_NOT_ACTIVE"}
```

If the shortened url contains an invalid code, the user receives a `ERROR_URLSHRTN_NOT_FOUND` status code:

```
{"status":"ERROR_NO_URLSHRTN_STORED"}
```

#### Removing a shortened URL

Shortened URLs can be removed anytime by invoking the **delurlshrtn** API:

`http://127.0.0.1:8080/delurlshrtn/<shortened_url_code>`

The user receives then a JSON response similar to the following one:

```
{"active":"True","status":"OK_DELETED","url_shrtn_code":"2641603234708071700"}
```

However, if the provided shortened url code corresponds to an already inactive entry, the user receives a `OK_URLSHRTN_ALREADY_INACTIVE` error code:

```
{"active":"False","status":"OK_URLSHRTN_ALREADY_INACTIVE","url_shrtn_code":"2675854229534319119"}
```

If the provided shortened url code is not valid, the user receives a `ERROR_URLSHRTN_NOT_FOUND` error code:

```
{"status":"ERROR_URLSHRTN_NOT_FOUND","url_shrtn_code":"2641603234708071700"}
```


#### Accessing an already shortened URL

An already shortened URL can be accessed anytime by means of the shortened url code received while creating a new shortened url:

`http://127.0.0.1:8080/geturlshrtn/<shortened_url_code>`

the user receives then a JSON response similar to the following one:

```
{"active":true,"expiration_time":"2021-02-02 16:41:25","status":"OK","url_original":"https://www.diewelt.de","url_shortened":"http://127.0.0.1:8080/teleport/513961572761687307","url_shortened_code":"513961572761687307"}
```

However, if the shortened url is not active, an `ERROR_URL_NOT_ACTIVE` error code is triggered:

```
{"status":"ERROR_URL_NOT_ACTIVE"}
```

If the provided shortened url code is wrong (non existing), an `ERROR_NO_URL_STORED` error code is generated:

```
{"status":"ERROR_NO_URL_STORED"}
```


#### Notes

the `db/test.sql` can be used to test and check the database structure and content.


## Software Architect Task B - Database Design for Settings

The task has been implemented in form of (populated) tables and and a view for the frontend. All database objects can be find in the `Hydrogrid` database of the `hydrogrid_db` MSSQL container instance, which can be accessed by **SQL Management Studio** using the following credentials:
* **Hostname**: `127.0.0.1`
* **Port**: `1433` (MSSQL standard)
* **Database**: `Hydrogrid`
* **Authentication Type**: SQL Credentials Authentication

The frontend can access directly the flat, denormalized (2NF) `Hydrogrid.dbo.Setting` database view.


