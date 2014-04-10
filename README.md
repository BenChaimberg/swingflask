Flask for Swing Paints
======================
Welcome to the revamping of the Swing Paints [website](http://www.swingpaints.com/), powered by [Flask](http://http://flask.pocoo.org/). The functional specification for this product can be found [here](https://github.com/Youppi3/flaskexample/blob/master/docs/FS.md#functional-specification) and the design specification can be found [here](https://github.com/Youppi3/flaskexample/blob/master/docs/DS.md#design-specification). A live version should be found [here](http://swingpaints.herokuapp.com/), but may not be up to date or functional at any point in time.

#### To fiddle locally (Mac): ####
```
$ git clone https://github.com/Youppi3/flaskexample.git
$ cd flaskexample
$ sudo easy_install virtualenv
$ virtualenv venv
$ . venv/bin/activate
$ pip install flask Flask-Mail Flask-WTF
$ python flaskexample.py
```
