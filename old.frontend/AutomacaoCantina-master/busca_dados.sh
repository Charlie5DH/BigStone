#!/bin/bash

processa (){ 

	INICIO=$2

	if [ "$INICIO" == "inicio" ] ; then
		echo "cliente_id,cliente_tipo,cliente_matricula,cliente_nome,cliente_familia,cliente_ano,cliente_pais_1,cliente_pais_2,cliente_email_1,cliente_email_2,cliente_telefone_1,cliente_telefone_2,cliente_telefone_3,cliente_telefone_4,cliente_telefone_5,cliente_telefone_6,cliente_telefone_7,cliente_telefone_8,cliente_telefone_9,cliente_data" > sai
	else
		rm -rf sai 2>/dev/null
	fi

	echo "Processando $1"

	cat $1  | awk -F\; '{ 
	   n=split($1,TUR,":")
	   if (n>1) {
		   split(TUR[2],T,"-")
		   turma = T[1]
	   }
	   if ($2 == "NOME DO ALUNO") next
	   if (length($2) > 2 ) {
		print "" 
	   }
	   else {
		n = split($1,EMAIL,"@")
		if (n > 1) {
			printf ";%s", $1
		}
		next
	   }
	   id += 1
	   cliente_id           = id
	   cliente_tipo         = "Aluno"
	   cliente_matricula    = $1
	   cliente_nome         = $2
	   cliente_familia      = $2
	   cliente_ano          = turma
	   cliente_pais_1       = ""
	   cliente_pais_2       = ""
	   printf cliente_id ";" cliente_tipo ";" cliente_matricula ";" cliente_nome ";" cliente_familia ";" cliente_ano ";" cliente_pais_1 ";" cliente_pais_2

	   # printf $1 ";" $2 ";" turma ";" email
	   #printf "%s;Aluno;%s;%s;%s;%s", id, $1, $2, $2, turma
	}' >>sai

	alunos=$(cat sai | wc -l)
	cat sai >> lista_alunos_2020.csv
	echo "$1 tem $alunos alunos"
	total=$(expr $total + $alunos)
	rm sai 2>/dev/null
}

total=0
rm lista_alunos_2020.csv 2>/dev/null
#processa educacao_infantil.csv
processa ensino_fundamental.csv "inicio"
processa ensino_medio.csv

echo "Total: $total alunos"


echo ""
echo "Analise do Clientes_atu.csv: Alunos que estão na lista recebida em 2020 e que não estao na Base do sistema"
echo "$(cat Clientes_atu.csv | wc -l) entradas"

insert=0
while IFS=";" read fID fTipo fMatr fNome fFamilia fTurma; do

	n=$(cat Clientes_atu.csv | grep $fMatr | wc -l)

	if [ $n -eq 0 ] ; then 
		echo "$fMatr $fNome $fTurma"
		insert=$(expr $insert + 1)
	fi

done < lista_alunos_2020.csv
echo "Serao inseridos $insert alunos"

exit

echo ""
echo "Analise paa REMOVER: Alunos que estao na Base do Sistema e que nao estao na lista recebida em 2020"
cat Clientes_atu.csv | awk -F\, '{ if ($5 == "\"Aluno\"") print $8 ";" $3 }' |  sed -e 's/\"//g' > lista_alunos_base.csv

remove=0
while IFS=";" read fMatr fNome; do

	if [ ${#fMatr} -lt 2 ] ; then
		echo "Aluno sem matricula: $fNome"
		continue
	fi
	n=$(cat lista_alunos_2020.csv | grep $fMatr | wc -l)

	if [ $n -eq 0 ] ; then 
		echo "$fMatr $fNome"
		remove=$(expr $remove + 1)
	fi

done < lista_alunos_base.csv
echo "Serao removidos $remove alunos"
