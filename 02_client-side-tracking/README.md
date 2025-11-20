# 02 – Client-side Tracking

For the siete.ch shop, I implemented a minimal and fully client-side tracking setup.

Technologies used:

- Google Tag Manager (Web)
- Google Analytics 4
- GTM4WP plugin to provide WooCommerce e-commerce event data

Objectives:

- Measure the full e-commerce funnel from product view to purchase
- Track key navigation interactions
- Track form submissions (currently contact, newsletter planned)
- Ensure no personally identifiable information is sent to GA4

## Event Setup

I currently work with two event groups:

### 1. Standard GA4 E-commerce Events  
(provided automatically by GTM4WP)

These events are pushed into the WooCommerce dataLayer and captured in GTM:

- view_item_list
- view_item
- select_item
- add_to_cart
- remove_from_cart
- view_cart
- begin_checkout
- add_payment_info
- add_shipping_info
- purchase

Trigger type: Custom Event  
Trigger pattern: Regex match on `_event`  
Event name mapping: uses `{{Event}}` directly

### 2. Custom Interaction Events

| Event name | Purpose | Trigger logic | Parameters |
|------------|---------|---------------|------------|
| hero_cta_click | Hero CTA click | CSS selector: `a.uagb-infobox-cta-link[...]` | `link_text`, `link_url`, `section="hero"` |
| header_nav_click | Header navigation | `header a.menu-link` | `link_text`, `link_url`, `section="header"` |
| footer_link_click | Footer navigation | `footer a[href]` | `link_text`, `link_url`, `section="footer"` |
| sureforms_submit | Contact form submit | `button.srfm-submit-button` | `form_name="contact"`, `page_path` |

The GA4 configuration tag handles all event dispatching through the central Google tag setup.

## Trigger Setup

| Trigger name | Type | Condition | Used for |
|-------------|------|-----------|----------|
| hero_cta_click | Click – All Elements | `a.uagb-infobox-cta-link[href*="/shop"]` | Hero CTA “Shop now” |
| header_nav_click | Click – All Elements | `header a.menu-link` | Main navigation |
| footer_link_click | Click – All Elements | `footer a[href]` | Footer links |
| contact_submit | Click – All Elements | `button.srfm-submit-button` | Contact form submission |
| Event – Ecommerce Events | Custom Event | Regex: `view_item|view_item_list|select_item|add_to_cart|remove_from_cart|view_cart|begin_checkout|add_payment_info|add_shipping_info|purchase` | WooCommerce e-commerce events |

Design principles:

- Minimal number of triggers
- Zero overlap or double-tagging
- Triggers represent **real UX interactions**

Debug approach:

- GTM Preview Mode
- Inspect `Click Element` match
- Network tab → `collect` hits
- GA4 Realtime → parameter validation

## Consent & Privacy

- Consent checks enabled through Google Tag
- No email, names, address data
- Sensitive dataLayer values from WooCommerce are excluded

## Debugging & QA

Primary verification methods:

- GA4 Debug Mode (GTM Preview)
- Browser DevTools → dataLayer inspection
- GA4 Realtime monitoring

Event documentation and parameters:
→ see `/03_ga4-setup/`
