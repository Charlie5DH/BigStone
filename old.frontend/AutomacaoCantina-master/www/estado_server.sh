#!/bin/bash

ps -ef | grep controleCantina | grep -v grep | awk 'END { if (NR > 0) print "Servidor  ativo desde " $5 ; else print "Servidor inativo!" }'
