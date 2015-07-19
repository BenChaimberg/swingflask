Flask for Swing Paints
======================
Welcome to the revamping of the Swing Paints [website](http://www.swingpaints.com/), powered by [Flask](http://flask.pocoo.org/). The functional specification for this product can be found [here](https://github.com/Youppi3/swingflask/blob/master/docs/FS.md#functional-specification) and the design specification can be found [here](https://github.com/Youppi3/swingflask/blob/master/docs/DS.md#design-specification). A live version should be found [here](http://swingpaints.herokuapp.com/), but may not be up to date or functional at any point in time.

#### To run locally (NIX): ####
```
$ git clone https://github.com/Youppi3/swingflask.git
$ cd swingflask
$ sudo pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt
# If pip raises 'EnvironmentError: mysql_config not found':
# Install mysql and add it to your PATH:
# export PATH=$PATH:/usr/local/mysql/bin
(venv) $ python app.py
```
