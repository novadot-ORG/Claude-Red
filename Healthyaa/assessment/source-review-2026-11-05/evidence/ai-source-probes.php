<?php
// Source-only synthetic probes. No WordPress bootstrap, database or network.
// Run: php ai-source-probes.php /path/to/healthyaa-wordpress
$root=$argv[1]??getcwd();
define('ABSPATH', '/synthetic/');
define('MINUTE_IN_SECONDS', 60);
function wp_strip_all_tags($v) { return strip_tags((string)$v); }
function strip_shortcodes($v) { return $v; }
function wp_unslash($v) { return $v; }
function sanitize_text_field($v) { return trim(strip_tags((string)$v)); }
function sanitize_email($v) { return filter_var($v,FILTER_SANITIZE_EMAIL); }
function is_email($v) { return filter_var($v,FILTER_VALIDATE_EMAIL); }
function wp_parse_args($v,$d) { return array_merge($d,$v); }
function get_option($key,$default=[]) { return $key==='healthyaa_ai_assistant_settings' ? ['lead_capture_enabled'=>0,'notification_email'=>'recipient@example.test'] : $default; }
function get_the_title($p) { return 'Synthetic protected page'; }
function get_permalink($p) { return 'https://example.test/item'; }
function get_the_excerpt($p) { return ''; }
function apply_filters($tag,$v) { return $v; }
function get_post_meta($id,$key,$single) { return ''; }
function get_post_field($key,$id) { return ''; }
function get_the_terms($id,$tax) { return []; }
function wc_price($n) { return (string)$n; }
function wp_trim_words($v,$n,$suffix='...') { return implode(' ',array_slice(explode(' ',$v),0,$n)); }
function wc_get_product($id) { return $id===4242 ? new WC_Product() : null; }
function wp_reset_postdata() {}
function current_time($format) { return '2026-11-05 00:00:00'; }
function esc_url_raw($v) { return $v; }
$GLOBALS['mail_calls']=0;
function wp_mail($to,$subject,$body) { $GLOBALS['mail_calls']++; return true; }
class WP_Query { public $posts=[]; public function __construct($args) {} }
class WP_Post { public $ID=3131; public $post_type='page'; public $post_status='publish'; public $post_password='synthetic-password'; public $post_content='SYNTHETIC_PASSWORD_PROTECTED_CONTENT'; public $post_modified_gmt='2026-11-05 00:00:00'; }
class WC_Product {
 public function get_id(){return 4242;} public function get_status(){return 'private';} public function is_visible(){return false;}
 public function get_name(){return 'SYNTHETIC_PRIVATE_ITEM';} public function get_slug(){return 'synthetic-private-item';}
 public function get_price(){return '123';} public function get_regular_price(){return '123';} public function get_price_html(){return '123';}
 public function get_short_description(){return 'SYNTHETIC_PRIVATE_DESCRIPTION';}
}
require $root.'/public_html/wp-content/plugins/healthyaa-ai-assistant/includes/class-healthyaa-ai-assistant.php';
require $root.'/public_html/wp-content/plugins/healthyaa-ai-assistant/includes/class-healthyaa-ai-knowledge-base.php';
function invoke_private($class,$method,...$args) { $r=new ReflectionMethod($class,$method); return $r->invoke(null,...$args); }
$rules=new ReflectionProperty('Healthyaa_AI_Assistant','topic_rules'); $rules->setValue(null,[]);
$suggestions=invoke_private('Healthyaa_AI_Assistant','build_suggested_products','zzsynthetic',['product_id'=>4242]);
$protected=invoke_private('Healthyaa_AI_Knowledge_Base','build_source_from_post',new WP_Post());
$session=invoke_private('Healthyaa_AI_Assistant','normalize_session_state',[]);
$lead=invoke_private('Healthyaa_AI_Assistant','process_lead_event','synthetic-session',$session,['action'=>'submit','stage'=>'email','email'=>'visitor@example.test','name'=>''],[]);
$result=[
 'probe_type'=>'isolated actual methods with synthetic WordPress/WooCommerce stubs; not a live endpoint test',
 'private_product_returned'=>count($suggestions)===1 && $suggestions[0]['name']==='SYNTHETIC_PRIVATE_ITEM' && $suggestions[0]['summary']==='SYNTHETIC_PRIVATE_DESCRIPTION',
 'password_protected_content_indexed'=>str_contains($protected['content']??'','SYNTHETIC_PASSWORD_PROTECTED_CONTENT'),
 'lead_capture_disabled_but_captured'=>($lead['session']['lead_status']??'')==='captured',
 'mock_mail_calls_when_disabled'=>$GLOBALS['mail_calls'],
 'actual_mail_sent'=>false
];
echo json_encode($result,JSON_PRETTY_PRINT),"\n";
exit($result['private_product_returned'] && $result['password_protected_content_indexed'] && $result['lead_capture_disabled_but_captured'] && $result['mock_mail_calls_when_disabled']===1 ? 0 : 1);
