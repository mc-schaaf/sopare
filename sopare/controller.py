#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import getopt
import sopare.config as config
import sopare.util as util
import sopare.log as log
import test.unit_tests as tests


class Controller:

    endless_loop = False
    debug = False
    outfile = None
    infile = None
    dict = None
    plot = False
    wave = False
    error = False
    cfg_ini = None
    recreate = False
    unit = False

    def __init__(self, argv):
        if len(argv) > 0:
            try:
                opts, args = getopt.getopt(argv, "ahelpv~cous:w:r:t:d:i:",
                                           ["analysis", "help", "error", "loop", "plot", "verbose", "wave", "create",
                                            "overview", "unit", "show=", "write=", "read=", "train=", "delete=", "ini="
                                            ])
            except getopt.GetoptError:
                self.usage()
                sys.exit(2)

            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    self.usage()
                    sys.exit(0)
                if opt in ("-e", "--error"):
                    self.error = True
                if opt in ("-l", "--loop"):
                    self.endless_loop = True
                if opt in ("-p", "--plot"):
                    if not self.endless_loop:
                        self.plot = True
                    else:
                        print("Plotting only works without loop option!")
                        sys.exit(0)
                if opt in ("-v", "--verbose"):
                    self.debug = True
                if opt in ("-~", "--wave"):
                    self.wave = True
                if opt in ("-c", "--create"):
                    self.recreate = True
                if opt in ("-o", "--overview"):
                    self.show_dict_ids()
                    sys.exit(0)
                if opt in ("-a", "--analysis"):
                    self.show_dict_analysis()
                    sys.exit(0)
                if opt in ("-s", "--show"):
                    self.show_word_entries(arg)
                    sys.exit(0)
                if opt in ("-w", "--write"):
                    self.outfile = arg
                if opt in ("-r", "--read"):
                    self.infile = arg
                if opt in ("-t", "--train"):
                    self.dict = arg
                if opt in ("-d", "--delete"):
                    self.delete_word(arg)
                    sys.exit(0)
                if opt in ("-i", "--ini"):
                    self.cfg_ini = arg
                if opt in ("-u", "--unit"):
                    self.unit = True

    def create_config(self):
        if self.cfg_ini is None:
            cfg = config.config()
        else:
            cfg = config.config(self.cfg_ini)
        logger = log.log(self.debug, self.error, cfg)
        cfg.addsection('cmdlopt')
        cfg.setoption('cmdlopt', 'endless_loop', str(self.endless_loop))
        cfg.setoption('cmdlopt', 'debug', str(self.debug))
        cfg.setoption('cmdlopt', 'plot', str(self.plot))
        cfg.setoption('cmdlopt', 'wave', str(self.wave))
        cfg.setoption('cmdlopt', 'outfile', self.outfile)
        cfg.setoption('cmdlopt', 'infile', self.infile)
        cfg.setoption('cmdlopt', 'dict', self.dict)
        cfg.addlogger(logger)
        return cfg

    def recreate_dict(self, cfg):
        print("recreating dictionary from raw input files...")
        utilities = util.util(self.debug, cfg.getfloatoption('characteristic', 'PEAK_FACTOR'))
        utilities.recreate_dict_from_raw_files()

    def delete_word(self, arg):
        if arg != "*":
            print("deleting " + arg + " from dictionary")
        else:
            print("deleting all entries from dictionary")
        utilities = util.util(self.debug, None)
        utilities.deletefromdict(arg)

    def show_word_entries(self, arg):
        print(arg + " entries in dictionary:")
        utilities = util.util(self.debug, None)
        utilities.showdictentry(arg)

    def show_dict_ids(self):
        print("current entries in dictionary:")
        utilities = util.util(self.debug, None)
        utilities.showdictentriesbyid()

    def show_dict_analysis(self):
        print("dictionary analysis:")
        utilities = util.util(self.debug, None)
        analysis = utilities.compile_analysis(utilities.getDICT())
        for analysis_id in analysis:
            print(analysis_id)
            for k, v in analysis[analysis_id].iteritems():
                print(' ' + str(k) + ' ' + str(v))

    def unit_tests(self, cfg):
        print("starting unit tests...")
        tests.unit_tests(self.debug, cfg)
        print("done.")

    def usage(self):
        print("usage:\n")
        print(" -h --help           : this help\n")
        print(" -l --loop           : loop forever\n")
        print(" -e --error          : redirect sdterr to error.log\n")
        print(" -p --plot           : plot results (only without loop option)\n")
        print(" -v --verbose        : enable verbose mode\n")
        print(" -~ --wave           : create *.wav files (token/tokenN.wav) for")
        print("                       each detected word\n")
        print(" -c --create         : create dict from raw input files\n")
        print(" -o --overview       : list all dict entries\n")
        print(" -s --show   [word]  : show detailed [word] entry information")
        print("                       '*' shows all entries!\n")
        print(" -w --write  [file]  : write raw to [dir/filename]\n")
        print(" -r --read   [file]  : read raw from [dir/filename]\n")
        print(" -t --train  [word]  : add raw data to raw dictionary file\n")
        print(" -d --delete [word]  : delete [word] from dictionary and exits.")
        print("                       '*' deletes everything!\n")
        print(" -i --ini    [file]  : use alternative configuration file\n")
        print(" -a --analysis       : show dictionary analysis and exits.\n")
        print(" -u --unit           : run unit tests\n")
