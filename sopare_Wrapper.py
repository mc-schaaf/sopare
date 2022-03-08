#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import sopare.recorder as recorder
import sopare.controller as controller
from sopare.version import __version__


if __name__ == "__main__":
    print ("sopare "+__version__)

    c = controller.Controller(sys.argv[1:])
    cfg = c.create_config()

    if c.recreate:
        c.recreate_dict(cfg)
        sys.exit(0)

    if c.unit:
        c.unit_tests(cfg)
        sys.exit(0)

    recorder.recorder(cfg)
