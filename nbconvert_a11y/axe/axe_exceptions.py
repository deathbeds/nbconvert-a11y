"""axe types generated from scripts/generate_axe_exceptions.py for axe-core version v4.8.1
"""

from .base_axe_exceptions import *




class ACT(AxeException): ...

class EN_301_549(AxeException): ...

class EN_9_1_1_1(AxeException): ...

class EN_9_1_2_1(AxeException): ...

class EN_9_1_2_2(AxeException): ...

class EN_9_1_3_1(AxeException): ...

class EN_9_1_3_4(AxeException): ...

class EN_9_1_3_5(AxeException): ...

class EN_9_1_4_1(AxeException): ...

class EN_9_1_4_12(AxeException): ...

class EN_9_1_4_2(AxeException): ...

class EN_9_1_4_3(AxeException): ...

class EN_9_1_4_4(AxeException): ...

class EN_9_2_1_1(AxeException): ...

class EN_9_2_1_3(AxeException): ...

class EN_9_2_2_1(AxeException): ...

class EN_9_2_2_2(AxeException): ...

class EN_9_2_4_1(AxeException): ...

class EN_9_2_4_2(AxeException): ...

class EN_9_2_4_4(AxeException): ...

class EN_9_2_5_3(AxeException): ...

class EN_9_3_1_1(AxeException): ...

class EN_9_3_1_2(AxeException): ...

class EN_9_3_3_2(AxeException): ...

class EN_9_4_1_2(AxeException): ...

class TT11_a(AxeException): ...

class TT11_b(AxeException): ...

class TT12_a(AxeException): ...

class TT12_d(AxeException): ...

class TT13_a(AxeException): ...

class TT13_c(AxeException): ...

class TT14_b(AxeException): ...

class TT17_a(AxeException): ...

class TT2_a(AxeException): ...

class TT2_b(AxeException): ...

class TT4_a(AxeException): ...

class TT5_c(AxeException): ...

class TT6_a(AxeException): ...

class TT7_a(AxeException): ...

class TT7_b(AxeException): ...

class TT8_a(AxeException): ...

class TT9_a(AxeException): ...

class TTv5(AxeException): ...

class best_practice(AxeException): ...

class cat:

    class aria(AxeException): ...

    class color(AxeException): ...

    class forms(AxeException): ...

    class keyboard(AxeException): ...

    class language(AxeException): ...

    class name_role_value(AxeException): ...

    class parsing(AxeException): ...

    class semantics(AxeException): ...

    class sensory_and_visual_cues(AxeException): ...

    class structure(AxeException): ...

    class tables(AxeException): ...

    class text_alternatives(AxeException): ...

    class time_and_media(AxeException): ...

class deprecated(AxeException): ...

class experimental(AxeException): ...

class review_item(AxeException): ...

class section508(AxeException): ...

class section508_22_a(AxeException): ...

class section508_22_f(AxeException): ...

class section508_22_g(AxeException): ...

class section508_22_i(AxeException): ...

class section508_22_j(AxeException): ...

class section508_22_n(AxeException): ...

class section508_22_o(AxeException): ...

class wcag111(AxeException): ...

class wcag121(AxeException): ...

class wcag122(AxeException): ...

class wcag131(AxeException): ...

class wcag134(AxeException): ...

class wcag135(AxeException): ...

class wcag141(AxeException): ...

class wcag1412(AxeException): ...

class wcag142(AxeException): ...

class wcag143(AxeException): ...

class wcag144(AxeException): ...

class wcag146(AxeException): ...

class wcag211(AxeException): ...

class wcag213(AxeException): ...

class wcag21a(AxeException): ...

class wcag21aa(AxeException): ...

class wcag221(AxeException): ...

class wcag222(AxeException): ...

class wcag224(AxeException): ...

class wcag22aa(AxeException): ...

class wcag241(AxeException): ...

class wcag242(AxeException): ...

class wcag244(AxeException): ...

class wcag249(AxeException): ...

class wcag253(AxeException): ...

class wcag258(AxeException): ...

class wcag2a(AxeException): ...

class wcag2a_obsolete(AxeException): ...

class wcag2aa(AxeException): ...

class wcag2aaa(AxeException): ...

class wcag311(AxeException): ...

class wcag312(AxeException): ...

class wcag325(AxeException): ...

class wcag332(AxeException): ...

class wcag411(AxeException): ...

class wcag412(AxeException): ...



class accesskeys(cat.keyboard, best_practice, ruleId="accesskeys"):
    """Ensures every accesskey attribute value is unique
    
accesskey attribute value should be unique

https://dequeuniversity.com/rules/axe/4.9/accesskeys?application=axeAPI"""
    


class area_alt(cat.text_alternatives, wcag2a, wcag244, wcag412, section508, section508_22_a, TTv5, TT6_a, EN_301_549, EN_9_2_4_4, EN_9_4_1_2, ACT, ruleId="area-alt"):
    """Ensures <area> elements of image maps have alternate text
    
Active <area> elements must have alternate text

https://dequeuniversity.com/rules/axe/4.9/area-alt?application=axeAPI"""
    


