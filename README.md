# Eve

*A async backend scaffold based on FastAPI.*

> If your project is front-end and back-end separated, or if it is solely a back-end providing external interfaces, then I recommend you to use an asynchronous scaffolding: *[viper](https://github.com/sungeer/viper)*.

> The reason I prefer to recommend the Starlette framework is that while FastAPI is built on Starlette, Pydantic, and Swagger, the design of Python type hints is quite cumbersome to use. Additionally, the APIs of Pydantic and SQLAlchemy are constantly changing, making them very unstable. Moreover, the maintenance of asynchronous database drivers, such as aiomysql, is quite concerning. The issue of disconnecting database connections has not been resolved for a long time, which can lead to millions of abnormal warning records being written to the MySQL server...
As for the inheritance of Swagger documentation, this is actually a matter of development philosophy: whether to prioritize design or development. I lean more towards customizing design documentation, so the integration of Swagger is mainly to appease front-end developers. Usually, I personally handle the coordination between front-end and back-end during joint debugging.
Therefore, I need a more purely asynchronous project based on the Starlette framework. For MySQL database operations, I opt for the synchronous mysqlclient and place synchronous operations in a thread pool to avoid blocking the event loop. For the scheduling of distributed task systems, I choose SAQ. If it's synchronous distributed task scheduling, I prefer Huey, which is more user-friendly for humans.

## Installation

clone:
```
$ git clone https://github.com/sungeer/eve.git
$ cd eve
```
create & activate virtual env then install dependency:

with venv + pip:
```
$ python -m venv venv
$ source venv/bin/activate  # use `venv\Scripts\activate` on Windows
$ pip install -r requirements.txt
```

run:
```
$ granian --interface wsgi eve:app
* Running on http://127.0.0.1:8000/
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
