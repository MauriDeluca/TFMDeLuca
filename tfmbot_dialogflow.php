<?php
include_once "../somosioticos/somosioticos_dialogflow.php";
credenciales('mauridelu', 'mauri7412');
//debug();


//conexion a la base de datos
$mysqli = mysqli_connect("localhost","id18509892_trabajofinaltfm","Mauridelu7412!","id18509892_dbbot");

if (!$mysqli) {
  echo "Error: No se puede conectar a la base de datos". PHP_EOL;
  die();
}

if (intent_recibido("consultar_ciudades")){
  //$resultado = $mysqli->query("SELECT * FROM `ciudades` WHERE 1");
  //$ciudades = mysqli_fetch_assoc($resultado);
  //$ciudad = $ciudades['ciudad'];
  $ciudades_a_enviar = consulta_ciudades();
  enviar_texto("Las ciudades son: $ciudades_a_enviar");

}


if (intent_recibido("Information - age")){
  $edad = obtener_variables()['edad'];

  enviar_texto("Bien, su edad es $edad años.\n¿Con quien estas pensando viajar en tus próximas vacaciones? (Sola/o - Pareja - Familia - Amigos - No lo se)");
}

if (intent_recibido("Information - company")){
  $compania = obtener_variables()['compania'];

  enviar_texto("Vale, perfecto, viajas $compania.\n¿Que fechas tenias pensado para sus próximas vacaciones?");

}

if (intent_recibido("Information - date")){
  $mes = obtener_variables()['mes'];
  $fecha_inicio = obtener_variables()['inicio'];
  $fecha_fin = obtener_variables ()['fin'];

  enviar_texto("Muy bien, estas pensando vacacionar entre $fecha_inicio y $fecha_fin.\nSi la informacion obtenida es correcta, entonces confirma");


}


if (intent_recibido("Information - date - yes")){

  enviar_texto("Correcto, sigamos.\n¿Que plan tenias pensado para tus proximas vacaciones?\n(Una ciudad grande o capital - Destino de veraneo - Destino con montañas o para aventura - Destino para ir en invierno)\n");

}


if (intent_recibido("destino_capital")){

  enviar_texto("Buena opcion.\n¿Le interesa mas estar en la naturaleza y estar al aire libre o que el destino tenga eventos culturales, museos, historia, etc?");

}

if (intent_recibido("destino_veraneo")){
    enviar_texto("Muy buena opcion!\n¿Le interesa mas estar en la naturaleza y aventura o que el destino sea de playa?");

}

if (intent_recibido("destino_montana_noinv")){

  enviar_texto("Muy buena opcion!\n¿Le interesa mas estar en la naturaleza y deportes de aventura o que el destino tenga eventos culturales, festivales, museos, historia, etc?");

}

if (intent_recibido("destino_invierno")){

  enviar_texto("Muy bien!\n¿Le interesa practicar deportes de invierno? (ski-snowboard)\nSalidas en la noche\nUn lugar con nieve\nBuena gastronomia y bebidas ");

}


//*************************************FUNCIONES**********************************

function consulta_ciudades(){
  global $mysqli;
  $resultado = $mysqli->query("SELECT * FROM `ciudades` WHERE 1");
  $ciudades = mysqli_fetch_assoc($resultado);
  $ciudad = $ciudades ['ciudad'];
  return $ciudad;
}


function verifica_rango($fecha_inicio, $fecha_fin) {
  $date_inicio = strtotime($fecha_inicio);
  $date_fin = strtotime($fecha_fin);
  if (($date_inicio > "2022-12-10T12:00:00-03:00") && ($date_fin < "2023-03-20T12:00:00-03:00"))
    return true;
  else {
    return false;
  }

}


#if (intent_recibido("calculadora")){
#  $valor1 = obtener_variables()['numero1'];
#  $valor2 = obtener_variables()['numero2'];
#  $resultado = $valor1 + $valor2;
#  enviar_texto("Luego de sumar los valores el resultado es $resultado");
#}
 ?>
