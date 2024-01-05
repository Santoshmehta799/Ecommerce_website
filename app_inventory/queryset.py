from django.db.models import QuerySet
from urllib.parse import unquote
from django.db.models import Q


class ProductSectionQuerySet(QuerySet):
    def get_main_and_sub_inventory(self, user):
        """
            create the dict main and sub product as below by passing user : 
            [ {'main':'obj','sub':['obj',]}, 
                {'main':'obj','sub':['obj',]},] 
        """
        inventory_obj = [{'main':product} for product in self.filter(
            account=user, variant_default=True)]
        for pro_obj in inventory_obj:
            sub_lst = self.filter(account=user, variant_default=False, 
                variant_product_id= pro_obj['main'].variant_product_id )
            pro_obj['sub'] = sub_lst
        return inventory_obj
    
    
    def get_main_and_sub_inventory_by_id(self, user, product_varient_id = None):
        """
            create the dict main and sub product as below 
            by passing user and product varient id : 
        """

        filtered_products = list(self.filter(account=user, variant_default=True, variant_product_id=product_varient_id))
        inventory_obj = [{'main': filtered_products[0]}] if filtered_products else []
        for pro_obj in inventory_obj:
            sub_lst = self.filter(account=user, variant_default=False, 
                variant_product_id= pro_obj['main'].variant_product_id,)
            pro_obj['sub'] = sub_lst
        return inventory_obj
    

    def filter_main_and_sub_inventory_by_product_id(self, user, serach_filter = None):
        """
            This filter search_filter and on bases of id and name it filter it. : 
        """
        inventory_obj = self.filter(account=user, variant_default=True).order_by('-date')
        # print("inventory_obj ====>>>>", inventory_obj)
        if serach_filter:
            # Decode URL-encoded string
            serach_filter_decoded = unquote(serach_filter)
            # print('enter serach_filter fielter -->', serach_filter)

            # Try to convert to an integer
            try:
                active_filter_id = int(serach_filter_decoded)
                print('active_filter_id type-->',type(active_filter_id))
                # Filter by ID or name using Q object
                inventory_obj = inventory_obj.filter(Q(id=active_filter_id) | Q(name__icontains=serach_filter_decoded))
                print("====>>>>", inventory_obj)
                print('enter try ...')
            except ValueError:
                # If conversion to int fails, assume it's a name and filter by name
                inventory_obj = inventory_obj.filter(name__icontains=serach_filter_decoded)
                print('enter except ...')
                print("====>>>>", inventory_obj)

        inventory_obj = [{'main':product} for product in inventory_obj]
        for pro_obj in inventory_obj:
            sub_lst = self.filter(account=user, variant_default=False, 
                variant_product_id=pro_obj['main'].variant_product_id )
            pro_obj['sub'] = sub_lst
        return inventory_obj


    def get_all_main_and_sub_inventory(self):
        """
            create the dict main and sub product for all products : 
            [ {'main':'obj','sub':['obj',]}, 
                {'main':'obj','sub':['obj',]},] 
        """
        inventory_obj = [{'main':product} for product in self.filter(variant_default=True)]
        for pro_obj in inventory_obj:
            sub_lst = self.filter(variant_default=False, variant_product_id=pro_obj['main'].variant_product_id )
            pro_obj['sub'] = sub_lst
        return inventory_obj
    
    def get_single_main_and_sub_inventory_by_id(self,product_varient_id = None):
        """
            create the dict main and sub product as below 
            by passing user and product varient id : 
        """

        filtered_products = list(self.filter(variant_default=True, variant_product_id=product_varient_id))
        inventory_obj = [{'main': filtered_products[0]}] if filtered_products else []
        for pro_obj in inventory_obj:
            sub_lst = self.filter(variant_default=False, 
                variant_product_id= pro_obj['main'].variant_product_id,)
            pro_obj['sub'] = sub_lst
        return inventory_obj