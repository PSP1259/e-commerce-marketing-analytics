# 03 – GA4 Setup

For siete.ch, I use a dedicated GA4 property with Enhanced Measurement enabled for core behavioral events.  
The e-commerce funnel events are pushed by WooCommerce via the GTM4WP plugin into the dataLayer and forwarded through GTM.

## Event Architecture

### Group A – Automatic Standard Events

- page_view
- scroll
- click (generic interactions)
- session_start

### Group B – E-commerce Funnel Events  
Transferred 1:1 from WooCommerce dataLayer to GA4

- view_item_list
- view_item
- select_item
- add_to_cart
- remove_from_cart
- view_cart
- begin_checkout
- add_shipping_info
- add_payment_info
- purchase

### Group C – Custom Interaction Events

To capture important UI interactions that are not covered by WooCommerce’s default dataLayer events:

| Event name | Description | Parameters |
|-----------|-------------|------------|
| hero_cta_click | Hero CTA interaction | section, link_text, link_url |
| header_nav_click | Header navigation link click | section, link_text, link_url |
| footer_link_click | Footer link click | section, link_text, link_url |
| sureforms_submit | Contact form submission | form_name, page_path |
