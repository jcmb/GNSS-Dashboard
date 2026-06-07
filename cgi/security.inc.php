<?php

function gnss_secret_key() {
   static $key = null;
   if ($key !== null) {
      return $key;
   }

   $env = getenv('GNSS_SECRET_KEY');
   if ($env !== false && $env !== '') {
      $key = $env;
      return $key;
   }

   $paths = array(
      '/usr/lib/cgi-bin/Dashboard/secret_key',
      dirname(__FILE__) . '/secret_key',
      dirname(__DIR__) . '/cgi/secret_key',
   );

   foreach ($paths as $path) {
      if (is_readable($path)) {
         $key = trim(file_get_contents($path));
         if ($key !== '') {
            return $key;
         }
      }
   }

   die('Security configuration error: secret key not found');
}

function gnss_csrf_token($user_id) {
   $secret = gnss_secret_key();
   $ts = (string)time();
   $msg = $user_id . ':' . $ts;
   $sig = hash_hmac('sha256', $msg, $secret);
   return $ts . ':' . $sig;
}

function gnss_validate_csrf($token, $user_id, $max_age = 3600) {
   if ($token === '' || strpos($token, ':') === false) {
      return false;
   }
   list($ts, $sig) = explode(':', $token, 2);
   if (!ctype_digit($ts)) {
      return false;
   }
   if (time() - (int)$ts > $max_age) {
      return false;
   }
   $secret = gnss_secret_key();
   $msg = $user_id . ':' . $ts;
   $expected = hash_hmac('sha256', $msg, $secret);
   return hash_equals($expected, $sig);
}

function gnss_csrf_field($user_id) {
   $token = gnss_csrf_token($user_id);
   return '<input type="hidden" name="csrf_token" value="' . h($token) . '">';
}

function h($value) {
   return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
}

function gnss_require_user_id($db) {
   if (empty($_REQUEST['User_ID'])) {
      die('Internal Error: Missing User ID');
   }
   $user_id = filter_var($_REQUEST['User_ID'], FILTER_VALIDATE_INT);
   if ($user_id === false) {
      die('Invalid User ID');
   }
   $stmt = $db->prepare('SELECT id FROM Users WHERE id=?');
   $stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
   $result = $stmt->execute();
   if (!$result || !$result->fetchArray()) {
      die('Invalid User ID');
   }
   return $user_id;
}

function gnss_verify_gnss_owner($db, $gnss_id, $user_id) {
   $gnss_id = filter_var($gnss_id, FILTER_VALIDATE_INT);
   if ($gnss_id === false) {
      die('Invalid receiver ID');
   }
   $stmt = $db->prepare('SELECT User_ID FROM GNSS WHERE id=?');
   $stmt->bindValue(1, $gnss_id, SQLITE3_INTEGER);
   $result = $stmt->execute();
   $row = $result ? $result->fetchArray(SQLITE3_ASSOC) : false;
   if (!$row || (int)$row['User_ID'] !== (int)$user_id) {
      die('Access denied');
   }
   return $gnss_id;
}

function gnss_display_receiver_password($stored) {
   if ($stored === null || $stored === '') {
      return '';
   }
   if (strpos($stored, 'enc:') !== 0) {
      return (string)$stored;
   }
   $cgi = is_dir('/usr/lib/cgi-bin/Dashboard')
      ? '/usr/lib/cgi-bin/Dashboard'
      : dirname(__FILE__);
   $code = 'import sys; from gnss_security import decrypt_receiver_password; print(decrypt_receiver_password(sys.argv[1]))';
   $cmd = 'cd ' . escapeshellarg($cgi) . ' && python3 -c ' . escapeshellarg($code) . ' ' . escapeshellarg($stored);
   $output = shell_exec($cmd);
   if ($output === null || trim($output) === '') {
      return '[encrypted]';
   }
   return trim($output);
}

?>
