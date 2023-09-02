<?php 
// session_start inicia a sessão
session_start();

// as variáveis login e senha recebem os dados digitados na página anterior
$login = $_POST['login'];
$senha = $_POST['senha'];

include('config_db.ini');

// Conectar com o bando de dados.
$conexao = mysqli_connect($db_host,$db_user,$db_pass,$db_name) or die($msg[0]);


$result = mysqli_query($conexao,"SELECT * FROM `credenciais` WHERE `NOME` = '$login' AND `SENHA`= '$senha'");
if(mysqli_num_rows ($result) > 0 )
{
	$_SESSION['login'] = $login;
	$_SESSION['senha'] = $senha;
	header('location:inicio.php'); //feito
        echo"<script language='javascript' type='text/javascript'>;window.location.href='inicio.php';</script>";
}
else{
	unset ($_SESSION['login']);
	unset ($_SESSION['senha']);
	echo"<script language='javascript' type='text/javascript'>alert('Login e/ou senha incorretos');window.location.href='index.php';</script>";
	}
?>
