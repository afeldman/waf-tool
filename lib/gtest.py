#! /usr/bin/env python
# encoding: utf-8
# author: Anton Feldmann

'''

When using this tool, the wscript will look like:

        def configure(conf):
                conf.load('compiler_cxx gtest')

        def build(bld):
                bld(source='main.cpp', target='app', use='GTEST')

Options are generated, in order to specify the location of gtest includes/libraries.


'''

def configure(conf):
        conf.check_cfg(package='gtest', args=['--cflags', '--libs'], uselib_store='GTEST', mandatory=True)

