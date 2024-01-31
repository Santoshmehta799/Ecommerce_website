import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from app_dashboard.models import Country, States
from app_inventory.models import Category, PickUpWarehouseLocation, PriceStructure, Product, ProductImage, ProductType, ProductVariant, ShippingDetails

from common.enums import ProductDimensionUnitEnums, ServicedRegionsEnums,\
    ShippingMethodEnums, PackedBoxDimensionsUnitEnums,\
    ProductWeighteEnums, MinimumOrderQuantityEnums,\
    GuaranteeEnums, TaxCodeEnums, WarrantyEnums
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

@login_required
def inventory(request):
    success = ""
    error = ""
    user = request.user

    product_obj = Product.objects.filter(seller=user)

    per_page_records = 10
    page_num = request.GET.get('page', 1)
    paginator = Paginator(product_obj, per_page_records)
    try:
        product_obj = paginator.page(page_num)
    except PageNotAnInteger:
        product_obj = paginator.page(1)
    except EmptyPage:
        product_obj = paginator.page(paginator.num_pages)
    context = {
        "success": success,
        "error": error,
        "product_obj": product_obj,
    }
    return render(request, 'app_inventory/products.html', context)

def inventory2(request):
    return HttpResponse("This is inventory home page")

@login_required
def add_inventory_step_1(request):
    success = ""
    error = ""
    user = request.user
   
    if request.method == 'POST':
        seller_id = user.id
        product_title = request.POST.get('product_title')
        category_id = request.POST.get('category')
        product_type_id = request.POST.get('product_type')
        product_brand = request.POST.get('product_brand')
        description = request.POST.get('description')
        about_the_brand = request.POST.get('about_the_brand')
        country_of_origin_id = request.POST.get('country_of_origin')
        product_has_variant = request.POST.get('var_added')
   
        category = Category.objects.get(id=category_id)
        product_type = ProductType.objects.get(id=product_type_id)
        country_of_origin = Country.objects.get(id=country_of_origin_id)

        product = Product.objects.create(
            seller_id=seller_id,
            product_title=product_title,
            category=category,
            product_type=product_type,
            product_brand=product_brand,
            description=description,
            about_the_brand=about_the_brand,
            country_of_origin=country_of_origin,
            product_has_variant=product_has_variant
        )

        if product_has_variant == 'True':
            return redirect('app_inventory:add_inventory_step_2', product_id=product.id)
        else:
            return redirect('app_inventory:add_inventory_step_3', product_id=product.id)
    
    context = {
        "success": success,
        "error": error,
        "country_objs": Country.objects.all(),
        "category_objs": Category.objects.all(),
        "product_type_objs": ProductType.objects.all(),
    }
    return render(request, 'app_inventory/add_product_step_1.html', context)


