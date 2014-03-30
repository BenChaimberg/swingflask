Design Specification
====================
The Swing Paints website revamp will create a dynamic website with the criteria listed in the [Functional Specification](https://github.com/Youppi3/flaskexample/blob/master/docs/FS.md#functional-specification). This document will outline the following inner workings of the website with the new Python-based Flask back end:
* [Server software and overall architecture](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#server-software-and-overall-architecture).
* [Server side programming language](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#server-side-programming-language).
* [Client side programming language](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#client-side-programming-language).
* [Data storage requirements and tool choices](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#data-storage-requirements-and-tool-choices).
* [Server system architecture](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#server-system-architecture).
* [Client system architecture](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#client-system-architecure).
* [Major entry points (URLs) to the site](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#marjor-entry-points--urls--to-the-site).
* [Software test strategy](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#software-test-strategy).
* [Bug tracking strategy](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#bug-tracking-strategy).
* [Software deployment instructions](https://github.com/Youppi3/flaskexample/edit/master/docs/DS.md#software-deployment-instructions).

Server Software and Overall Architecture
----------------------------------------
Development software will run locally on a virtual environment, and publically through a app hosting service, using Gunicorn and venv. Deployment software is to be determined by the employer, but will most likely be run on a *nix server using wsgi to handle the Flask app.

Server Side Programming Language
--------------------------------
Any server side scripting will be written in Python using Flask and its dependencies, notably Jinja. HTML and CSS will obviously be heavily used.

Client Side Programming Language
--------------------------------
Any client side scripting will be written in Javascript enhanced by jQuery. CSS will also be dynamically adjusted.

Data Storage Requirements and Tool Choices
------------------------------------------
Data storage at this time will only be static, but could be tweaked to allow for user input as well. Until that change has been made, data will be stored in readable Python dictionaries. Examples of such are [producttitle.py](https://github.com/Youppi3/flaskexample/blob/master/static/producttitle.py) and [categoryproducts.py](https://github.com/Youppi3/flaskexample/blob/master/static/categoryproducts.py).

