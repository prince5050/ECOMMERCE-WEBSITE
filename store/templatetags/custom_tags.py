from django import template
register = template.Library()


@register.filter()
def percentage(actual_price, percentage):
    after_percentage = int(actual_price) - int(actual_price)*int(percentage)/100;
    return after_percentage

@register.filter()
def percentage_amount(actual_price, percentage):
    percentage_amt = int(actual_price)*int(percentage)/100;
    return percentage_amt

@register.filter()
def pro_with_percentage(actual_price, percentage):
    after_percentage = int(actual_price) + int(actual_price)*int(percentage)/100;
    return after_percentage

@register.filter()
def replace_name(strs):
    new_str = strs.replace(" ", "-")
    new_str1 = new_str.replace("|", "of")
    new_str2 = new_str1.replace("&", "and")
    new_str2 = new_str2.lower()
    return new_str2
