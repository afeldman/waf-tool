#! /usr/bin/env python
# encoding: utf-8
# author: Anton Feldmann

'''

When using this tool, the wscript will look like:

        def configure(conf):
                conf.load('compiler_cxx gmock')

        def build(bld):
                bld(source='main.cpp', target='app', use='GMOCK')

Options are generated, in order to specify the location of gmock includes/libraries.


'''

def configure(conf):
        conf.check_cfg(package='gmock', args=['--cflags', '--libs'], uselib_store='GMOCK', mandatory=True)

