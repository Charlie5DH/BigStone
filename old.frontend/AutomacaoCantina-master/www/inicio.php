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
        <title>Cantina do Dindo - Almo&ccedil;o</title>
        <style type="text/css">
            *{ /*Formata todos os elementos da página*/
                padding:0px; /*espaço entre a borda e o conteúdo do elemento*/
                margin:0px; /*espaço entre a borda e os elementos externos*/
            }
            #topo{
                width: 100%; /*largura*/
                height: 80px; /*altura*/
                text-align: center; /*alinhamento do texto*/
                clear: both; /*não permite elementos flutuantes ao lado*/
                background-color: #ffffff; /*cor de fundo*/
            }
            #menu{
                height: 30px; /*altura*/
                text-align: center; /*alinhamento do texto*/
                padding: 10px; /*espaço entre a borda e o conteúdo do elemento*/
                background-color: #ffc000; /*cor de fundo*/
            }
            #meio{
                width: 100%; /*largura*/
                background-color: #f90; /*cor de fundo*/
                height: 80%;; /*altura*/
            }
            #lateral{
                float:right; /*define que o elemento deve flutuar à direita*/
                background-color: #ffffff; /*cor de fundo*/
                padding: 2px; /*espaço entre a borda e o conteúdo do elemento*/
                width: 18% /*largura*/
            }
            #conteudo{
                padding: 10px; /*espaço entre a borda e o conteúdo do elemento*/
                width: 80%; /*largura*/
                float:left; /*define que o elemento deve flutuar à esquerda*/
                background-color: #ffffff; /*cor de fundo*/
            }
            #rodape{
                clear: both; /*não permite elementos flutuantes ao lado*/
                text-align: center; /*alinhamento do texto*/
                padding: 10px; /*espaço entre a borda e o conteúdo do elemento*/
                background-color: #ffffff; /*cor de fundo*/
            }
            #titulo{
                display: block;
                font-size: 2em;
                margin-top: 0.67em;
                margin-bottom: 0.67em;
                margin-left: 1em;
                margin-right: 0;
            }

            #texto_inicio{
                display: block;
                font-size: 1em;
                margin-top: 0.67em;
                margin-bottom: 5.67em;
                margin-left: 2em;
                margin-right: 0;
            }
            #operacao{
                display: block;
                font-size: 1em;
                margin-top: 0.67em;
                margin-bottom: 2.67em;
                margin-left: 2em;
                margin-right: 0;
            }
            #identificacao{
                display: block;
                font-size: 1em;
                margin-top: 0.2;
                margin-bottom: 0.2;
                margin-left: 1.2em;
                margin-right: 0;
            }
            #nome{
                display: block;
                font-size: 1em;
                margin-top: 0.2;
                margin-bottom: 0.2;
                margin-left: 1.2em;
                margin-right: 0;
            }
            #nome_inserido{
                display: block;
                font-size: 1em;
                margin-top: 0.2;
                margin-bottom: 0.2;
                margin-left: 1.2em;
                margin-right: 0;
            }
            #nome_manual{
                display: block;
                font-size: 1em;
                margin-top: 0.2;
                margin-bottom: 0.2;
                margin-left: 1.2em;
                margin-right: 0;
            }
            #valor{
                display: block;
                font-size: 1em;
                margin-top: 0.2;
                margin-bottom: 0.2;
                margin-left: 1.2em;
                margin-right: 0;
            }
            #peso{
                display: block;
                font-size: 1em;
                margin-top: 0.2;
                margin-bottom: 0.2;
                margin-left: 1.2em;
                margin-right: 0;
            }
            #suco{
                display: block;
                font-size: 1em;
                margin-top: 0.2;
                margin-bottom: 0.2;
                margin-left: 1.2em;
                margin-right: 0;
            }
            .forms {
                display: block;
            }
            .forms > form {
                display: inline-block;
            }
            .campo1 {
                float:left;
            }
            button {
                border: none;
                background-color: transparent;
                outline: none;
                width: 150px;
                height: 35px;
                border: solid 1px #088CC9; /*Cor da linha do objeto quando o mouse está sobre o mesmo*/
                border-radius: 5px; /*Define o arredondamento do objeto*/
            }
            button:focus {
                border: 5px;
                background: #ffff00;
                border: solid 1px #088CC9; /*Cor da linha do objeto quando o mouse está sobre o mesmo*/
                border-radius: 5px; /*Define o arredondamento do objeto*/
            }
            button:hover {
                border: 5px;
                background: #ffcf00;
                border: solid 1px #088CC9; /*Cor da linha do objeto quando o mouse está sobre o mesmo*/
                border-radius: 5px; /*Define o arredondamento do objeto*/
            }
            button:visited {
                border: 5px;
                background: #ffff00;
                border: solid 1px #088CC9; /*Cor da linha do objeto quando o mouse está sobre o mesmo*/
                border-radius: 5px; /*Define o arredondamento do objeto*/
            }

        </style>
    </head>
    <body>

    <?php
          include('db_connect.php');
    ?>

    <header id="topo">
      <table border=0 width="100%" cellpadding="0">
       <tr>
        <td width="30%" align="center" valign="midle">
         <img src="img/logo.jpg" align="midle" alt="Cantina Logo" height="42" width="98"/> <br />
        </td>

        <td width="40%" align="center" valign="midle">
         <h1><em> Cantina do Dindo - Almo&ccedil;o e Lanches</em></h1>
        </td>
        <td width="30%" align="center" valign="midle">
          <p style="text-align: right;">
           <?php
            echo" Bem vindo <b>$logado</b>! ";
          ?>
         </p>
        </td>
       </tr>
      </table>
    </header>

    <nav id="menu">
      <div class="forms">
      <form method="post" action="inicio.php">
         <button class="button" type="submit" >Início</buttom>
      </form>
      <form method="post" action="almoco.php">
         <button class="button" type="submit" >Almoço</buttom>
      </form>
      <form method="post" action="lanche.php">
         <button class="button" type="submit">Lanche</buttom>
      </form>
      <form method="post" action="relatorios.php">
         <button class="button" type="submit">Relat&oacute;rios</buttom>
      </form>


      <form method="post" action="doLogout.php">
         <button type="submit" style="width: 150px; height: 35px">Sair</buttom>
      </form>
      </div>

    </nav>

    <section id="meio">

        <article id="conteudo">
            <div id="titulo">
            </div>

            <div id="operacao">
               <font size=5> Sistema de Registro de Almoços </font><br />

            </div>
            <div id="texto_inicio">
              <?php
                $data_atual = date('d/m/Y H:i');
		$dia_atual = date('d/m/Y');
		$t = './pega_ender_ip.sh';
			$cmd    = escapeshellcmd($t);
            $endereco_ip_wlan = shell_exec($cmd);

            echo "<table border=0 width=\"100%\" cellspacing=\"1\" cellpadding=\"4\">";
			echo "<tr><td>";

                  $query = "SELECT * FROM `Entradas_Registradas` where `produto` = \"Almoco\" and `datahora` like \"$dia_atual%\"";
                  $resultado = mysqli_query($conexao,$query);
                  $quantidade_almocos = 0;
                  $valor_almoco = 0;
                   while ($linha = mysqli_fetch_array($resultado)) {
                    if ($linha['removido'] == "NAO") {
                        $quantidade_almocos = $quantidade_almocos + 1;
                        $valor_almoco = $valor_almoco + $linha['valor'];
                    }
                  }

                  $query = "SELECT * FROM `Entradas_Registradas` where `produto` = \"Suco\" and `datahora` like \"$dia_atual%\"";
                  $resultado = mysqli_query($conexao,$query);
                  $quantidade_sucos = 0;
                  $valor_suco = 0;
                  while ($linha = mysqli_fetch_array($resultado)) {
                    if ($linha['removido'] == "NAO") {
                            $quantidade_sucos = $quantidade_sucos + $linha['quantidade'];
                    $valor_suco = $valor_suco + $linha['valor'];
                    }
                  }
                  $valor_total = $valor_suco + $valor_almoco;
                  $quantidade_total = $quantidade_almocos + $quantidade_sucos;

               echo "<br /><b>Relatório do dia: </b><br />";
                          echo "<table border=0 width=\"70%\" cellspacing=\"10\" cellpadding=\"4\">";
                          echo "<tr> 
                                    <td><b>Item</b></td> 
                                    <td align=\"center\"><b>Quantidade</b></td>
                                    <td align=\"right\"><b>Valor (R$)</b></td>
                                </tr>";
                          echo "<tr> 
                                    <td>Almocos </td> 
                                    <td align=\"center\">" . $quantidade_almocos . "</td>
                                    <td align=\"right\">".number_format($valor_almoco,2,',','.')."</td>
                                </tr>";

                          echo "<tr> 
                                     <td >Sucos   </td> 
                                     <td align=\"center\">" . $quantidade_sucos . "</td>
                                     <td align=\"right\">".number_format($valor_suco,2,',','.')."</td>
                                </tr>";
                          echo "<tr> 
                                     <td><b>Total</b>   </td> 
                                     <td align=\"center\"><b>" . $quantidade_total . "</b></td>
                                     <td align=\"right\"><b>".number_format($valor_total,2,',','.')."</b></td>
                                </tr>";

                          echo "</table>";
		 echo "</td>";
		 echo "<td>";
		 echo "Endereco IP: $endereco_ip_wlan<br />";
                 $data_atual = date('d/m/Y H:i');
                 $dia_atual = date('d/m/Y');

		 echo "<p> Dia: $dia_atual <br /></p>";


		 echo "<br />";
		 echo "<b> Estado Servidor: </b>";
		 echo "<br />";
                 if (isset($_GET['reiniciar'])) {
                      if ($_GET['reiniciar'] == "sim") {

			      echo "Reiniciando controlador...";
                         $t = 'sudo ../resetaControleCantina.sh';
                         $cmd    = escapeshellcmd($t);
			 $output = shell_exec($cmd);
			 echo " ok! <br />";
                      }
                   }

                   $t = './estado_server.sh ';
                   $cmd    = escapeshellcmd($t);
                   $output = shell_exec($cmd);
                   echo " > $output</b><br />";
		   echo "<br />
               <form action=\"inicio.php\">
                   <input type=\"hidden\" name=\"reiniciar\"  value=\"sim\">
                   <button class=\"button\" type=\"submit\">Reinicia Servidor</buttom>
               </form>";


			  echo "</td></tr>";
			  echo "</table>";

                  ?>
         
            </div>


        </article>

        <aside id="lateral">

