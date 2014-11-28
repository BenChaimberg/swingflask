Design Specification
====================
The Swing Paints website revamp will create a dynamic website with the criteria listed in the [Functional Specification](https://github.com/Youppi3/flaskexample/blob/master/docs/FS.md#functional-specification). This document will outline the following inner workings of the website with the new Python-based Flask back end:
* [Server software and overall architecture](#server-software-and-overall-architecture)
* [Server side programming language](#server-side-programming-language)
* [Client side programming language](#client-side-programming-language)
* [Data storage requirements and tool choices](#data-storage-requirements-and-tool-choices)
* [Server system architecture](#server-system-architecture)
* [Client system architecture](#client-system-architecture)
* [Product page creation](#product-page-creation)
* [Category page creation](#category-page-creation)
* [Software test strategy](#software-test-strategy)
* [Bug tracking strategy](#bug-tracking-strategy)
* [Software deployment instructions](#software-deployment-instructions)

Server Software and Overall Architecture
----------------------------------------
Development software will run locally on a virtual environment, and publically through a app hosting service, using Gunicorn and venv. Deployment software is to be determined by the employer, but will most likely be run on a *nix server using WSGI to handle the Flask app.

Server Side Programming Language
--------------------------------
Any server side scripting will be written in Python using Flask and its dependencies, notably Jinja. HTML and CSS will obviously be heavily used.

Client Side Programming Language
--------------------------------
Any client side scripting will be written in Javascript enhanced by jQuery. CSS will also be dynamically adjusted.

Data Storage Requirements and Tool Choices
------------------------------------------
Data storage at this time will only be static, but could be tweaked to allow for user input as well. Until that change has been made, data will be stored in readable Python dictionaries. Examples of such are [producttitle.py](https://github.com/Youppi3/flaskexample/blob/master/static/producttitle.py) and [categoryproducts.py](https://github.com/Youppi3/flaskexample/blob/master/static/categoryproducts.py).

Server System Architecture
--------------------------
The server will utilize (most likely) a WSGI wrapper of a Flask-enhanced Python app, with Jinja template dependencies and static files in child folders. A vitrualenv will be created with the latest versions of Python, Flask, and its dependencies, and the server will reroute itself through this vitrual environment.

Client System Architecture
--------------------------
On the client side, a fluid blend of HTML, CSS, and Javascript + jQuery will produce a wonderful example of fung shui in byte form. Dynamic elements will respond to the browser, OS, screen size etc. while also providing for a mobile-optimized web experience.

Product Page Creation
---------------------
Each product page will be created off of its product ID, generally a four digit number, which is also the URL [http://www.swingpaints.com/product/####](##). In addition to the static elements, the product's category will be found and printed, as well as its image, general description, directions, more information, demonstration, and buying options. This information will be found in Python dictionaries, see more above. Data in dictionaries will be kept in a minimal fashion, so the exterior structure elements will be produced automatically while displaying.

Category Page Creation
----------------------
As with the above, each category page will be created from its category ID, a string, which is pulled from the URL [(http://www.swingpaints.com/category/&lt;string&gt;)](##). Once again, in addition to the static elements, the category page will pull its correct image, its products and their respective products, and possibly a brief descriptions of the products to be found within.

Software Test Strategy
----------------------
A URL will be given to some choice few known for their aptitude in breaking technology with the hopes that if bugs are to be found, they will be attracted to the use of these "tech wrecks." Flask will handle all server-side testing with its built-in capability for such. Obviously, no code will be deployed in an unfinished state or one of undeterminable stability.

Bug Tracking Strategy
---------------------
All code will be hosted on the Github public repository, with any sensitive data, if existent, purged and added to the .gitignore before upload. Users may submit comments and suggestions through the issues and code through the pull requests. All client data will be carefully considered and inspected before acceptance or rejection.

Software Deployment Instructions
--------------------------------
The following must be completed before code is made live:

1. The code is tested in full, and runs with no errors, warnings, or issues.
2. A tarball will be created from the code to be pushed (.tar.gz file compressed from the entire folder of code, excluding system requirements such as WSGI).
3. Create a new release on Github, tagged and semantically versioned, and upload the tarball to the release.
4. Copy the URL of the distribution binary file.
5. SSH into the server and navigate to the server document root.
6. Download the release using the noted URL: ```$ wget <URL>```
7. Expand the downloaded binary: ```$ tar -xvf <filename>```
8. Replace the old folder with the new folder: ```$ mv <newfolder> <oldfolder>```
