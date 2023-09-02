#!/bin/bash

ps -ef | grep controleCantina | grep -v grep | awk '{ print "kill -9 " $2 "; "}'| sh
