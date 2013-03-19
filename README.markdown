simpleserial
============

A simple serial connection handler written in Python.

Dependencies
------------
 * Python 2.7
 * pyserial (http://pyserial.sourceforge.net/):
   * Install with `pip install pyserial`

Usage
-----

``` bash
./simpleserial.py
```

Examples
--------

Power On a Sharp Aquos TV:

``` bash
./simpleserial.py -i /dev/tty.KeySerial1 -r 9600 -d 8 -s 1 -p None -f off -a off -m "POWR1   "
```

Power Off a Sharp Aquos TV:

``` bash
./simpleserial.py -i /dev/tty.KeySerial1 -r 9600 -d 8 -s 1 -p None -f off -a off -m "POWR0   "
```
