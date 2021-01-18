# smtptest.py

Simple script to test sending messages through smtp servers.
Relies on python's standard lib only.


```
usage: smtptest.py [-h] [-u USERNAME] [-p PASSWORD | -P | -r PASSWORD_FILE] [--port PORT] [--ssl | --starttls | --plaintext] [-q] [-v] server fromaddr to

positional arguments:
  server
  fromaddr
  to

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username for smtp auth (default: None)
  -p PASSWORD, --password PASSWORD
                        Password for smtp auth (default: None)
  -P, --prompt-password
                        Prompt password for smtp auth (default: False)
  -r PASSWORD_FILE, --password-file PASSWORD_FILE
                        Read smtp auth password from first line of file (default: None)
  --port PORT           TCP port to connect to (default: 25)
  --ssl                 enable SSL/TLS wrapped SMTP -- automatically enabled on port 465 (default: False)
  --starttls            enable STARTTLS SMTP -- automatically enabled on port 587 (default: False)
  --plaintext           Force plaintext (default: False)
  -q, --quiet           Quiet (default: False)
  -v, --verbose         Verbose mode (use multiple time to increase verbosity) (default: 0)
```

# Examples

```
# Without authentication
./smtptest.py localhost from@something to@somethingelse

# STARTTLS over port 587 with authentication
./smtptest.py --port 587 -u username -P localhost from@something to@somethingelse

# SSL over port 465 with authentication
./smtptest.py --port 465 -u username -P localhost from@something to@somethingelse
```
