#!/bin/bash

ARQ=lista_matriculas.csv
BASE=1000000
FORM=ean13
#FORM=upca

while IFS=";" read NOME MATR ; do
  
  if [ "$MATR" != "" ] ; then
    echo "Gerando codigo de barras para \"$NOME\""
    mat=$(expr $MATR + $BASE)
    pybarcode2 create $mat TESTE_"$MATR"_"$FORM" -b $FORM -t jpeg
  else
    echo "ERRO!! Nao existe matricula para $NOME"
  fi

done < $ARQ


