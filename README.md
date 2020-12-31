Flask for Swing Paints
======================
Welcome to the revamping of the Swing Paints [website](http://www.swingpaints.com/), powered by [Flask](http://flask.pocoo.org/). The functional specification for this product can be found [here](https://github.com/BenChaimberg/swingflask/blob/master/docs/FS.md#functional-specification) and the design specification can be found [here](https://github.com/BenChaimberg/swingflask/blob/master/docs/DS.md#design-specification).

#### To run locally (NIX): ####
```
# Install mysql and add it to your PATH:
$ export PATH=$PATH:/usr/local/mysql/bin
$ export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/usr/local/mysql/lib

# Download the source code
$ git clone https://github.com/BenChaimberg/swingflask.git
$ cd swingflask

# Install a virtual environment to silo this project's dependencies. Add `--ignore-installed six` if you run into a "Cannot uninstall" error.
$ sudo -H pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate

# Install dependencies
(venv) $ pip install -r requirements.txt

# Create a self-signed certificate to enable SSL
# You may need to trust the certificate in order to skip browser warning screens (in macOS, this is through Keychain Access)
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -config cert.cnf

# Start the development server
(venv) $ FLASK_ENV=development flask run --cert cert.pem --key key.pem

# Go to https://localhost:5000 to see the site
```
