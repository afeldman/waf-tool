#!/usr/bin/env python
# encoding: utf-8
# Anton Feldmann: anton.feldmann(at)gmail.com
# Anton Feldmann 2017

import os
from os.path import basename, dirname, splitext


from waflib           import Utils
from waflib.Configure import conf
from waflib.Task      import Task, update_outputs
from waflib.TaskGen   import extensions, features, taskgen_method

def configure(conf):
    conf.find_ghc()
    conf.find_ghc_pkg()

@conf
def find_ghc(self):
    self.find_program ('ghc', VAR='GHC')
    self.find_program ('ghc-pkg', VAR='GHC-PKG')

@conf
def find_ghc_pkg(self):
    if not hasattr(self, 'ghc_pkg'):
        self.ghc_pkg = 'base'

    self.ghc_pkg = Utils.to_list(self.ghc_pkg)
        

    installed_pkg = get_packages(self)
    l_ghc_pkg = [x.lower().strip() for x in self.ghc_pkg];
    
    for pkg in installed_pkg:
        self.msg('Chacking for %s' % pkg)
        try:
            l_ghc_pkg.index(pkg)
            self.msg("package %s found" % pkg, 'GREEN')

            self.env.append_unique('LINKFLAGS_'+)
            
        except:
            self.fatal("package %s not found" % pkg)

def get_packages(self):

    list_str = self.cmd_and_log(self.env.GHC-PKG + ['list'])
    ret=list()

    for line in list_str.split('\n').strip().lower():
        if line.startswith('/'):
            continue
        line = line[:line.rindex('-')]
        ret.append(line)

    return ret
