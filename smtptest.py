#!/usr/bin/env python3

import argparse
import logging
import time
from getpass import getpass
from smtplib import SMTP, SMTP_SSL
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--username", help="Username for smtp auth")
    pwgroup = parser.add_mutually_exclusive_group()
    pwgroup.add_argument("-p", "--password", help="Password for smtp auth")
    pwgroup.add_argument(
        "-P", "--prompt-password", action="store_true", help="Prompt password for smtp auth"
    )
    pwgroup.add_argument("-r", "--password-file", help="Read smtp auth password from first line of file")

    parser.add_argument("--port", help="TCP port to connect to", type=int, default=25)
    cryptogroup = parser.add_mutually_exclusive_group()
    cryptogroup.add_argument(
        "--ssl",
        action="store_true",
        help="enable SSL/TLS wrapped SMTP -- automatically enabled on port 465",
    )
    cryptogroup.add_argument(
        "--starttls",
        action="store_true",
        help="enable STARTTLS SMTP -- automatically enabled on port 587",
    )
    cryptogroup.add_argument("--plaintext", action="store_true", help="Force plaintext")

    parser.add_argument("-q", "--quiet", help="Quiet", action="store_true")
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose mode (use multiple time to increase verbosity)",
        action="count",
        default=0,
    )

    parser.add_argument("server")
    parser.add_argument("fromaddr")
    parser.add_argument("to")
    args = parser.parse_args()

    args.verbose = args.verbose if args.verbose <= 2 else 2
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format=("%(asctime)s.%(msecs)03d %(name)15s[%(levelname)s] %(message)s"),
        level=logging.WARNING if args.quiet else logging.INFO,
    )

    pw = None
    if args.password:
        pw = args.password
    elif args.prompt_password:
        pw = getpass("SMTP password: ")
    elif args.password_file:
        with open(args.password_file) as f:
            pw = f.readline().strip()

    if pw and not args.username:
        logging.warning("Password set but no username?")

    msg = (
        f"From: <{args.fromaddr}>\n"
        f"To: <{args.to}>\n"
        f"Subject: Test email from smtptest - {datetime.now(tz=timezone.utc)}\n"  # noqa: E501
        "\n"
        f"testing 1 2 check\n"
    )

    # Turn on ssl/starttls based on port unless we're doing crazy tests
    if args.port == 587 and not (args.ssl or args.starttls or args.plaintext):
        args.starttls = True
    if args.port == 465 and not (args.ssl or args.starttls or args.plaintext):
        args.ssl = True

    _SMTP = SMTP_SSL if args.ssl else SMTP
    with _SMTP(args.server, port=args.port) as smtp:
        logging.info(
            "Sending message from:%s to:%s via %s:%d", args.fromaddr, args.to, args.server, args.port
        )
        smtp.set_debuglevel(args.verbose)
        if args.starttls:
            smtp.starttls()

        if pw:
            if not (args.ssl or args.starttls):
                logging.warning(
                    "!!! About to send plaintext credentials over the wire. ctrl-c to abort !!!"
                )
                time.sleep(5)
                logging.warning("Too late")
            smtp.login(args.username, pw)
        smtp.sendmail(args.fromaddr, args.to, msg)
        logging.info("Message sent")


if __name__ == "__main__":
    main()
