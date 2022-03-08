#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import sopare.recorder as recorder
import sopare.controller as controller
import time

if __name__ == "__main__":

    words = sys.argv[1:]

    words = ["rechts", "links"]

    print("\n"*10)
    print("We will now begin calibrating the system. Prepare to speak into the microphone.")
    print("Each training round will start with an instruction on the word to be displayed. After that, debug info " +
          "will rush by.")
    print("Speak after the line: \"INFO:sopare.recorder:start endless recording\"")

    for word in words:
        for i in range(15):
            print("The next word will be {}.".format(word))
            print("Starting in 3 seconds...")
            time.sleep(3)
            c = controller.Controller(["-v", "-t", word])
            cfg = c.create_config()

            if c.recreate:
                c.recreate_dict(cfg)
                sys.exit(0)

            if c.unit:
                c.unit_tests(cfg)
                sys.exit(0)

            recorder.recorder(cfg)
