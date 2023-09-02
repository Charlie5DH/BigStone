<!DOCTYPE HTML>
<html xmlns="http://www.w3.org/1999/xhtml">
<div w3-include-html="head.html"></div>

<head>
<?php
session_start();
if((!isset ($_SESSION['login']) == true) and (!isset ($_SESSION['senha']) == true))
{
        unset($_SESSION['login']);
        unset($_SESSION['senha']);
        header('location:index.php'); // feito
        echo"<script language='javascript' type='text/javascript'>;window.location.href='index.php';</script>";
        }

$logado = $_SESSION['login'];
?>

        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
	<title>Cantina do Dindo</title>
       <style type="text/css">
                @page { size: 20.55cm 28.19cm; margin-left: 0.72cm; margin-top: 1.52cm }
                p { margin-bottom: 0.25cm; line-height: 115% }
                a:link { so-language: zxx }
        </style>

    </head>
<body lang="pt-BR" dir="ltr">


<?php
  include('db_connect.php');


	  $query = "SELECT `cliente_nome`, `cliente_matricula` FROM `Clientes` WHERE 1";
	  $resultado = mysqli_query($conexao,$query);

	  $arquivo = '/tmp/lista_matriculas.csv';
	  unlink($arquivo);
	  $abrir = fopen($arquivo, 'a');

	  $top_ini = 1.52;
	  $left_ini = 0.72;
	  $passo_width = 6.61 + 0.20;
	  $passo_height = 3.81+0.18;

	  $top = $top_ini;
	  $left = $left_ini;

	  $COLS = 3;
	  $ROWS = 7;
	  $cols = $COLS;
	  $rows = $ROWS;
	  $frame = 1;
	  while ($linha = mysqli_fetch_array($resultado)) {
		 echo "<div id=\"Frame".$frame."\" dir=\"ltr\" style=\"position: absolute; top: ".$top."cm; left: ".$left."cm; width: 6.61cm; height: 3.81cm; border: none; padding: 0cm; background: #ffffff\">";
		 echo "<p style=\"margin-bottom: 0cm; line-height: 100%\">";
		 echo "<font size=\"3\">";
		 echo "<center>";
		 echo "<b>" . reduzirNome($linha['cliente_nome'],20) ."</b><br />";
		 echo "</font>";
		 echo "<font size=\"2\">";
		 echo "Matricula: " . $linha['cliente_matricula']   ."<br />";
		 echo "</font><br />";
		 echo "<img src='codigo_barras/M_".$linha['cliente_matricula']."_ean8.jpeg'  width='200' height='70'>";
		 echo "</center>";
		 echo "</p> </div>";
		 $frame = $frame + 1;

		$cols = $cols - 1;
		 if ($cols == 0) {
			$top = $top + $passo_height;
			$left = $left_ini;
			$cols = $COLS;

			$rows = $rows - 1;
			if ($rows == 0) {
				#echo "Nova pagina";
				$rows = $ROWS;
				$top = $top + 1.52 + 0.25 + 0.58;
			}
		 }
		 else {

			 $left = $left + $passo_width;
		 }

		 fwrite($abrir, $linha['cliente_nome'] . ";" . $linha['cliente_matricula'] . "\n");
	  } 
	  fclose($abrir);

function reduzirNome( $texto, $tamanho )
{
// Se o nome for maior que o permitido
if( strlen( $texto ) > ( $tamanho - 2 ) )
        {
            $texto = strip_tags( $texto );

            // Pego o primeiro nome
            $palavas    = explode( ' ', $texto );
            $nome       = $palavas[0];

            // Pego o ultimo nome
            $palavas    = explode( ' ', $texto );
            $sobrenome  = trim( $palavas[count( $palavas ) - 1]);

            // Vejo qual e a posicao do ultimo nome
            $ult_posicao= count( $palavas ) - 1;

            // Crio uma variavel para receber os nomes do meio abreviados
            $meio = '';

            // Listo todos os nomes do meios e abrevio eles
            for( $a = 1; $a < $ult_posicao; $a++ ):

                // Enquanto o tamanho do nome nao atingir o limite de caracteres
                // completo com o nomes do meio abreviado
                if( strlen( $nome.' '.$meio.' '.$sobrenome )<=$tamanho ):
                    $meio .= ' '.strtoupper( substr( $palavas[$a], 0,1 ) );
                endif;
            endfor;

        }else{
           $nome       = $texto;
           $meio       = '';
           $sobrenome  = '';
        }

        return trim( $nome.$meio.' '.$sobrenome );
    }
          ?>
    </body>

</html>  
