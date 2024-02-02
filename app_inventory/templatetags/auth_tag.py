from django import template
register = template.Library()


# pagination
@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url,encoded_querystring)
    return url


@register.filter()
def makelistofvariationstag(value):
    value = value.split('*')
    # print(value)
    return value

@register.filter()
def makelistofvariationstagbycomma(value):
    value = value.replace('*', ', ')
    # print(value)
    return value

@register.filter()
def make_options_list_by_obj(value):
    print('make_options_list_by_obj ->', value)
    if value.product_has_variant == True:

        if value.product_variant.all():
            for obj in value.product_variant.all():
                if obj.default_variant == True:
                    print('enter hear1 .....................', obj)
                    main_var_val = obj.value.split('*')
                    varient_dict = {f"{obj.name.split('*')[var]}":[main_var_val[var]] for var in range(len(obj.name.split('*')))}
                    print('main name  ->', varient_dict)

            for sub_obj in value.product_variant.all():
                print('enter hear .....................', sub_obj.name.split('*'))
                if sub_obj.default_variant == False:
                    # for sub_var in value['sub']:
                    for sub_name_count in range(len(sub_obj.name.split('*'))):
                        print('sub name-->', obj.name.split('*')[sub_name_count], sub_name_count)

                        var_val = varient_dict[obj.name.split('*')[sub_name_count]]
                        var_val.append(obj.value.split('*')[sub_name_count])
                    

                    # Create a new dictionary with unique values
                    value = {key: list(set(values)) for key, values in varient_dict.items()}
                    print('main value  ->', value)

                                # print(main_var_val[''])
                        # sub_var_name = sub_var.variant_name.split('*')
                        # sub_var_val = sub_var.variant_value.split('*')
                    return value.items()
                else:
                    print('enter in else hear...')
        else:
            return {}
                
    else:
        return {}
    
    
@register.filter()
def filter_percentage_off_in_sale_marked_price(obj):
    # print(old_discount)
    formatted_percentage = 0.0
    # print(obj.sellingPrice, obj.markedPrice)
    if obj.sellingPrice and obj.markedPrice:
        percentage_difference = ((float(obj.markedPrice) - float(obj.sellingPrice)) / float(obj.markedPrice)) * 100
        formatted_percentage = "{:.2f}".format(percentage_difference)
    return formatted_percentage

