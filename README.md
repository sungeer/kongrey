# Eve

*A async backend scaffold based on FastAPI.*

> If your project is front-end and back-end separated, or if it is solely a back-end providing external interfaces, then I recommend you to use an asynchronous scaffolding: *[viper](https://github.com/sungeer/viper)*.

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
