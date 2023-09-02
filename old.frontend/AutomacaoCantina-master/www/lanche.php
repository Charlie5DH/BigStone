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
                margin-left: 0;
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
                width: 160px;
                height: 45px;
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

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

    
      
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
         <button style="width: 150px; height: 35px" type="submit" >Início</buttom>
      </form>
      <form method="post" action="almoco.php">
         <button style="width: 150px; height: 35px" type="submit" >Almoço</buttom>
      </form>
      <form method="post" action="lanche.php">
         <button style="width: 150px; height: 35px" type="submit">Lanche</buttom>
      </form>
      <form method="post" action="relatorios.php">
         <button style="width: 150px; height: 35px" type="submit">Relat&oacute;rios</buttom>
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
               <font size=5> Lanches</font><br />
<?php

    $dia_atual = date('d/m/Y');
	$t = './pega_ender_ip.sh';
	$cmd = escapeshellcmd($t);
    $endereco_ip_wlan = shell_exec($cmd);

    echo "Endereço: ".$endereco_ip_wlan;
?>

<br />
        <table width="1100" border=0 cellspacing="1" cellpadding="1" VALIGN="top">
			<tr>
                <td width="450" VALIGN="top" align="center">
                   <table width="100%" border=0 cellspacing="1" cellpadding="1" VALIGN="top">
                   <!-- <tr><td align="center">
                        <b> <font size=4> Busca pessoa:</font>
                        <div id="nome_manual"> <br />
                            <form action="lanche.php">
                                <table width="250" border=0 cellspacing="10" cellpadding="1" VALIGN="top">
                                    <tr><td>Nome:     </td><td> <input type="text" name="nome" style="width: 200px" height="40">  <br /></td></tr>
                                    <tr><td>Matrícula:</td><td> <input type="text" name="matr" style="width: 200px" height="40">  <br /></td></tr>
                                </table>
                                <center><button style="width: 150px; height: 35px" type="submit" >Buscar</button></center>
                            </form>
                        </div>
                    </td></tr> -->
                    <tr><td align="left">
                    <?php echo "Data atual: $dia_atual"; ?><br /><br />
                    <font size=5> Operação:</font><br />

                    <table width="100%" border=0 cellspacing="10" cellpadding="1" VALIGN="top">
                        <tr>
                            <td width="25%"><b>Identificação:</b></td>
                            <td align="left"><div id="nome" class="nome"> Aguardando pessoa ... </div></td>
                        </tr>

                        <tr>
                            <td width="25%"><b>Lanche:</b></td>
                            <td align="left"><div id="produto" class="produto"> </div></td>
                        </tr>
                        <tr>
                            <td width="25%"><b>Quantidade:</b></td>
                            <td>
                                <table width="100%" border=0 cellspacing="1" cellpadding="1" VALIGN="top">
                                    <tr>
                                        <td width="30%"> <div id="lanches"> 1 </div></td>
                                        <td> Quantos:
                                        <select id="qnt_lanches" name="qnt_lanches" onchange="if (this.selectedIndex) ConfirmaQuantidade()">
                                            <option value="1" selected > 1 </option>
                                            <option value="2"> 2 </option>
                                            <option value="3"> 3 </option>
                                            <option value="4"> 4 </option>
                                        </select>
                                        </td>
                                    </tr>
                                    </table>
                            </td>
                        </tr>
                    </table>
                    <tr><td align="center">
				<br />

              <button style="width: 150px; height: 35px" onclick="ConfirmRegister()">Confirmar registro</button>
              <button style="width: 150px; height: 35px" onclick="CancelRegister()">Cancelar</button>
            </td></tr>
            </td></tr></table>

            </td>

            <td width=650>

                <?php
                $resultado = mysqli_query($conexao,"SELECT * from Produtos");
                while ($linha = mysqli_fetch_array($resultado))
                {
                    $produto = $linha['prd_produto'];
                    $prd = (strlen($produto) > 20) ? substr($produto,0,20).'...' : $produto;
                    echo "<button onclick=\"ConfirmProduct('".$produto."')\">".$prd."</button>";
                }
                ?>

            </td>
            </tr></table>

        </div>

        <HR>
            <div id="texto_inicio">
               <font size=5> Ultimos registros </font><br />
          <?php

                      $mostra = 5;
                
                      $query = "SELECT * FROM `Entradas_Registradas` where `datahora` like \"$dia_atual%\" ORDER BY `id` DESC ; #limit 0,$mostra";
                      
                      $resultado = mysqli_query($conexao,$query);

                          echo "<font size=\"2\">";
                          echo "<table border=0 width=\"100%\" cellspacing=\"10\" cellpadding=\"4\" VALIGN=\"top\">";
                          echo "<tr>";
                          echo "<td> ";
                          echo "<table border=0 width=\"90%\" cellspacing=\"10\" cellpadding=\"4\" VALIGN=\"top\">";
                          echo "<tr>";
                          echo "<td><b> Numero   </b></td>";
                          echo "<td><b> Cliente   </b></td>";
                          echo "<td><b> Produto   </b></td>";
                          echo "<td align=\"right\"><b> Quantidade </b></td>";
                          echo "<td align=\"right\"><b> Valor (R$)     </b></td>";
                          echo "<td align=\"center\"><b> Data Hora </b></td>";
                          echo "<td align=\"center\"> <b> Açoes </b></td>";
                          echo "</tr>";
                          while ($linha = mysqli_fetch_array($resultado)) {
                            echo "<tr>";
                            echo "<td>".$linha['id'] ."</td>";

                            echo "<td>";
                            echo "<form id=\"busca_pessoa".$seq."\" action=\"almoco.php\">";
                            echo "<input type=\"button\" value=\"".$linha['cliente']."\" 
                              onclick=\"ConfirmaPessoaFromName('".$linha['cliente']."');\" />";
                            echo "</form>";
                            echo "</td>";
        
                          #  echo "<td>".$linha['cliente'] ."</td>";
                            echo "<td>".$linha['produto'] ."</td>";
                            echo "<td align=\"right\">".$linha['quantidade']."</td>";
                            if ($linha['removido'] == "SIM") {
                                echo "<td align=\"right\"><strike>".number_format($linha['valor'],2,',','.')."</strike></td>";
                            } else {
                               echo "<td align=\"right\">".number_format($linha['valor'],2,',','.')."</td>";
                            }
                            echo "<td align=\"center\">".$linha['datahora']."</td>";

                            echo "<td>";

                            echo "<table border=0 width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" VALIGN=\"top\" align=\"center\">";
                            echo "<tr>";
                            echo "<td align=\"center\" width=\"50%\">";
                                if ($linha['removido'] == "NAO") {
                                    if ($linha['pago'] == "Aberto") {
            
                                        echo "<form id=\"pagto_form".$seq."\" action=\"relatorios.php\">";
                                        echo "<input type=\"button\" value=\"Pagar\" onclick=\"confirma_pagto('".$linha['id']."');\" />";
                                        echo "</form>";
                        
                                    }
                                    else {
                                        if ($linha['pago'] == "Aberto") {
                                            echo $linha['pago'];
                                        }
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
                          echo "<td VALIGN=\"top\">";
                         
                          echo "</td>";
                          echo "</tr>";
                          echo "</table>";
                  


          ?>
            </div>
    </article>

    <aside id="lateral">

    <b> <font size=4> <br /><br />Busca pessoa:</font>
                        <div id="nome_manual"> <br />
                            <form action="lanche.php">
                                <table width="250" border=0 cellspacing="10" cellpadding="1" VALIGN="top">
                                    <tr><td>Nome:     </td><td> <input type="text" name="nome" style="width: 200px" height="40">  <br /></td></tr>
                                    <tr><td>Matrícula:</td><td> <input type="text" name="matr" style="width: 200px" height="40">  <br /></td></tr>
                                </table>
                                <center><button style="width: 150px; height: 35px" type="submit" >Buscar</button></center>
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

if (isset($_GET['matr'])){
  if ($_GET['matr'] != "") {
      $matr = $_GET['matr'];
    $query_matr = "`cliente_matricula` = '" .$matr. "' ";
  }
}

if ($nome != "") {
   if ($matr != "") {
      $query = $query . $query_nome . " and " . $query_matr;
   } 
   else { 
      $query = $query . $query_nome;
   }
}
else {
   if ($matr != "") {
      $query = $query . $query_matr;
   }
   else {
      $query = "";
   }
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
         echo "<td>";
         echo "<form id=\"busca_pessoa".$seq."\" action=\"almoco.php\">";
         echo "<input type=\"button\" value=\"".$linha['cliente_nome']."\" onclick=\"ConfirmaPessoa('".$linha['cliente_matricula']."');\" />";
         echo "</form>";
         echo "</td>";
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

    <script type="text/javascript">
    $(document).ready(function () { 
            ip = "<?php echo $endereco_ip_wlan ?>";
            $.ajax({
                method: "GET",
                url: "http://" + ip + ":4567/dados_lanche",
            }).done(function (answer) {
                $('#produto').html(answer.produto);
                $('#nome').html(answer.nome);
                $('#lanches').html(answer.quantidade);

            }).fail(function (jqXHR, textStatus) {
                console.log("getLastSync failed: " + textStatus); //executa se falhar 
            });
    } );

    </script>
	

    <script type="text/javascript">
      function ConfirmRegister()
      {
        	ip = "<?php echo $endereco_ip_wlan ?>";
            nome = document.getElementsByClassName("nome")[0].innerHTML;
            lanche = document.getElementsByClassName("produto")[0].innerHTML;

            console.log("Nome cliente: " + nome);

            if (nome == "Aguardando identificação...") {
                alert ("Informe o nome da pessoa");
                return;                  
            }

            console.log("Lanche: " + lanche);

            if (lanche == "Selecione lanche ...") {
                alert ("Informe o Lanche");
                return;                  
            }


            if (confirm("Confirma registro para " + nome + "?"))
            $.ajax({
                method: "POST",
                url: "http://" + ip + ":4567/confirma_lanche",
                data: { "nome" : nome }
            }).done(function (answer) {
                $('#nome').html(answer);//Executa se tiver sucesso
                window.location = window.location.pathname

            }).fail(function (jqXHR, textStatus) {
                console.log("ConfirmRegister failed: " + textStatus); //executa se falhar 
	    });
      }
      function ConfirmProduct(produto)
      {
        	ip = "<?php echo $endereco_ip_wlan ?>";

            console.log("Produto: " + produto);

            if (produto == "Selecione lanche ...") {
                alert ("Informe o produto");
                return;                  
            }

            $.ajax({
                method: "POST",
                url: "http://" + ip + ":4567/produto",
                data: { "produto" : produto }
            }).done(function (answer) {
                $('#produto').html(answer);//Executa se tiver sucesso

            }).fail(function (jqXHR, textStatus) {
                console.log("ConfirmProdutct failed: " + textStatus); //executa se falhar 
	    });
      }
    </script>

    <script type="text/javascript">
      function ConfirmaPessoa(matricula)
      {
    	ip = "<?php echo $endereco_ip_wlan ?>";
	    console.log("Informa matricula: " + matricula + " ip: " + ip);

            $.ajax({
                method: "POST",
                url: "http://" + ip + ":4567/matricula",
                data: { "matricula" : matricula }
            }).done(function (answer) {
                $('#nome').html(answer);//Executa se tiver sucesso
                
            }).fail(function (jqXHR, textStatus) {
                console.log("ConfirmaPessoa failed: " + textStatus); //executa se falhar 
	    });
      }
    </script>


<script type="text/javascript">
      function ConfirmaPessoaFromName(nome)
      {
    	ip = "<?php echo $endereco_ip_wlan ?>";
	    console.log("Informa nome: " + nome);

            $.ajax({
                method: "POST",
                url: "http://" + ip + ":4567/nome",
                data: { "nome" : nome }
            }).done(function (answer) {
                $('#nome').html(answer);//Executa se tiver sucesso
                
            }).fail(function (jqXHR, textStatus) {
                console.log("ConfirmaPessoafromName failed: " + textStatus); //executa se falhar 
	    });
      }
    </script>

    <script type="text/javascript">
      function CancelRegister()
      {
	    ip = "<?php echo $endereco_ip_wlan ?>";
        $.ajax({
                method: "GET", //GET OU POST
                url: "http://" + ip + ":4567/cancela" //LOCAL DO ARQUIVO

            }).done(function (answer) {
                $('#confirma').html(answer);//Executa se tiver sucesso
                window.location = window.location.pathname

            }).fail(function (jqXHR, textStatus) {
                console.log("CancelRegister failed: " + textStatus); //executa se falhar 
	    });
	    location.reload();
        console.log("reload");
      }
    </script>


    <script type="text/javascript">
      function ConfirmaQuantidade()
      {
        	ip = "<?php echo $endereco_ip_wlan ?>";
            qnt = document.getElementById("qnt_lanches").value
            
            console.log("Quantidade: " + qnt + " " + ip);
            $.ajax({
                method: "POST", //GET OU POST
                url: "http://" + ip + ":4567/quantidade_produto", //LOCAL DO ARQUIVO
                data: { "quantidade": qnt }

            }).done(function (answer) {
                $('#lanches').html(answer);//Executa se tiver sucesso
                console.log("Sucesso: " + answer)

            }).fail(function (jqXHR, textStatus) {
                console.log("ConfirmaQuantidade failed: " + textStatus); //executa se falhar 
            });
      }
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
                //alert("Registrado pagamento com sucesso!")
                console.log("Pago com sucesso")

            }).fail(function (jqXHR, textStatus) {
                console.log("confirma_pagto failed: " + textStatus); //executa se falhar 
                //alert("ERRO: Não consegui fazer o pagamento!")
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
                //alert("ERRO: Não consegui remover!")
            });
            location.reload();
        
		 }
         }
    </script>

</html>  