<?php

       if (isset($_GET['nome'])){

         if ($_GET['nome'] != "") {
				$nome = $_GET['nome'];

           $query = "from `Clientes` WHERE `cliente_nome` LIKE '%" .$nome."%' or `cliente_familia` LIKE '%".$nome."%'";

           $total = mysqli_query($conexao,"SELECT count(*) as qtd " .$query);
           $t = mysqli_fetch_assoc($total);
           $n = $t['qtd'];

           $resultado = mysqli_query($conexao,"SELECT * ".$query);

           if ($n == 0) {
              echo "Nenhum cliente encontrado! Tente novamente.";
           }
           else {
                          echo "<font size=\"2\">";
                          echo "<table border=0 cellspacing=\"10\" cellpadding=\"4\">";
                          echo "<tr>";
                          echo "<td><b> Cliente </b></td>";
                          echo "</tr>";
                          while ($linha = mysqli_fetch_array($resultado))
                          {
                            echo "<tr>";
                            echo "<td> <a href='?cliente_busca=".$linha['cliente_nome']."'>".$linha['cliente_nome'] ."</a></td>";

                            echo "</tr>";
                          }
                          echo "</table>";

           }

         }
     }

?>

        </aside>

    </section>

    <footer id="rodape">
    </footer>

    </body>

</html>  
