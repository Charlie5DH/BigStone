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
                width: 95%; /*largura*/
                background-color: #f90; /*cor de fundo*/
                height: 80%;; /*altura*/
            }
            #lateral{
                float:right; /*define que o elemento deve flutuar à direita*/
                background-color: #ffffff; /*cor de fundo*/
                padding: 2px; /*espaço entre a borda e o conteúdo do elemento*/
                width: 18%; /*largura*/
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

    <?php

$data_atual = date('d/m/Y H:i');
$dia_atual = date('d/m/Y');
$t = './pega_ender_ip.sh';
$cmd = escapeshellcmd($t);
$endereco_ip_wlan = shell_exec($cmd);
?>


    <link rel="stylesheet" href="libs/jquery-ui.css">
    <script src="libs/jquery-1.12.4.js"></script>
    <script src="libs/jquery-ui.js"></script>

    <script type="text/javascript">
    $(document).ready(function () { 
            ip = "<?php echo $endereco_ip_wlan ?>";
            $.ajax({
                method: "GET",
                url: "http://" + ip + ":4567/ultimaAtualizacao",
            }).done(function (answer) {
                $('#sinc').html(answer);

            }).fail(function (jqXHR, textStatus) {
                console.log("getLastSync failed: " + textStatus); //executa se falhar 
            });
    } );
    </script>

    <script type="text/javascript">
    		$( function() {
			$( "#datepicker_set" ).datepicker({ dateFormat: 'dd/mm/yy' }).val();
            } );
    </script>

    <script type="text/javascript">
         function confirma_pagto(id_entrada) {
		 var r=confirm("Confirma pagamento? ");
		 if (r==true)
		 {

            ip = "<?php echo $endereco_ip_wlan ?>";
            // console.log("Endereco ip: "+ ip)
            // console.log("Endereco ip: "+ id_entrada)

            $.ajax({
                method: "POST",
                url: "http://" + ip + ":4567/paga",
                data: { "id" : id_entrada }
            }).done(function (answer) {
                alert("Registrado pagamento com sucesso!")
                console.log("Pago com sucesso")

            }).fail(function (jqXHR, textStatus) {
                console.log("confirma_pagto failed: " + textStatus); //executa se falhar 
            });
            location.reload();
		 }
         }
	</script>

    <script type="text/javascript">
        function confirma_remover(id_entrada) {
		var r=confirm("Confirma remover?");
        if (r==true)
		 {
            ip = "<?php echo $endereco_ip_wlan ?>";
            // console.log("Endereco ip: "+ ip)
            // console.log("Endereco ip: "+ id_entrada)

            $.ajax({
                method: "POST",
                url: "http://" + ip + ":4567/apaga",
                data: { "id" : id_entrada }
            }).done(function (answer) {
                //alert("Removido com sucesso!")
                console.log("Removido com sucesso")

            }).fail(function (jqXHR, textStatus) {
                console.log("confirma_remover failed: " + textStatus); //executa se falhar 
            });
            location.reload();
        
		 }
         }
    </script>
    
    <script type="text/javascript">
        function sincroniza_dados(dia_atual) {
         
            console.log("sincroniza: " + dia_atual);
	    	var r=confirm("Confirma envio de dados?");
            if (r==true)
            {
                ip = "<?php echo $endereco_ip_wlan ?>";
                // console.log("Endereco ip: "+ ip)
                // console.log("Endereco ip: "+ id_entrada)

                $.ajax({
                    method: "POST",
                    url: "http://" + ip + ":4567/sincroniza",
                    data: { "dia" : dia_atual }
                }).done(function (answer) {
                    alert("Sincronizado com sucesso!")

                }).fail(function (jqXHR, textStatus) {
                    console.log("sincroniza_dados failed: " + textStatus); //executa se falhar 
                    //alert("ERRO: Não consegui sincronizar!")
                });
                location.reload();
            }
         }
	</script>
     
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
         <h1><em> Cantina do Dindo</em></h1>
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
               <font size=5> Registros do Dia</font><br />

