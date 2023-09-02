<?php
session_start();
   session_destroy();
   header("location:index.php"); //feito
   echo"<script language='javascript' type='text/javascript'>;window.location.href='index.php';</script>";
   exit();
?>
