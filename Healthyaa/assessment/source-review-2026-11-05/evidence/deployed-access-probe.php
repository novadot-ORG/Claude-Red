<?php
// Run only on the isolated read-only source capture, never through WordPress.
// php deployed-access-probe.php /path/to/source-capture
$root = $argv[1] ?? exit(2);
define('ABSPATH', '/synthetic/');
function __($s, ...$args) { return $s; }
function current_user_can($cap) { return in_array($cap, $GLOBALS['caps'] ?? [], true); }
function register_rest_route($namespace, $route, $args) { $GLOBALS['routes'][$namespace . '/' . $route] = $args; }
class WP_REST_Server { const READABLE = 'GET'; const EDITABLE = 'POST, PUT, PATCH'; const CREATABLE = 'POST'; }
class WC_Payment_Gateway { public $id; }
require $root . '/public_html/wp-content/plugins/wc-thanks-redirect/src/Api.php';
require $root . '/public_html/wp-content/plugins/wc-thanks-redirect/src/Modules/SandBoxPayment.php';
$api = (new ReflectionClass('NeeBPlugins\\Wctr\\Api'))->newInstanceWithoutConstructor();
$api->register_routes();
$permission = $GLOBALS['routes']['wctr-api/v1/tyrules/fetch'][0]['permission_callback'];
$results = ['rule_read_has_permission_callback' => is_array($permission) && is_callable($permission)];
$GLOBALS['caps'] = [];
$results['anonymous_rule_read_denied'] = call_user_func($permission) === false;
$GLOBALS['caps'] = ['read'];
$results['ordinary_customer_rule_read_denied'] = call_user_func($permission) === false;
$GLOBALS['caps'] = ['manage_woocommerce'];
$results['shop_management_capability_allowed'] = call_user_func($permission) === true;
$gateway = (new ReflectionClass('NeeBPlugins\\Wctr\\Modules\\SandBoxPayment'))->newInstanceWithoutConstructor();
$source = file_get_contents($root . '/public_html/wp-content/plugins/wc-thanks-redirect/src/Modules/SandBoxPayment.php');
if (!preg_match('/\$this->id\s*=\s*\x27([^\x27]+)\x27/', $source, $match)) throw new RuntimeException('Gateway ID missing');
$gateway->id = $match[1];
$GLOBALS['caps'] = ['read'];
$results['current_gateway_id_filtered_for_customer'] = !isset($gateway->restrict_to_admins([$gateway->id => $gateway])[$gateway->id]);
$GLOBALS['caps'] = ['administrator'];
$results['current_gateway_id_retained_for_admin'] = isset($gateway->restrict_to_admins([$gateway->id => $gateway])[$gateway->id]);
echo json_encode(['mode'=>'actual deployed-source methods with synthetic capabilities; no HTTP or WordPress bootstrap','gateway_id'=>$gateway->id,'checks'=>$results,'all_expected_observations_reproduced'=>!in_array(false,$results,true),'real_orders_or_payments'=>false], JSON_PRETTY_PRINT), "\n";
exit(in_array(false, $results, true) ? 1 : 0);
