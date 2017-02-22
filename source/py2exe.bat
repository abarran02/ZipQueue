@echo off
set build=ZipQueue
title Building %build%.exe
CLS
py -3.4 -m py2exe.build_exe %build%.py