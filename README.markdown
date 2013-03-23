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

Run interactively:

``` bash
./simpleserial.py
```

### Non-interactively send messages

#### Examples

Power On a Sharp Aquos TV:

``` bash
./simpleserial.py -i /dev/tty.KeySerial1 -r 9600 -d 8 -s 1 -p None -c off -a off -m "POWR1   "
```

Power Off a Sharp Aquos TV:

``` bash
./simpleserial.py -i /dev/tty.KeySerial1 -r 9600 -d 8 -s 1 -p None -c off -a off -m "POWR0   "
```

### Read messages from a file

`simpleserial.py` will happily read a series of messages from a file for you. This can be useful in scripting
a series of commands that needs to be sent to a device, for example. The file should be comma-delimited with
the message in the first column, and the number of expected bytes in the response (if any) in the second column:

```
POWR1   ,3
POWR0   ,4
VOLM42  ,5
```
Note: Columns don't have to line up -- in my example, whitespace is required in the message string because
the receiving device (a Sharp Aquos TV) expects a total of 8-bytes in each message, otherwise it returns a 3-byte
response of "ERR". In other words, this is perfectly okay as well if your device supports it:

```
HELLOTHERE,10
I,1
GET,3
ECHOED,6
BACK,4
BY,2
THE,3
REMOTE,6
DEVICE,6
SO,2
I,1
EXPECT,6
THE,3
EXACT,5
SAME,4
NUMBER,6
OF,2
BYTES,5
THAT,4
I,1
SEND,4
PER,3
MESSAGE,7
```

Once a file is ready, we can just pass the filename to `simpleserial.py` and it will iterate through each message and send it.
Note that it does this in a single serial connection, and closes the connection after the last message is sent and a response is
received.

``` bash
./simpleserial.py -i /dev/tty.KeySerial1 -r 9600 -d 8 -s 1 -p None -c off -a off -f myfile.txt
```