def add_inventory_step_2(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")


    if request.method == 'POST':
        variants_name_list = request.POST.getlist('variant_name[]',[])
        final_varient_name_list = request.POST.getlist('final_varient_name',[])
        mrp_list = request.POST.getlist('mrp',[])
        sale_price_list = request.POST.getlist('sale_price',[])
        default_variant = request.POST.getlist('default_variant',[])
        price_in_request = request.POST.getlist('price_in_request',[])
        var_added = product.product_has_variant

        if var_added == True:
            for varient_index in range (len(final_varient_name_list)):
                delimiter = '*'
                product_varient_obj_name = delimiter.join(variants_name_list)
                product_varient_obj, created = ProductVariant.objects.get_or_create(
                    product=product,
                    name=product_varient_obj_name,
                    value=str(final_varient_name_list[varient_index]).replace(', ', '*').replace(',', '*'),
                    defaults={
                        'price_on_request': str(final_varient_name_list[varient_index])
                            .replace(', ', '*').replace(',', '*') in price_in_request,
                        'default_variant': str(final_varient_name_list[varient_index])
                            .replace(', ', '*').replace(',', '*') in default_variant,
                    }
                )
                price_structure_obj, created = PriceStructure.objects.get_or_create(
                    product_variant=product_varient_obj,
                    defaults={
                        'sale_price': sale_price_list[varient_index],
                        'mrp': mrp_list[varient_index],
                    }
                )


                images_prefix = 'picture_'
                varient_prefix = images_prefix + final_varient_name_list[varient_index]\
                    .replace(', ', '*').replace(',','*')+'|'
                for count in range(1,11):
                    images_name = varient_prefix + str(count)
                    # print('fatch value ====->',count ,request.FILES.get(f"{images_name}"))
                    if request.FILES.get(f"{images_name}"):
                        product_image_obj = ProductImage()
                        product_image_obj.product_variant = product_varient_obj
                        product_image_obj.picture = request.FILES.get(f"{images_name}")
                        product_image_obj.save()
                
        else:
            pass

        return redirect('app_inventory:add_inventory_step_3', product_id=product.id)

    context = {
        "success": success,
        "error": error,
        "product_obj": product,
    }

    return render(request, 'app_inventory/add_product_step_2.html', context)


@login_required
def add_inventory_step_3(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")
    
    if request.method == 'POST':
        storage = request.POST.get('storage')
        usage = request.POST.get('usage')
        installation = request.POST.get('installation')
        product_handling = request.POST.get('product_handling')
        warranty = request.POST.get('warranty')
        guarantee = request.POST.get('guarantee')
        components_per_unit = request.POST.get('components_per_unit')
        packaging_size = request.POST.get('packaging_size')
        material = request.POST.get('material')

        product.storage = storage
        product.usage = usage
        product.installation = installation
        product.product_handling = product_handling
        product.warranty = warranty
        product.guarantee = guarantee
        product.components_per_unit = components_per_unit
        product.packaging_size = packaging_size
        product.material = material
        product.save()


        if not product.product_has_variant:
            product_varient_obj, created  = ProductVariant.objects.get_or_create(product=product)
            product_varient_obj.default_variant = True
            product_varient_obj.save()
            for i in range(1, 11):
                picture_name = f"picture{i}"
                pictures = request.FILES.get(picture_name)
                if pictures:
                    print("=-======>",pictures)
                    product_image_obj = ProductImage(product_variant=product_varient_obj)
                    print("======>>ddd",product_image_obj)
                    product_image_obj.picture = pictures
                    product_image_obj.save()

        return redirect('app_inventory:add_inventory_step_4', product_id=product.id)
    
    context = {
        "success": success,
        "error": error,
        "warranty" : WarrantyEnums.choices,   
        "guarantee" : GuaranteeEnums.choices, 
        "product_obj": product,  
    }

    return render(request, 'app_inventory/add_product_step_3.html', context)


def add_inventory_step_4(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")
    
    try:
        product_variant_obj = ProductVariant.objects.filter(product=product)
    except:
        raise Http404("Given Varient query not found....")
    
  
    if request.method == 'POST':
        hsn_code = request.POST.get('hsn_code')
        price_on_request = request.POST.get('price_on_request')
        mrp = request.POST.get('mrp')
        sale_price = request.POST.get('sale_price')
        tax_code = request.POST.get('tax_code')
        shipping_include = request.POST.get('shipping_include')
        minimum_order_qunatity = request.POST.get('minimum_order_qunatity')
        minimum_order_qunatity_unit = request.POST.get('minimum_order_qunatity_unit')
        # print('shipping_include  -->', price_on_request, shipping_include)

        if product.product_has_variant:
            product.minimum_order_qunatity = minimum_order_qunatity
            product.minimum_order_qunatity_unit = minimum_order_qunatity_unit
            product.save()

            try:
                price_structure_obj = PriceStructure.objects.filter(product_variant__product=product.id)
                for price_structure in price_structure_obj:
                    price_structure.hsn_code = hsn_code
                    price_structure.tax_code = tax_code
                    price_structure.product_variant.product.shipping_include = shipping_include
                    price_structure.product_variant.product.save()
                    price_structure.product_variant.save()
                    price_structure.save()
            except Exception as e:
                print(f'ERROR : {e}')
        
        else:
            price_structure_obj, created = PriceStructure.objects.get_or_create(product_variant=product_variant_obj.first())
            price_structure_obj.hsn_code = hsn_code
            if price_on_request == 'True':
                # print('enter if', price_structure_obj.product_variant.price_on_request)
                price_structure_obj.product_variant.price_on_request = price_on_request
                price_structure_obj.product_variant.product.shipping_include = False
            else:
                # print('enter else', price_structure_obj.product_variant.price_on_request)
                # print('shipping_include add -->',price_structure_obj.product_variant.product.shipping_include)
                price_structure_obj.product_variant.product.shipping_include = shipping_include
                price_structure_obj.product_variant.price_on_request = price_on_request
                # print('shipping_include after -->',price_structure_obj.product_variant.product.shipping_include)
                price_structure_obj.mrp = mrp
                price_structure_obj.sale_price = sale_price
                price_structure_obj.tax_code = tax_code

            price_structure_obj.product_variant.product.save()
            price_structure_obj.product_variant.save()
            price_structure_obj.save()
            # print('shipping_include final -->',price_structure_obj.product_variant.product.shipping_include)
        return redirect('app_inventory:add_inventory_step_5', product_id=product.id)

    context = {
        "success": success,
        "error": error,
        "minimum_order_quantity" : MinimumOrderQuantityEnums.choices,
        "tax_code" : TaxCodeEnums.choices,
        "product_obj": product,
    }
    return render(request, 'app_inventory/add_product_step_4.html',context)


def add_inventory_step_5(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")
    
    try:
        product_variant_obj = ProductVariant.objects.filter(product=product)
    except:
        raise Http404("Given Varient query not found....")
    
    if request.method == 'POST':
        product_weight = request.POST.get('product_weight')
        product_weight_unit = request.POST.get('product_weight_unit')
        returnable_product = request.POST.get('returnable_product')
        return_policy = request.POST.get('return_policy')
        shipping_method = request.POST.get('shipping_method')
        product_dimensions_unit = request.POST.get('product_dimensions_unit')
        product_dimensions_length = request.POST.get('product_dimensions_length')
        product_dimensions_width = request.POST.get('product_dimensions_width')
        product_dimensions_height = request.POST.get('product_dimensions_height')
        packed_box_dimensions_unit = request.POST.get('packed_box_dimensions_unit')
        packed_box_dimensions_length = request.POST.get('packed_box_dimensions_length')
        packed_box_dimensions_width = request.POST.get('packed_box_dimensions_width')
        packed_box_dimensions_height = request.POST.get('packed_box_dimensions_height')
        serviced_regions = request.POST.get('serviced_regions')
        pick_up_location = request.POST.getlist('pick_up_location')

   

        product_varient_obj = ProductVariant.objects.filter(product = product.id)
        # pick_up_ware_house_location_obj = PickUpWarehouseLocation
        
        for product_varient in product_varient_obj:
            shipping_detail_obj, created = ShippingDetails.objects.get_or_create(
                product_variant=product_varient
            )
            shipping_detail_obj.product_weight = product_weight
            shipping_detail_obj.product_weight = product_weight
            shipping_detail_obj.product_weight_unit = product_weight_unit
            shipping_detail_obj.returnable_product = returnable_product
            shipping_detail_obj.return_policy = return_policy
            shipping_detail_obj.shipping_method = shipping_method
            shipping_detail_obj.product_dimensions_unit = product_dimensions_unit
            shipping_detail_obj.product_dimensions_length = product_dimensions_length
            shipping_detail_obj.product_dimensions_width = product_dimensions_width
            shipping_detail_obj.product_dimensions_height = product_dimensions_height
            shipping_detail_obj.packed_box_dimensions_unit = packed_box_dimensions_unit
            shipping_detail_obj.packed_box_dimensions_length = packed_box_dimensions_length
            shipping_detail_obj.packed_box_dimensions_width = packed_box_dimensions_width
            shipping_detail_obj.packed_box_dimensions_height = packed_box_dimensions_height

            shipping_detail_obj.pick_up_location.clear()

            print("Before setting pick_up_location:", shipping_detail_obj.pick_up_location.all())
            shipping_detail_obj.pick_up_location.set(list(pick_up_location))
            print("After setting pick_up_location:", shipping_detail_obj.pick_up_location.all())

            # shipping_detail_obj.pick_up_location.set(list(pick_up_location))

            if serviced_regions == "True":
                shipping_detail_obj.product_variant.product.serviced_regions = ServicedRegionsEnums.TO_PAN_INDIA
            else:    
                shipping_detail_obj.product_variant.product.serviced_regions = ServicedRegionsEnums.TO_SPECIFIED_STATES_CITIES

            shipping_detail_obj.product_variant.product.save()
            shipping_detail_obj.save()


        return redirect('app_dashboard:dashboard-page')
        
    context = {
        "success": success,
        "error": error,
        "shipping_method": ShippingMethodEnums.choices,
        "product_dimensions_unit": ProductDimensionUnitEnums.choices,
        "packed_box_dimensions_unit": PackedBoxDimensionsUnitEnums.choices,
        "product_weight": ProductWeighteEnums.choices,
        "pick_up_warehouse_location": PickUpWarehouseLocation.objects.filter(seller=request.user),
        "product_obj": product,
        "states_name" : [state.name for state in States.objects.filter(country__name='INDIA')],
        "states_id" : [state.id for state in States.objects.filter(country__name='INDIA')]
    }
    return render(request, 'app_inventory/add_product_step_5.html',context)



# Edit product 

@login_required
def edit_inventory_step_1(request, product_id):
    success = ""
    error = ""
    user = request.user

    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")
    
    try:
        product_variant_obj = ProductVariant.objects.filter(product=product)
    except:
        raise Http404("Given Varient query not found....")
   
    if request.method == 'POST':
        seller_id = user.id
        product_title = request.POST.get('product_title')
        category_id = request.POST.get('category')
        product_type_id = request.POST.get('product_type')
        product_brand = request.POST.get('product_brand')
        description = request.POST.get('description')
        about_the_brand = request.POST.get('about_the_brand')
        country_of_origin_id = request.POST.get('country_of_origin')
   
        category = Category.objects.get(id=category_id)
        product_type = ProductType.objects.get(id=product_type_id)
        country_of_origin = Country.objects.get(id=country_of_origin_id)

        product.product_title=product_title
        product.category=category
        product.product_type=product_type
        product.product_brand=product_brand
        product.description=description
        product.about_the_brand=about_the_brand
        product.country_of_origin=country_of_origin
        product.save()

        if product.product_has_variant == True:
            return redirect('app_inventory:edit_inventory_step_2', product_id=product.id)
        else:
            return redirect('app_inventory:edit_inventory_step_3', product_id=product.id)
    
    context = {
        "success": success,
        "error": error,
        "country_objs": Country.objects.all(),
        "category_objs": Category.objects.all(),
        "product_type_objs": ProductType.objects.all(),
        'product_objs': product
    }
    return render(request, 'app_inventory/edit_product_step_1.html', context)


def edit_inventory_step_2(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")


    if request.method == 'POST':
        variants_name_list = request.POST.getlist('variant_name[]',[])
        final_varient_name_list = request.POST.getlist('final_varient_name',[])
        mrp_list = request.POST.getlist('mrp',[])
        sale_price_list = request.POST.getlist('sale_price',[])
        default_variant = request.POST.getlist('default_variant',[])
        price_in_request = request.POST.getlist('price_in_request',[])
        var_added = product.product_has_variant
        
        if var_added == True:
            for varient_index in range (len(final_varient_name_list)):
                delimiter = '*'
                product_varient_obj_name = delimiter.join(variants_name_list)
                product_varient_obj, created = ProductVariant.objects.get_or_create(
                    product=product,
                    name=product_varient_obj_name,
                    value=str(final_varient_name_list[varient_index]).replace(', ', '*').replace(',', '*'),
                    defaults={
                        'price_on_request': str(final_varient_name_list[varient_index])
                            .replace(', ', '*').replace(',', '*') in price_in_request,
                        'default_variant': str(final_varient_name_list[varient_index])
                            .replace(', ', '*').replace(',', '*') in default_variant,
                    }
                )
                price_structure_obj, created = PriceStructure.objects.get_or_create(
                    product_variant=product_varient_obj,
                    defaults={
                        'sale_price': sale_price_list[varient_index],
                        'mrp': mrp_list[varient_index],
                    }
                )

                if not created:
                    price_structure_obj.sale_price = sale_price_list[varient_index]
                    price_structure_obj.mrp = mrp_list[varient_index]
                    price_structure_obj.save()
                

                images_prefix = 'picture_'
                varient_prefix = images_prefix + final_varient_name_list[varient_index]\
                    .replace(', ', '*').replace(',','*')+'|'
                for count in range(1,11):
                    images_name = varient_prefix + str(count)
                    # print('fatch value ====->',count ,request.FILES.get(f"{images_name}"))
                    if request.FILES.get(f"{images_name}"):
                        product_image_obj = ProductImage()
                        product_image_obj.product_variant = product_varient_obj
                        product_image_obj.picture = request.FILES.get(f"{images_name}")
                        product_image_obj.save()
                
        else:
            pass

        return redirect('app_inventory:edit_inventory_step_3', product_id=product.id)

    context = {
        "success": success,
        "error": error,
        "product_obj": product,
    }

    return render(request, 'app_inventory/edit_product_step_2.html', context)


@login_required
def edit_inventory_step_3(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")
    
    try:
        product_variant_obj = ProductVariant.objects.filter(product=product)
    except:
        raise Http404("Given Varient query not found....")
    
    if request.method == 'POST':
        storage = request.POST.get('storage')
        usage = request.POST.get('usage')
        installation = request.POST.get('installation')
        product_handling = request.POST.get('product_handling')
        warranty = request.POST.get('warranty')
        guarantee = request.POST.get('guarantee')
        components_per_unit = request.POST.get('components_per_unit')
        packaging_size = request.POST.get('packaging_size')
        material = request.POST.get('material')

        product.storage = storage
        product.usage = usage
        product.installation = installation
        product.product_handling = product_handling
        product.warranty = warranty
        product.guarantee = guarantee
        product.components_per_unit = components_per_unit
        product.packaging_size = packaging_size
        product.material = material
        product.save()


        if not product.product_has_variant:
            product_varient_obj = product_variant_obj.first()
            product_varient_obj.default_variant = True
            product_varient_obj.save()
            for i in range(1, 11):
                picture_name = f"picture{i}"
                pictures = request.FILES.get(picture_name)
                if pictures:
                    print("=-======>",pictures)
                    product_image_obj = ProductImage(product_variant=product_varient_obj)
                    print("======>>update", product_image_obj)
                    product_image_obj.picture = pictures
                    product_image_obj.save()

        return redirect('app_inventory:edit_inventory_step_4', product_id=product.id)
    
    context = {
        "success": success,
        "error": error,
        "warranty" : WarrantyEnums.choices,   
        "guarantee" : GuaranteeEnums.choices, 
        "product_obj": product,  
    }

    return render(request, 'app_inventory/edit_product_step_3.html', context)


def edit_inventory_step_4(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")
    
    try:
        product_variant_obj = ProductVariant.objects.filter(product=product)
    except:
        raise Http404("Given Varient query not found....")
    
  
    if request.method == 'POST':
        hsn_code = request.POST.get('hsn_code')
        price_on_request = request.POST.get('price_on_request')
        mrp = request.POST.get('mrp')
        sale_price = request.POST.get('sale_price')
        tax_code = request.POST.get('tax_code')
        shipping_include = request.POST.get('shipping_include')
        minimum_order_qunatity = request.POST.get('minimum_order_qunatity')
        minimum_order_qunatity_unit = request.POST.get('minimum_order_qunatity_unit')

        # print('shipping_include  -->', price_on_request, shipping_include)
        if product.product_has_variant:
            product.minimum_order_qunatity = minimum_order_qunatity
            product.minimum_order_qunatity_unit = minimum_order_qunatity_unit
            product.save()

            try:
                price_structure_obj = PriceStructure.objects.filter(product_variant__product=product.id)
                for price_structure in price_structure_obj:
                    price_structure.hsn_code = hsn_code
                    price_structure.product_variant.product.shipping_include = shipping_include
                    price_structure.tax_code = tax_code
                    price_structure.product_variant.product.save()
                    price_structure.product_variant.save()
                    price_structure.save()
            except Exception as e:
                print(f'ERROR : {e}')
        
        else:
            price_structure_obj, created = PriceStructure.objects.get_or_create(product_variant=product_variant_obj.first())
            price_structure_obj.hsn_code = hsn_code
            if price_on_request == 'True':
                # print('enter if', price_structure_obj.product_variant.price_on_request)
                price_structure_obj.product_variant.price_on_request = price_on_request
                price_structure_obj.product_variant.product.shipping_include = False
            else:
                # print('enter else', price_structure_obj.product_variant.price_on_request)
                # print('shipping_include add -->',price_structure_obj.product_variant.product.shipping_include)
                price_structure_obj.product_variant.product.shipping_include = shipping_include
                price_structure_obj.product_variant.price_on_request = price_on_request
                # print('shipping_include after -->',price_structure_obj.product_variant.product.shipping_include)
                price_structure_obj.mrp = mrp
                price_structure_obj.sale_price = sale_price
                price_structure_obj.tax_code = tax_code

            price_structure_obj.product_variant.product.save()
            price_structure_obj.product_variant.save()
            price_structure_obj.save()
            # print('shipping_include final -->',price_structure_obj.product_variant.product.shipping_include)
        return redirect('app_inventory:edit_inventory_step_5', product_id=product.id)

    context = {
        "success": success,
        "error": error,
        "minimum_order_quantity" : MinimumOrderQuantityEnums.choices,
        "tax_code" : TaxCodeEnums.choices,
        "product_obj": product,
    }
    return render(request, 'app_inventory/edit_product_step_4.html',context)


def edit_inventory_step_5(request, product_id):
    success = ""
    error = ""
    user = request.user
    try:
        product = Product.objects.get(id=product_id, seller=user)
    except:
        raise Http404("Given query not found....")
    
    try:
        product_variant_obj = ProductVariant.objects.filter(product=product)
    except:
        raise Http404("Given Varient query not found....")
    
    if request.method == 'POST':
        product_weight = request.POST.get('product_weight')
        product_weight_unit = request.POST.get('product_weight_unit')
        returnable_product = request.POST.get('returnable_product')
        return_policy = request.POST.get('return_policy')
        shipping_method = request.POST.get('shipping_method')
        product_dimensions_unit = request.POST.get('product_dimensions_unit')
        product_dimensions_length = request.POST.get('product_dimensions_length')
        product_dimensions_width = request.POST.get('product_dimensions_width')
        product_dimensions_height = request.POST.get('product_dimensions_height')
        packed_box_dimensions_unit = request.POST.get('packed_box_dimensions_unit')
        packed_box_dimensions_length = request.POST.get('packed_box_dimensions_length')
        packed_box_dimensions_width = request.POST.get('packed_box_dimensions_width')
        packed_box_dimensions_height = request.POST.get('packed_box_dimensions_height')
        serviced_regions = request.POST.get('serviced_regions')
        pick_up_location = request.POST.getlist('pick_up_location')

   

        product_varient_obj = ProductVariant.objects.filter(product = product.id)
        # pick_up_ware_house_location_obj = PickUpWarehouseLocation
        
        for product_varient in product_varient_obj:
            shipping_detail_obj, created = ShippingDetails.objects.get_or_create(
                product_variant=product_varient
            )
            shipping_detail_obj.product_weight = product_weight
            shipping_detail_obj.product_weight = product_weight
            shipping_detail_obj.product_weight_unit = product_weight_unit
            shipping_detail_obj.returnable_product = returnable_product
            shipping_detail_obj.return_policy = return_policy
            shipping_detail_obj.shipping_method = shipping_method
            shipping_detail_obj.product_dimensions_unit = product_dimensions_unit
            shipping_detail_obj.product_dimensions_length = product_dimensions_length
            shipping_detail_obj.product_dimensions_width = product_dimensions_width
            shipping_detail_obj.product_dimensions_height = product_dimensions_height
            shipping_detail_obj.packed_box_dimensions_unit = packed_box_dimensions_unit
            shipping_detail_obj.packed_box_dimensions_length = packed_box_dimensions_length
            shipping_detail_obj.packed_box_dimensions_width = packed_box_dimensions_width
            shipping_detail_obj.packed_box_dimensions_height = packed_box_dimensions_height

            shipping_detail_obj.pick_up_location.clear()

            print("Before setting pick_up_location:", shipping_detail_obj.pick_up_location.all())
            shipping_detail_obj.pick_up_location.set(list(pick_up_location))
            print("After setting pick_up_location:", shipping_detail_obj.pick_up_location.all())

            # shipping_detail_obj.pick_up_location.set(list(pick_up_location))

            if serviced_regions == "True":
                shipping_detail_obj.product_variant.product.serviced_regions = ServicedRegionsEnums.TO_PAN_INDIA
            else:    
                shipping_detail_obj.product_variant.product.serviced_regions = ServicedRegionsEnums.TO_SPECIFIED_STATES_CITIES

            shipping_detail_obj.product_variant.product.save()
            shipping_detail_obj.save()

        return redirect('app_dashboard:dashboard-page')
    
    context = {
        "success": success,
        "error": error,
        "shipping_method": ShippingMethodEnums.choices,
        "product_dimensions_unit": ProductDimensionUnitEnums.choices,
        "packed_box_dimensions_unit": PackedBoxDimensionsUnitEnums.choices,
        "product_weight": ProductWeighteEnums.choices,
        "pick_up_warehouse_location": PickUpWarehouseLocation.objects.filter(seller=request.user),
        "product_obj": product,
        "states_name" : [state.name for state in States.objects.filter(country__name='INDIA')],
        "states_id" : [state.id for state in States.objects.filter(country__name='INDIA')],
    }
    return render(request, 'app_inventory/edit_product_step_5.html',context)


def load_subcategory(request):  
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        print('$$$$$$$$$$$$$$ ->',category_id)

        html ="<option disabled value="">---Sub Category---</option>"
        sub_category = ProductType.objects.filter(category_id = category_id)
        print('sub_category ->', sub_category)
        if sub_category:
            for s_cat in sub_category:
                html += f'<option value="{s_cat.id}">{s_cat.name}</option>'
                
            context = {
                "data": html,
                "status" : True,
            }
            return JsonResponse(context) 
        else:
            context = {
                "data": "",
                "status" : False,
            }
            return JsonResponse(context) 




