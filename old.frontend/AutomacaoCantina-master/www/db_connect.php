<?php

   include('config_db.ini');

   $msg[0] = "Conexão com o banco falhou!\n";
   $msg[1] = "Não foi possível selecionar o banco de dados!\n";

   $conexao = mysqli_connect($db_host,$db_user,$db_pass,$db_name) or die($msg[0]);

   mysqli_query($conexao,"SET NAMES 'utf8'");
   mysqli_query($conexao,'SET character_set_connection=utf8');
   mysqli_query($conexao,'SET character_set_client=utf8');
   mysqli_query($conexao,'SET character_set_results=utf8');
?>
