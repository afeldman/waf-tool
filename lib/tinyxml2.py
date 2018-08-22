#! /usr/bin/env python
# encoding: utf-8
# author: Anton Feldmann


'''

When using this tool, the wscript will look like:

        def configure(conf):
                conf.load('compiler_cxx tinyxml2')

Options are generated, in order to specify the location of tinyxml2 includes/libraries.


'''

def options(opt):
    opt.load('compiler_cxx')


def configure(conf):
    conf.load('compiler_cxx')

    conf.check_cfg(package='tinyxml2')
