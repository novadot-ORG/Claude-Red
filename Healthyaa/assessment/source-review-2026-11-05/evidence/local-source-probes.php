<?php
/** Offline probes of selected actual functions. No WordPress bootstrap/DB/network.
 * Run: php local-source-probes.php /path/to/healthyaa-wordpress
 * Stubs model only the dependencies needed by each assertion; not integration tests.
 */
$root = $argv[1] ?? exit(2);
define('ABSPATH', '/synthetic/');
define('ARRAY_A', 'ARRAY_A');
define('HOUR_IN_SECONDS', 3600);
function load_functions($path, $names) {
    $tokens = token_get_all(file_get_contents($path));
    $loaded = [];
    for ($i = 0; $i < count($tokens); $i++) {
        if (!is_array($tokens[$i]) || $tokens[$i][0] !== T_FUNCTION) continue;
        $j = $i + 1;
        while (is_array($tokens[$j]) && $tokens[$j][0] === T_WHITESPACE) $j++;
        if (!is_array($tokens[$j]) || !in_array($tokens[$j][1], $names, true)) continue;
        $name = $tokens[$j][1]; $code = ''; $depth = 0; $begun = false;
        for ($k = $i; $k < count($tokens); $k++) {
            $t = $tokens[$k]; $v = is_array($t) ? $t[1] : $t; $code .= $v;
            if ($t === '{' || (is_array($t) && in_array($t[0], [T_CURLY_OPEN, T_DOLLAR_OPEN_CURLY_BRACES], true))) { $depth++; $begun = true; }
            if ($t === '}') $depth--;
            if ($begun && $depth === 0) break;
        }
        eval($code); // Only named functions from the explicitly supplied local source.
        $loaded[] = $name;
    }
    if (count($loaded) !== count($names)) throw new RuntimeException('Missing source function');
}
function sanitize_key($s) { return preg_replace('/[^a-z0-9_\-]/', '', strtolower((string)$s)); }
function wp_salt($s) { return 'synthetic-salt'; }
function apply_filters($tag, $value, ...$args) { return $value; }
function get_transient($k) { return $GLOBALS['transients'][$k] ?? false; }
function set_transient($k, $v, $ttl) { $GLOBALS['transients'][$k] = $v; return true; }
function get_option($key, $default = '') { return $key === 'healthyaa_abandoned_cart_api_token' ? 'synthetic-secret' : $default; }
function __($s, ...$args) { return $s; }
function current_user_can($cap) { return $GLOBALS['admin'] ?? false; }
function wc_add_notice($message, $kind) { $GLOBALS['notices'][] = $message; }
function sanitize_text_field($s) { return trim(strip_tags((string)$s)); }
function update_post_meta($id, $key, $value) { $GLOBALS['saved'][$key] = $value; }
function remove_action($hook, $callback, ...$args) { $GLOBALS['removed'][] = [$hook, $callback]; }
class WP_Error {
    public $errors = [];
    public function __construct($code = '', $message = '', $data = []) { if ($code) $this->add($code, $message); }
    public function add($code, $message) { $this->errors[$code] = $message; }
}
class WP_REST_Request {
    public function __construct(public $headers = [], public $params = []) {}
    public function get_header($name) { return $this->headers[$name] ?? ''; }
    public function get_param($name) { return $this->params[$name] ?? null; }
}
class WC_Payment_Gateway { public $id; }
class SyntheticDatabase {
    public $prefix = 'synthetic_'; public $queries = [];
    public function prepare($sql, ...$args) { return [$sql, $args]; }
    public function get_row($query, $format) {
        $this->queries[] = $query;
        if (str_contains($query[0], 'email_hash = %s') && $query[1][0] === 'synthetic-victim-email-hash')
            return ['id'=>321,'cart_hash'=>'same-public-cart','item_count'=>1,'updated_at'=>'2026-11-05 00:00:00'];
        return null;
    }
}
$mu = $root . '/public_html/wp-content/mu-plugins/';
load_functions($mu . 'healthyaa-analytics.php', [
    'healthyaa_analytics_rate_limit_ok', 'healthyaa_analytics_ip_address', 'healthyaa_analytics_trust_forwarded_ip_headers',
    'healthyaa_analytics_find_cart_activity_row', 'healthyaa_analytics_should_reuse_cart_activity_row',
    'healthyaa_analytics_cart_table_name', 'healthyaa_analytics_existing_uuid',
    'healthyaa_analytics_rest_permission', 'healthyaa_analytics_rest_api_token', 'healthyaa_analytics_rest_request_token'
]);
load_functions($mu . 'healthyaa-checkout-refresh.php', [
    'healthyaa_checkout_refresh_delivery_options', 'healthyaa_checkout_refresh_sanitize_delivery_option',
    'healthyaa_checkout_refresh_delivery_fee_amount', 'healthyaa_checkout_refresh_validate_order_delivery_fee',
    'healthyaa_checkout_refresh_order_delivery_fee_amount', 'healthyaa_checkout_refresh_is_delivery_fee',
    'healthyaa_checkout_refresh_delivery_fee_labels', 'healthyaa_checkout_refresh_replace_delivery_option_handlers'
]);
load_functions($root . '/public_html/wp-content/themes/oceanwp/functions.php', [
    'healthyaa_validate_consent_checkbox', 'healthyaa_save_consent_checkbox', 'validate_appointment_date_field'
]);
require $root . '/public_html/wp-content/plugins/wc-thanks-redirect/src/Modules/SandBoxPayment.php';
$results = [];
function check($name, $condition) {
    $GLOBALS['results'][$name] = (bool)$condition;
    if (!$condition) throw new RuntimeException('Unexpected probe outcome: ' . $name);
}
$_SERVER = ['REMOTE_ADDR'=>'192.0.2.10', 'HTTP_USER_AGENT'=>'synthetic-A'];
$GLOBALS['transients'] = [];
for ($i=0; $i<20; $i++) check('rate_initial_requests_accepted', healthyaa_analytics_rate_limit_ok('cart',20));
check('rate_same_agent_blocked_at_cap', !healthyaa_analytics_rate_limit_ok('cart',20));
$_SERVER['HTTP_USER_AGENT'] = 'synthetic-B';
check('finding_rate_cap_reset_by_user_agent', healthyaa_analytics_rate_limit_ok('cart',20));
$_SERVER['HTTP_X_FORWARDED_FOR'] = '198.51.100.99';
check('untrusted_forwarded_ip_ignored', healthyaa_analytics_ip_address() === '192.0.2.10');
$wpdb = new SyntheticDatabase();
$id = healthyaa_analytics_find_cart_activity_row('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa','bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb','synthetic-victim-email-hash','same-public-cart');
check('finding_other_session_selects_existing_email_cart', $id === 321 && count($wpdb->queries) === 1 && !str_contains($wpdb->queries[0][0], 'visitor_id'));
check('different_nonempty_cart_not_merged', healthyaa_analytics_find_cart_activity_row('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa','bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb','synthetic-victim-email-hash','different-cart') === 0);
check('missing_analytics_api_token_denied', healthyaa_analytics_rest_permission(new WP_REST_Request()) instanceof WP_Error);
check('wrong_analytics_api_token_denied', healthyaa_analytics_rest_permission(new WP_REST_Request(['authorization'=>'Bearer wrong'])) instanceof WP_Error);
check('correct_analytics_header_token_accepted', healthyaa_analytics_rest_permission(new WP_REST_Request(['authorization'=>'Bearer synthetic-secret'])) === true);
check('query_string_token_also_accepted', healthyaa_analytics_rest_permission(new WP_REST_Request([], ['token'=>'synthetic-secret'])) === true);
check('invalid_delivery_option_rejected', healthyaa_checkout_refresh_sanitize_delivery_option('free') === '');
check('array_delivery_option_rejected', healthyaa_checkout_refresh_sanitize_delivery_option(['to_clinic']) === '');
check('valid_delivery_option_accepted', healthyaa_checkout_refresh_sanitize_delivery_option('to_clinic') === 'to_clinic');
$order = new class { public function get_meta($key,$single) { return $key === 'Delivery Option' ? 'to_clinic' : ''; } public function get_items($type) { return []; } };
$error = new WP_Error(); healthyaa_checkout_refresh_validate_order_delivery_fee($order,$error);
check('missing_required_fee_rejected', isset($error->errors['healthyaa_delivery_fee_mismatch']));
healthyaa_checkout_refresh_replace_delivery_option_handlers();
check('legacy_anonymous_delivery_handlers_removed', in_array(['wp_ajax_nopriv_update_delivery_option','update_delivery_option'],$GLOBALS['removed'],true) && in_array(['wp_ajax_nopriv_update_delivery_fee','update_delivery_fee'],$GLOBALS['removed'],true));
$gateway = (new ReflectionClass('NeeBPlugins\\Wctr\\Modules\\SandBoxPayment'))->newInstanceWithoutConstructor();
$gateway->id='sandboxpaymentgateway-wctr'; $GLOBALS['admin']=false;
check('sandbox_gateway_removed_for_nonadmin', !isset($gateway->restrict_to_admins([$gateway->id=>$gateway])[$gateway->id]));
$GLOBALS['admin']=true;
check('sandbox_gateway_retained_for_admin', isset($gateway->restrict_to_admins([$gateway->id=>$gateway])[$gateway->id]));
$_POST=['healthyaa_consent'=>'0']; $GLOBALS['notices']=[];
healthyaa_validate_consent_checkbox(); healthyaa_save_consent_checkbox(1);
check('finding_false_consent_accepted_and_saved_no', !$GLOBALS['notices'] && $GLOBALS['saved']['healthyaa_consent']==='No');
$_POST=[]; $GLOBALS['notices']=[]; healthyaa_validate_consent_checkbox();
check('missing_consent_rejected', count($GLOBALS['notices'])===1);
$_POST=['appointment_date'=>'not-a-date']; $GLOBALS['notices']=[]; validate_appointment_date_field();
check('finding_invalid_nonempty_date_accepted', !$GLOBALS['notices']);
$_POST=['appointment_date'=>'']; $GLOBALS['notices']=[]; validate_appointment_date_field();
check('empty_date_rejected', count($GLOBALS['notices'])===1);
echo json_encode(['mode'=>'isolated actual functions with synthetic stubs; true means expected observation reproduced, including weaknesses','checks'=>$results,'checks_count'=>count($results),'all_expected_observations_reproduced'=>!in_array(false,$results,true),'network_database_mail_order_operations'=>false], JSON_PRETTY_PRINT), "\n";