class aria_allowed_attr(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-allowed-attr"):
    """Ensures an element's role supports its ARIA attributes
    
Elements must only use supported ARIA attributes

https://dequeuniversity.com/rules/axe/4.9/aria-allowed-attr?application=axeAPI"""
    


class aria_allowed_role(cat.aria, best_practice, ruleId="aria-allowed-role"):
    """Ensures role attribute has an appropriate value for the element
    
ARIA role should be appropriate for the element

https://dequeuniversity.com/rules/axe/4.9/aria-allowed-role?application=axeAPI"""
    


class aria_braille_equivalent(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-braille-equivalent"):
    """Ensure aria-braillelabel and aria-brailleroledescription have a non-braille equivalent
    
aria-braille attributes must have a non-braille equivalent

https://dequeuniversity.com/rules/axe/4.9/aria-braille-equivalent?application=axeAPI"""
    


class aria_command_name(cat.aria, wcag2a, wcag412, TTv5, TT6_a, EN_301_549, EN_9_4_1_2, ACT, ruleId="aria-command-name"):
    """Ensures every ARIA button, link and menuitem has an accessible name
    
ARIA commands must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-command-name?application=axeAPI"""
    


class aria_conditional_attr(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-conditional-attr"):
    """Ensures ARIA attributes are used as described in the specification of the element's role
    
ARIA attributes must be used as specified for the element's role

https://dequeuniversity.com/rules/axe/4.9/aria-conditional-attr?application=axeAPI"""
    


class aria_deprecated_role(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-deprecated-role"):
    """Ensures elements do not use deprecated roles
    
Deprecated ARIA roles must not be used

https://dequeuniversity.com/rules/axe/4.9/aria-deprecated-role?application=axeAPI"""
    


class aria_dialog_name(cat.aria, best_practice, ruleId="aria-dialog-name"):
    """Ensures every ARIA dialog and alertdialog node has an accessible name
    
ARIA dialog and alertdialog nodes should have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-dialog-name?application=axeAPI"""
    


class aria_hidden_body(cat.aria, wcag2a, wcag131, wcag412, EN_301_549, EN_9_1_3_1, EN_9_4_1_2, ruleId="aria-hidden-body"):
    """Ensures aria-hidden="true" is not present on the document body.
    
aria-hidden="true" must not be present on the document body

https://dequeuniversity.com/rules/axe/4.9/aria-hidden-body?application=axeAPI"""
    


class aria_hidden_focus(cat.name_role_value, wcag2a, wcag412, TTv5, TT6_a, EN_301_549, EN_9_4_1_2, ruleId="aria-hidden-focus"):
    """Ensures aria-hidden elements are not focusable nor contain focusable elements
    
ARIA hidden element must not be focusable or contain focusable elements

https://dequeuniversity.com/rules/axe/4.9/aria-hidden-focus?application=axeAPI"""
    


class aria_input_field_name(cat.aria, wcag2a, wcag412, TTv5, TT5_c, EN_301_549, EN_9_4_1_2, ACT, ruleId="aria-input-field-name"):
    """Ensures every ARIA input field has an accessible name
    
ARIA input fields must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-input-field-name?application=axeAPI"""
    


class aria_meter_name(cat.aria, wcag2a, wcag111, EN_301_549, EN_9_1_1_1, ruleId="aria-meter-name"):
    """Ensures every ARIA meter node has an accessible name
    
ARIA meter nodes must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-meter-name?application=axeAPI"""
    


class aria_progressbar_name(cat.aria, wcag2a, wcag111, EN_301_549, EN_9_1_1_1, ruleId="aria-progressbar-name"):
    """Ensures every ARIA progressbar node has an accessible name
    
ARIA progressbar nodes must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-progressbar-name?application=axeAPI"""
    


class aria_prohibited_attr(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-prohibited-attr"):
    """Ensures ARIA attributes are not prohibited for an element's role
    
Elements must only use permitted ARIA attributes

https://dequeuniversity.com/rules/axe/4.9/aria-prohibited-attr?application=axeAPI"""
    


class aria_required_attr(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-required-attr"):
    """Ensures elements with ARIA roles have all required ARIA attributes
    
Required ARIA attributes must be provided

https://dequeuniversity.com/rules/axe/4.9/aria-required-attr?application=axeAPI"""
    


class aria_required_children(cat.aria, wcag2a, wcag131, EN_301_549, EN_9_1_3_1, ruleId="aria-required-children"):
    """Ensures elements with an ARIA role that require child roles contain them
    
Certain ARIA roles must contain particular children

https://dequeuniversity.com/rules/axe/4.9/aria-required-children?application=axeAPI"""
    


class aria_required_parent(cat.aria, wcag2a, wcag131, EN_301_549, EN_9_1_3_1, ruleId="aria-required-parent"):
    """Ensures elements with an ARIA role that require parent roles are contained by them
    
Certain ARIA roles must be contained by particular parents

https://dequeuniversity.com/rules/axe/4.9/aria-required-parent?application=axeAPI"""
    


class aria_roledescription(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, deprecated, ruleId="aria-roledescription"):
    """Ensure aria-roledescription is only used on elements with an implicit or explicit role
    
aria-roledescription must be on elements with a semantic role

https://dequeuniversity.com/rules/axe/4.9/aria-roledescription?application=axeAPI"""
    


class aria_roles(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-roles"):
    """Ensures all elements with a role attribute use a valid value
    
ARIA roles used must conform to valid values

https://dequeuniversity.com/rules/axe/4.9/aria-roles?application=axeAPI"""
    


class aria_text(cat.aria, best_practice, ruleId="aria-text"):
    """Ensures role="text" is used on elements with no focusable descendants
    
"role=text" should have no focusable descendants

https://dequeuniversity.com/rules/axe/4.9/aria-text?application=axeAPI"""
    


class aria_toggle_field_name(cat.aria, wcag2a, wcag412, TTv5, TT5_c, EN_301_549, EN_9_4_1_2, ACT, ruleId="aria-toggle-field-name"):
    """Ensures every ARIA toggle field has an accessible name
    
ARIA toggle fields must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-toggle-field-name?application=axeAPI"""
    


class aria_tooltip_name(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-tooltip-name"):
    """Ensures every ARIA tooltip node has an accessible name
    
ARIA tooltip nodes must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-tooltip-name?application=axeAPI"""
    


class aria_treeitem_name(cat.aria, best_practice, ruleId="aria-treeitem-name"):
    """Ensures every ARIA treeitem node has an accessible name
    
ARIA treeitem nodes should have an accessible name

https://dequeuniversity.com/rules/axe/4.9/aria-treeitem-name?application=axeAPI"""
    


class aria_valid_attr_value(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-valid-attr-value"):
    """Ensures all ARIA attributes have valid values
    
ARIA attributes must conform to valid values

https://dequeuniversity.com/rules/axe/4.9/aria-valid-attr-value?application=axeAPI"""
    


class aria_valid_attr(cat.aria, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="aria-valid-attr"):
    """Ensures attributes that begin with aria- are valid ARIA attributes
    
ARIA attributes must conform to valid names

https://dequeuniversity.com/rules/axe/4.9/aria-valid-attr?application=axeAPI"""
    


class audio_caption(cat.time_and_media, wcag2a, wcag121, EN_301_549, EN_9_1_2_1, section508, section508_22_a, deprecated, ruleId="audio-caption"):
    """Ensures <audio> elements have captions
    
<audio> elements must have a captions track

https://dequeuniversity.com/rules/axe/4.9/audio-caption?application=axeAPI"""
    


class autocomplete_valid(cat.forms, wcag21aa, wcag135, EN_301_549, EN_9_1_3_5, ACT, ruleId="autocomplete-valid"):
    """Ensure the autocomplete attribute is correct and suitable for the form field
    
autocomplete attribute must be used correctly

https://dequeuniversity.com/rules/axe/4.9/autocomplete-valid?application=axeAPI"""
    


class avoid_inline_spacing(cat.structure, wcag21aa, wcag1412, EN_301_549, EN_9_1_4_12, ACT, ruleId="avoid-inline-spacing"):
    """Ensure that text spacing set through style attributes can be adjusted with custom stylesheets
    
Inline text spacing must be adjustable with custom stylesheets

https://dequeuniversity.com/rules/axe/4.9/avoid-inline-spacing?application=axeAPI"""
    


class blink(cat.time_and_media, wcag2a, wcag222, section508, section508_22_j, TTv5, TT2_b, EN_301_549, EN_9_2_2_2, ruleId="blink"):
    """Ensures <blink> elements are not used
    
<blink> elements are deprecated and must not be used

https://dequeuniversity.com/rules/axe/4.9/blink?application=axeAPI"""
    


class button_name(cat.name_role_value, wcag2a, wcag412, section508, section508_22_a, TTv5, TT6_a, EN_301_549, EN_9_4_1_2, ACT, ruleId="button-name"):
    """Ensures buttons have discernible text
    
Buttons must have discernible text

https://dequeuniversity.com/rules/axe/4.9/button-name?application=axeAPI"""
    


class bypass(cat.keyboard, wcag2a, wcag241, section508, section508_22_o, TTv5, TT9_a, EN_301_549, EN_9_2_4_1, ruleId="bypass"):
    """Ensures each page has at least one mechanism for a user to bypass navigation and jump straight to the content
    
Page must have means to bypass repeated blocks

https://dequeuniversity.com/rules/axe/4.9/bypass?application=axeAPI"""
    


class color_contrast_enhanced(cat.color, wcag2aaa, wcag146, ACT, ruleId="color-contrast-enhanced"):
    """Ensures the contrast between foreground and background colors meets WCAG 2 AAA enhanced contrast ratio thresholds
    
Elements must meet enhanced color contrast ratio thresholds

https://dequeuniversity.com/rules/axe/4.9/color-contrast-enhanced?application=axeAPI"""
    


class color_contrast(cat.color, wcag2aa, wcag143, TTv5, TT13_c, EN_301_549, EN_9_1_4_3, ACT, ruleId="color-contrast"):
    """Ensures the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds
    
Elements must meet minimum color contrast ratio thresholds

https://dequeuniversity.com/rules/axe/4.9/color-contrast?application=axeAPI"""
    


class css_orientation_lock(cat.structure, wcag134, wcag21aa, EN_301_549, EN_9_1_3_4, experimental, ruleId="css-orientation-lock"):
    """Ensures content is not locked to any specific display orientation, and the content is operable in all display orientations
    
CSS Media queries must not lock display orientation

https://dequeuniversity.com/rules/axe/4.9/css-orientation-lock?application=axeAPI"""
    


class definition_list(cat.structure, wcag2a, wcag131, EN_301_549, EN_9_1_3_1, ruleId="definition-list"):
    """Ensures <dl> elements are structured correctly
    
<dl> elements must only directly contain properly-ordered <dt> and <dd> groups, <script>, <template> or <div> elements

https://dequeuniversity.com/rules/axe/4.9/definition-list?application=axeAPI"""
    


class dlitem(cat.structure, wcag2a, wcag131, EN_301_549, EN_9_1_3_1, ruleId="dlitem"):
    """Ensures <dt> and <dd> elements are contained by a <dl>
    
<dt> and <dd> elements must be contained by a <dl>

https://dequeuniversity.com/rules/axe/4.9/dlitem?application=axeAPI"""
    


class document_title(cat.text_alternatives, wcag2a, wcag242, TTv5, TT12_a, EN_301_549, EN_9_2_4_2, ACT, ruleId="document-title"):
    """Ensures each HTML document contains a non-empty <title> element
    
Documents must have <title> element to aid in navigation

https://dequeuniversity.com/rules/axe/4.9/document-title?application=axeAPI"""
    


class duplicate_id_active(cat.parsing, wcag2a_obsolete, wcag411, deprecated, ruleId="duplicate-id-active"):
    """Ensures every id attribute value of active elements is unique
    
IDs of active elements must be unique

https://dequeuniversity.com/rules/axe/4.9/duplicate-id-active?application=axeAPI"""
    


class duplicate_id_aria(cat.parsing, wcag2a, wcag412, EN_301_549, EN_9_4_1_2, ruleId="duplicate-id-aria"):
    """Ensures every id attribute value used in ARIA and in labels is unique
    
IDs used in ARIA and labels must be unique

https://dequeuniversity.com/rules/axe/4.9/duplicate-id-aria?application=axeAPI"""
    


class duplicate_id(cat.parsing, wcag2a_obsolete, wcag411, deprecated, ruleId="duplicate-id"):
    """Ensures every id attribute value is unique
    
id attribute value must be unique

https://dequeuniversity.com/rules/axe/4.9/duplicate-id?application=axeAPI"""
    


class empty_heading(cat.name_role_value, best_practice, ruleId="empty-heading"):
    """Ensures headings have discernible text
    
Headings should not be empty

https://dequeuniversity.com/rules/axe/4.9/empty-heading?application=axeAPI"""
    


class empty_table_header(cat.name_role_value, best_practice, ruleId="empty-table-header"):
    """Ensures table headers have discernible text
    
Table header text should not be empty

https://dequeuniversity.com/rules/axe/4.9/empty-table-header?application=axeAPI"""
    


class focus_order_semantics(cat.keyboard, best_practice, experimental, ruleId="focus-order-semantics"):
    """Ensures elements in the focus order have a role appropriate for interactive content
    
Elements in the focus order should have an appropriate role

https://dequeuniversity.com/rules/axe/4.9/focus-order-semantics?application=axeAPI"""
    


class form_field_multiple_labels(cat.forms, wcag2a, wcag332, TTv5, TT5_c, EN_301_549, EN_9_3_3_2, ruleId="form-field-multiple-labels"):
    """Ensures form field does not have multiple label elements
    
Form field must not have multiple label elements

https://dequeuniversity.com/rules/axe/4.9/form-field-multiple-labels?application=axeAPI"""
    


class frame_focusable_content(cat.keyboard, wcag2a, wcag211, TTv5, TT4_a, EN_301_549, EN_9_2_1_1, ruleId="frame-focusable-content"):
    """Ensures <frame> and <iframe> elements with focusable content do not have tabindex=-1
    
Frames with focusable content must not have tabindex=-1

https://dequeuniversity.com/rules/axe/4.9/frame-focusable-content?application=axeAPI"""
    


class frame_tested(cat.structure, best_practice, review_item, ruleId="frame-tested"):
    """Ensures <iframe> and <frame> elements contain the axe-core script
    
Frames should be tested with axe-core

https://dequeuniversity.com/rules/axe/4.9/frame-tested?application=axeAPI"""
    


class frame_title_unique(cat.text_alternatives, wcag2a, wcag412, TTv5, TT12_d, EN_301_549, EN_9_4_1_2, ruleId="frame-title-unique"):
    """Ensures <iframe> and <frame> elements contain a unique title attribute
    
Frames must have a unique title attribute

https://dequeuniversity.com/rules/axe/4.9/frame-title-unique?application=axeAPI"""
    


class frame_title(cat.text_alternatives, wcag2a, wcag412, section508, section508_22_i, TTv5, TT12_d, EN_301_549, EN_9_4_1_2, ruleId="frame-title"):
    """Ensures <iframe> and <frame> elements have an accessible name
    
Frames must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/frame-title?application=axeAPI"""
    


class heading_order(cat.semantics, best_practice, ruleId="heading-order"):
    """Ensures the order of headings is semantically correct
    
Heading levels should only increase by one

https://dequeuniversity.com/rules/axe/4.9/heading-order?application=axeAPI"""
    


class hidden_content(cat.structure, best_practice, experimental, review_item, ruleId="hidden-content"):
    """Informs users about hidden content.
    
Hidden content on the page should be analyzed

https://dequeuniversity.com/rules/axe/4.9/hidden-content?application=axeAPI"""
    


class html_has_lang(cat.language, wcag2a, wcag311, TTv5, TT11_a, EN_301_549, EN_9_3_1_1, ACT, ruleId="html-has-lang"):
    """Ensures every HTML document has a lang attribute
    
<html> element must have a lang attribute

https://dequeuniversity.com/rules/axe/4.9/html-has-lang?application=axeAPI"""
    


class html_lang_valid(cat.language, wcag2a, wcag311, TTv5, TT11_a, EN_301_549, EN_9_3_1_1, ACT, ruleId="html-lang-valid"):
    """Ensures the lang attribute of the <html> element has a valid value
    
<html> element must have a valid value for the lang attribute

https://dequeuniversity.com/rules/axe/4.9/html-lang-valid?application=axeAPI"""
    


class html_xml_lang_mismatch(cat.language, wcag2a, wcag311, EN_301_549, EN_9_3_1_1, ACT, ruleId="html-xml-lang-mismatch"):
    """Ensure that HTML elements with both valid lang and xml:lang attributes agree on the base language of the page
    
HTML elements with lang and xml:lang must have the same base language

https://dequeuniversity.com/rules/axe/4.9/html-xml-lang-mismatch?application=axeAPI"""
    


class identical_links_same_purpose(cat.semantics, wcag2aaa, wcag249, ruleId="identical-links-same-purpose"):
    """Ensure that links with the same accessible name serve a similar purpose
    
Links with the same name must have a similar purpose

https://dequeuniversity.com/rules/axe/4.9/identical-links-same-purpose?application=axeAPI"""
    


class image_alt(cat.text_alternatives, wcag2a, wcag111, section508, section508_22_a, TTv5, TT7_a, TT7_b, EN_301_549, EN_9_1_1_1, ACT, ruleId="image-alt"):
    """Ensures <img> elements have alternate text or a role of none or presentation
    
Images must have alternate text

https://dequeuniversity.com/rules/axe/4.9/image-alt?application=axeAPI"""
    


class image_redundant_alt(cat.text_alternatives, best_practice, ruleId="image-redundant-alt"):
    """Ensure image alternative is not repeated as text
    
Alternative text of images should not be repeated as text

https://dequeuniversity.com/rules/axe/4.9/image-redundant-alt?application=axeAPI"""
    


class input_button_name(cat.name_role_value, wcag2a, wcag412, section508, section508_22_a, TTv5, TT5_c, EN_301_549, EN_9_4_1_2, ACT, ruleId="input-button-name"):
    """Ensures input buttons have discernible text
    
Input buttons must have discernible text

https://dequeuniversity.com/rules/axe/4.9/input-button-name?application=axeAPI"""
    


class input_image_alt(cat.text_alternatives, wcag2a, wcag111, wcag412, section508, section508_22_a, TTv5, TT7_a, EN_301_549, EN_9_1_1_1, EN_9_4_1_2, ACT, ruleId="input-image-alt"):
    """Ensures <input type="image"> elements have alternate text
    
Image buttons must have alternate text

https://dequeuniversity.com/rules/axe/4.9/input-image-alt?application=axeAPI"""
    


class label_content_name_mismatch(cat.semantics, wcag21a, wcag253, EN_301_549, EN_9_2_5_3, experimental, ruleId="label-content-name-mismatch"):
    """Ensures that elements labelled through their content must have their visible text as part of their accessible name
    
Elements must have their visible text as part of their accessible name

https://dequeuniversity.com/rules/axe/4.9/label-content-name-mismatch?application=axeAPI"""
    


class label_title_only(cat.forms, best_practice, ruleId="label-title-only"):
    """Ensures that every form element has a visible label and is not solely labeled using hidden labels, or the title or aria-describedby attributes
    
Form elements should have a visible label

https://dequeuniversity.com/rules/axe/4.9/label-title-only?application=axeAPI"""
    


class label(cat.forms, wcag2a, wcag412, section508, section508_22_n, TTv5, TT5_c, EN_301_549, EN_9_4_1_2, ACT, ruleId="label"):
    """Ensures every form element has a label
    
Form elements must have labels

https://dequeuniversity.com/rules/axe/4.9/label?application=axeAPI"""
    


class landmark_banner_is_top_level(cat.semantics, best_practice, ruleId="landmark-banner-is-top-level"):
    """Ensures the banner landmark is at top level
    
Banner landmark should not be contained in another landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-banner-is-top-level?application=axeAPI"""
    


class landmark_complementary_is_top_level(cat.semantics, best_practice, ruleId="landmark-complementary-is-top-level"):
    """Ensures the complementary landmark or aside is at top level
    
Aside should not be contained in another landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-complementary-is-top-level?application=axeAPI"""
    


class landmark_contentinfo_is_top_level(cat.semantics, best_practice, ruleId="landmark-contentinfo-is-top-level"):
    """Ensures the contentinfo landmark is at top level
    
Contentinfo landmark should not be contained in another landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-contentinfo-is-top-level?application=axeAPI"""
    


class landmark_main_is_top_level(cat.semantics, best_practice, ruleId="landmark-main-is-top-level"):
    """Ensures the main landmark is at top level
    
Main landmark should not be contained in another landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-main-is-top-level?application=axeAPI"""
    


class landmark_no_duplicate_banner(cat.semantics, best_practice, ruleId="landmark-no-duplicate-banner"):
    """Ensures the document has at most one banner landmark
    
Document should not have more than one banner landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-no-duplicate-banner?application=axeAPI"""
    


class landmark_no_duplicate_contentinfo(cat.semantics, best_practice, ruleId="landmark-no-duplicate-contentinfo"):
    """Ensures the document has at most one contentinfo landmark
    
Document should not have more than one contentinfo landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-no-duplicate-contentinfo?application=axeAPI"""
    


class landmark_no_duplicate_main(cat.semantics, best_practice, ruleId="landmark-no-duplicate-main"):
    """Ensures the document has at most one main landmark
    
Document should not have more than one main landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-no-duplicate-main?application=axeAPI"""
    


class landmark_one_main(cat.semantics, best_practice, ruleId="landmark-one-main"):
    """Ensures the document has a main landmark
    
Document should have one main landmark

https://dequeuniversity.com/rules/axe/4.9/landmark-one-main?application=axeAPI"""
    


class landmark_unique(cat.semantics, best_practice, ruleId="landmark-unique"):
    """Landmarks should have a unique role or role/label/title (i.e. accessible name) combination
    
Ensures landmarks are unique

https://dequeuniversity.com/rules/axe/4.9/landmark-unique?application=axeAPI"""
    


class link_in_text_block(cat.color, wcag2a, wcag141, TTv5, TT13_a, EN_301_549, EN_9_1_4_1, ruleId="link-in-text-block"):
    """Ensure links are distinguished from surrounding text in a way that does not rely on color
    
Links must be distinguishable without relying on color

https://dequeuniversity.com/rules/axe/4.9/link-in-text-block?application=axeAPI"""
    


class link_name(cat.name_role_value, wcag2a, wcag244, wcag412, section508, section508_22_a, TTv5, TT6_a, EN_301_549, EN_9_2_4_4, EN_9_4_1_2, ACT, ruleId="link-name"):
    """Ensures links have discernible text
    
Links must have discernible text

https://dequeuniversity.com/rules/axe/4.9/link-name?application=axeAPI"""
    


class list(cat.structure, wcag2a, wcag131, EN_301_549, EN_9_1_3_1, ruleId="list"):
    """Ensures that lists are structured correctly
    
<ul> and <ol> must only directly contain <li>, <script> or <template> elements

https://dequeuniversity.com/rules/axe/4.9/list?application=axeAPI"""
    


class listitem(cat.structure, wcag2a, wcag131, EN_301_549, EN_9_1_3_1, ruleId="listitem"):
    """Ensures <li> elements are used semantically
    
<li> elements must be contained in a <ul> or <ol>

https://dequeuniversity.com/rules/axe/4.9/listitem?application=axeAPI"""
    


class marquee(cat.parsing, wcag2a, wcag222, TTv5, TT2_b, EN_301_549, EN_9_2_2_2, ruleId="marquee"):
    """Ensures <marquee> elements are not used
    
<marquee> elements are deprecated and must not be used

https://dequeuniversity.com/rules/axe/4.9/marquee?application=axeAPI"""
    


class meta_refresh_no_exceptions(cat.time_and_media, wcag2aaa, wcag224, wcag325, ruleId="meta-refresh-no-exceptions"):
    """Ensures <meta http-equiv="refresh"> is not used for delayed refresh
    
Delayed refresh must not be used

https://dequeuniversity.com/rules/axe/4.9/meta-refresh-no-exceptions?application=axeAPI"""
    


class meta_refresh(cat.time_and_media, wcag2a, wcag221, TTv5, TT8_a, EN_301_549, EN_9_2_2_1, ruleId="meta-refresh"):
    """Ensures <meta http-equiv="refresh"> is not used for delayed refresh
    
Delayed refresh under 20 hours must not be used

https://dequeuniversity.com/rules/axe/4.9/meta-refresh?application=axeAPI"""
    


class meta_viewport_large(cat.sensory_and_visual_cues, best_practice, ruleId="meta-viewport-large"):
    """Ensures <meta name="viewport"> can scale a significant amount
    
Users should be able to zoom and scale the text up to 500%

https://dequeuniversity.com/rules/axe/4.9/meta-viewport-large?application=axeAPI"""
    


class meta_viewport(cat.sensory_and_visual_cues, wcag2aa, wcag144, EN_301_549, EN_9_1_4_4, ACT, ruleId="meta-viewport"):
    """Ensures <meta name="viewport"> does not disable text scaling and zooming
    
Zooming and scaling must not be disabled

https://dequeuniversity.com/rules/axe/4.9/meta-viewport?application=axeAPI"""
    


class nested_interactive(cat.keyboard, wcag2a, wcag412, TTv5, TT6_a, EN_301_549, EN_9_4_1_2, ruleId="nested-interactive"):
    """Ensures interactive controls are not nested as they are not always announced by screen readers or can cause focus problems for assistive technologies
    
Interactive controls must not be nested

https://dequeuniversity.com/rules/axe/4.9/nested-interactive?application=axeAPI"""
    


class no_autoplay_audio(cat.time_and_media, wcag2a, wcag142, TTv5, TT2_a, EN_301_549, EN_9_1_4_2, ACT, ruleId="no-autoplay-audio"):
    """Ensures <video> or <audio> elements do not autoplay audio for more than 3 seconds without a control mechanism to stop or mute the audio
    
<video> or <audio> elements must not play automatically

https://dequeuniversity.com/rules/axe/4.9/no-autoplay-audio?application=axeAPI"""
    


class object_alt(cat.text_alternatives, wcag2a, wcag111, section508, section508_22_a, EN_301_549, EN_9_1_1_1, ruleId="object-alt"):
    """Ensures <object> elements have alternate text
    
<object> elements must have alternate text

https://dequeuniversity.com/rules/axe/4.9/object-alt?application=axeAPI"""
    


class p_as_heading(cat.semantics, wcag2a, wcag131, EN_301_549, EN_9_1_3_1, experimental, ruleId="p-as-heading"):
    """Ensure bold, italic text and font-size is not used to style <p> elements as a heading
    
Styled <p> elements must not be used as headings

https://dequeuniversity.com/rules/axe/4.9/p-as-heading?application=axeAPI"""
    


class page_has_heading_one(cat.semantics, best_practice, ruleId="page-has-heading-one"):
    """Ensure that the page, or at least one of its frames contains a level-one heading
    
Page should contain a level-one heading

https://dequeuniversity.com/rules/axe/4.9/page-has-heading-one?application=axeAPI"""
    


class presentation_role_conflict(cat.aria, best_practice, ACT, ruleId="presentation-role-conflict"):
    """Elements marked as presentational should not have global ARIA or tabindex to ensure all screen readers ignore them
    
Ensure elements marked as presentational are consistently ignored

https://dequeuniversity.com/rules/axe/4.9/presentation-role-conflict?application=axeAPI"""
    


class region(cat.keyboard, best_practice, ruleId="region"):
    """Ensures all page content is contained by landmarks
    
All page content should be contained by landmarks

https://dequeuniversity.com/rules/axe/4.9/region?application=axeAPI"""
    


class role_img_alt(cat.text_alternatives, wcag2a, wcag111, section508, section508_22_a, TTv5, TT7_a, EN_301_549, EN_9_1_1_1, ACT, ruleId="role-img-alt"):
    """Ensures [role="img"] elements have alternate text
    
[role="img"] elements must have an alternative text

https://dequeuniversity.com/rules/axe/4.9/role-img-alt?application=axeAPI"""
    


class scope_attr_valid(cat.tables, best_practice, ruleId="scope-attr-valid"):
    """Ensures the scope attribute is used correctly on tables
    
scope attribute should be used correctly

https://dequeuniversity.com/rules/axe/4.9/scope-attr-valid?application=axeAPI"""
    


class scrollable_region_focusable(cat.keyboard, wcag2a, wcag211, wcag213, TTv5, TT4_a, EN_301_549, EN_9_2_1_1, EN_9_2_1_3, ruleId="scrollable-region-focusable"):
    """Ensure elements that have scrollable content are accessible by keyboard
    
Scrollable region must have keyboard access

https://dequeuniversity.com/rules/axe/4.9/scrollable-region-focusable?application=axeAPI"""
    


class select_name(cat.forms, wcag2a, wcag412, section508, section508_22_n, TTv5, TT5_c, EN_301_549, EN_9_4_1_2, ACT, ruleId="select-name"):
    """Ensures select element has an accessible name
    
Select element must have an accessible name

https://dequeuniversity.com/rules/axe/4.9/select-name?application=axeAPI"""
    


class server_side_image_map(cat.text_alternatives, wcag2a, wcag211, section508, section508_22_f, TTv5, TT4_a, EN_301_549, EN_9_2_1_1, ruleId="server-side-image-map"):
    """Ensures that server-side image maps are not used
    
Server-side image maps must not be used

https://dequeuniversity.com/rules/axe/4.9/server-side-image-map?application=axeAPI"""
    


class skip_link(cat.keyboard, best_practice, ruleId="skip-link"):
    """Ensure all skip links have a focusable target
    
The skip-link target should exist and be focusable

https://dequeuniversity.com/rules/axe/4.9/skip-link?application=axeAPI"""
    


class svg_img_alt(cat.text_alternatives, wcag2a, wcag111, section508, section508_22_a, TTv5, TT7_a, EN_301_549, EN_9_1_1_1, ACT, ruleId="svg-img-alt"):
    """Ensures <svg> elements with an img, graphics-document or graphics-symbol role have an accessible text
    
<svg> elements with an img role must have an alternative text

https://dequeuniversity.com/rules/axe/4.9/svg-img-alt?application=axeAPI"""
    


class tabindex(cat.keyboard, best_practice, ruleId="tabindex"):
    """Ensures tabindex attribute values are not greater than 0
    
Elements should not have tabindex greater than zero

https://dequeuniversity.com/rules/axe/4.9/tabindex?application=axeAPI"""
    


class table_duplicate_name(cat.tables, best_practice, ruleId="table-duplicate-name"):
    """Ensure the <caption> element does not contain the same text as the summary attribute
    
tables should not have the same summary and caption

https://dequeuniversity.com/rules/axe/4.9/table-duplicate-name?application=axeAPI"""
    


class table_fake_caption(cat.tables, experimental, wcag2a, wcag131, section508, section508_22_g, EN_301_549, EN_9_1_3_1, ruleId="table-fake-caption"):
    """Ensure that tables with a caption use the <caption> element.
    
Data or header cells must not be used to give caption to a data table.

https://dequeuniversity.com/rules/axe/4.9/table-fake-caption?application=axeAPI"""
    


class target_size(cat.sensory_and_visual_cues, wcag22aa, wcag258, ruleId="target-size"):
    """Ensure touch target have sufficient size and space
    
All touch targets must be 24px large, or leave sufficient space

https://dequeuniversity.com/rules/axe/4.9/target-size?application=axeAPI"""
    


class td_has_header(cat.tables, experimental, wcag2a, wcag131, section508, section508_22_g, TTv5, TT14_b, EN_301_549, EN_9_1_3_1, ruleId="td-has-header"):
    """Ensure that each non-empty data cell in a <table> larger than 3 by 3  has one or more table headers
    
Non-empty <td> elements in larger <table> must have an associated table header

https://dequeuniversity.com/rules/axe/4.9/td-has-header?application=axeAPI"""
    


class td_headers_attr(cat.tables, wcag2a, wcag131, section508, section508_22_g, TTv5, TT14_b, EN_301_549, EN_9_1_3_1, ruleId="td-headers-attr"):
    """Ensure that each cell in a table that uses the headers attribute refers only to other cells in that table
    
Table cells that use the headers attribute must only refer to cells in the same table

https://dequeuniversity.com/rules/axe/4.9/td-headers-attr?application=axeAPI"""
    


class th_has_data_cells(cat.tables, wcag2a, wcag131, section508, section508_22_g, TTv5, TT14_b, EN_301_549, EN_9_1_3_1, ruleId="th-has-data-cells"):
    """Ensure that <th> elements and elements with role=columnheader/rowheader have data cells they describe
    
Table headers in a data table must refer to data cells

https://dequeuniversity.com/rules/axe/4.9/th-has-data-cells?application=axeAPI"""
    


class valid_lang(cat.language, wcag2aa, wcag312, TTv5, TT11_b, EN_301_549, EN_9_3_1_2, ACT, ruleId="valid-lang"):
    """Ensures lang attributes have valid values
    
lang attribute must have a valid value

https://dequeuniversity.com/rules/axe/4.9/valid-lang?application=axeAPI"""
    


class video_caption(cat.text_alternatives, wcag2a, wcag122, section508, section508_22_a, TTv5, TT17_a, EN_301_549, EN_9_1_2_2, ruleId="video-caption"):
    """Ensures <video> elements have captions
    
<video> elements must have captions

https://dequeuniversity.com/rules/axe/4.9/video-caption?application=axeAPI"""
    