<?php

    $dia_atual = date('d/m/Y');
	$t = './pega_ender_ip.sh';
	$cmd = escapeshellcmd($t);
    $endereco_ip_wlan = shell_exec($cmd);

    # echo "IP: " . $endereco_ip_wlan;

    if (isset($_GET['bday'])) {
		$dia_atual = $_GET['bday'];
    }
    $query_cli = "";
    if (isset($_GET['cliente_busca'])) {
        $cliente = $_GET['cliente_busca'];
        $query_cli = " and `cliente` = \"".$cliente."\"";
	}

    $query = "SELECT `valor` FROM `Entradas_Registradas` where `removido` != \"SIM\" and `produto` = \"Almoco\" and `datahora` like \"$dia_atual%\"".$query_cli;
    $total = mysqli_query($conexao,$query);
    $quantidade_almocos = 0;
    $valor_almocos = 0;
    while ($linha = mysqli_fetch_array($total)) {
        $quantidade_almocos = $quantidade_almocos + 1;
        $valor_almocos = $valor_almocos + $linha['valor'];
    }

    $query = "SELECT `quantidade`,`valor` FROM `Entradas_Registradas` where `removido` != \"SIM\" and `produto` = \"Suco\" and `datahora` like \"$dia_atual%\"".$query_cli;
    $resultado = mysqli_query($conexao,$query);
    $quantidade_sucos = 0;
    $valor_sucos = 0;
    while ($linha = mysqli_fetch_array($resultado)) {
        $quantidade_sucos = $quantidade_sucos + $linha['quantidade'];
        $valor_sucos = $valor_sucos + $linha['valor'];
    }

    $qtotal = $quantidade_sucos + $quantidade_almocos;
    $vtotal = $valor_sucos + $valor_almocos;

        $seq = 0;
  
        $query = "SELECT * FROM `Entradas_Registradas` where `datahora` like \"$dia_atual%\" $query_cli ORDER BY `id` DESC";
        
        $resultado = mysqli_query($conexao,$query);

	echo "<form action=\"relatorios.php\">";
    echo "<table width=\"80%\" border=0 cellspacing=\"10\" cellpadding=\"4\">";
    echo "<tr>";

    echo "<td VALIGN=\"top\">";
        echo "<table border=0 width=\"50%\" cellspacing=\"10\" cellpadding=\"10\">";
        echo "<tr>";
        echo "<td VALIGN=\"bottom\"> Data: </td>";
        echo "<td VALIGN=\"bottom\"><input value=\"" . $dia_atual . "\" type=\"text\" id=\"datepicker_set\" name=\"bday\" style=\"width: 180px\"></td>";
        echo "</tr>";
        echo "<tr>";
        echo "<td>";
        echo "</td>";
        echo "<td>";
        echo "<button type=\"submit\" style=\"width: 180px; height: 35px\">Selecionar</button>";
        echo "</td>";
        echo "</tr>";
        echo "</table>";
    echo "</td>";

    echo "<td VALIGN=\"top\">";
        echo "<b>Registros do dia: </b>";
        echo "<table border=0 width=\"80%\" cellspacing=\"10\" cellpadding=\"10\">";
        echo "<tr> <td></td> <td>Quantidade</td><td align=\"right\">Valor (R$)</td></tr>";
        echo "<tr> <td>Almocos: </td> <td>" . $quantidade_almocos . "</td><td  align=\"right\">" . number_format($valor_almocos,2,',','.'). "</td></tr>";
        echo "<tr> <td>Sucos:   </td> <td>" . $quantidade_sucos . "</td><td align=\"right\">" . number_format($valor_sucos,2,',','.') . "</td></tr>";
        echo "<tr> <td><b>Total</b></td> <td><b>".$qtotal."</b></td><td align=\"right\"><b>".number_format($vtotal,2,',','.')."</b></td></tr>";
        echo "</table>";
    echo "</td>";
    echo "</tr>";
    echo "</table>";
    echo "</form>";

    echo "<font size=\"3\">";
    echo "Dia: $dia_atual";

    if (isset($_GET['cliente_busca'])) {
        echo "<br />";
        echo "<br />";  
        echo "<b>Cliente: $cliente</b>";
        echo "<br />";
    }
    echo "</font>";

                echo "<font size=\"2\">";
                echo "<table border=0 width=\"90%\" cellspacing=\"10\" cellpadding=\"4\" VALIGN=\"top\">";
                echo "<tr>";
                echo "<td> ";
                echo "<table border=0 width=\"100%\" cellspacing=\"3\" cellpadding=\"2\" VALIGN=\"top\">";
                echo "<tr>";
                echo "<td><b> Numero   </b></td>";
                echo "<td><b> Cliente   </b></td>";
                echo "<td><b> Data Hora </b></td>";
                echo "<td><b> Produto   </b></td>";
                echo "<td><b> Quantidade </b></td>";
                echo "<td><b> Valor (R$)     </b></td>";
                echo "<td align=\"center\"><b> A&ccedil;&otilde;es</b></td>";
                echo "</tr>";

                while ($linha = mysqli_fetch_array($resultado)) {

				  $seq += 1;

                echo "<tr>";
                echo "<td>".$linha['id'] ."</td>";
                echo "<td>".$linha['cliente'] ."</td>";
			    echo "<td>".$linha['datahora']."</td>";
                echo "<td>".$linha['produto'] ."</td>";
                echo "<td align=\"right\">".$linha['quantidade']."</td>";
			    if ($linha['removido'] == "SIM") {
				    echo "<td align=\"right\"><strike>".number_format($linha['valor'],2,',','.')."</strike></td>";
			    } else {
			       echo "<td align=\"right\">".number_format($linha['valor'],2,',','.')."</td>";
			    }
			    echo "<td>";

                echo "<table border=0 width=\"100%\" cellspacing=\"10\" cellpadding=\"4\" VALIGN=\"top\" align=\"center\">";
                echo "<tr>";
                            echo "<td align=\"center\" width=\"50%\">";
                                if ($linha['removido'] == "NAO") {
                                    if ($linha['pago'] == "Aberto") {
            
                                        echo "<form id=\"pagto_form".$seq."\" action=\"relatorios.php\">";
                                        echo "<input type=\"button\" value=\"Pagar\" onclick=\"confirma_pagto('".$linha['id']."');\" />";
                                        echo "</form>";
                        
                                    }
                                    else {
                                        echo $linha['pago'];
                                    }
                                }
                                else {
                                    if ($linha['removido'] != "SIM") {
                               
                                        if ($linha['pago'] == "SIM") {
                                            echo "Pago";
                                        }
                                        else {
                                            echo $linha['pago'];
                                        }
                                    }
                                }
                            echo "</td>";
                            echo "<td align=\"center\" width=\"50%\">";
                                if ($linha['removido'] == "NAO") {
                                    echo "<form id=\"remove_form".$seq."\" action=\"relatorios.php\">";
                                    echo "<input type=\"button\" value=\"Remover\" onclick=\"confirma_remover('".$linha['id']."');\" />";
                                    echo "</form>";
                    
                                }
                                else {
                                    if ($linha['removido'] == "SIM") {
                                        echo "Removido";
                                    }

                                    if (($linha['removido'] == "fechado") &&  ($linha['pago'] == "DEPOSITO")) {
                                            echo $linha['id_org'];
                                    }
                                }
                            echo "</td>";
                            echo "</tr>";
			    echo "</table>";

			    echo "</td>";
                            echo "</tr>";
                          } 
                          echo "</table>";
                          echo "</td>";
                          echo "</tr>";
                          echo "</table>";
                  


          ?>
            </div>


        </article>

        <aside id="lateral">
        <br />
        <br /><b> <font size=4> Envio de Dados para Servidor:</font></b>
        <br />
        <br />
        <button onclick="sincroniza_dados('<?php echo $dia_atual;  ?>')">Encaminhar registros</button>

        <br />
        <br /> Ultima sincronização: 
        <div id="sinc">  </div>
        <br />
        <hr>

        <br /><b> <font size=4> Busca pessoa:</font></b>
            <div id="nome_manual"> <br />
    			    <form action="relatorios.php">
                    <center><button type="submit" >Buscar</button></center>
				       <table width="100%" border=0 cellspacing="10" cellpadding="1" VALIGN="top">
                   <tr><td>Nome:     </td><td> <input type="text" name="nome" style="width: 200px" height="40">  <br /></td></tr>
                   </table>
                   <?php
                        if (isset($_GET['bday'])) {
                            echo "   <input type=\"hidden\" name=\"bday\" value=\"".$_GET['bday']."\">";
                        }
                   ?>
                 </form>
            </div>
        <?php

$query = " from `Clientes` WHERE ";
$nome = "";
$matr = "";

if (isset($_GET['nome'])){
  if ($_GET['nome'] != "") {
      $nome = $_GET['nome'];
    $query_nome = "`cliente_nome` LIKE '%" .$nome."%' or `cliente_familia` LIKE '%".$nome."%' ";
  }
}

if ($nome != "") {
      $query = $query . $query_nome;
}
else {
      $query = "";
}

if ($query != "") {

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
          $bday_info = "";
          if (isset($_GET['bday'])) {
              $bday_info="&bday=".$dia_atual;
          }
          echo "<td> <a href='?cliente_busca=".$linha['cliente_nome'].$bday_info."'>".$linha['cliente_nome'] ."</a></td>";
          echo "</tr>";
       }
       echo "</table>";
    }
}
?>


        </aside>

    </section>

    <footer id="rodape">
    </footer>

    </body>
	 
</html>  
