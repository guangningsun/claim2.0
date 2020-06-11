# -*- coding:UTF-8 -*-
from django.contrib import admin
from AppModel.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin, ExportActionModelAdmin
import logging,json,datetime
from django.utils.html import format_html
from django import forms
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from feincms.module.page.models import Page
from django.utils.html import format_html,escape, mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import time


logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
handler = logging.FileHandler("tjctwl.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# 资产管理
@admin.register(AssetInfo)
class AssetInfoAdmin(ImportExportModelAdmin):
    list_display=['asset_name','asset_type','asset_sn','asset_band','asset_specification','asset_unit','asset_image','asset_ccategory','asset_limit_nu','asset_limit_price','asset_if_deduct']
    # list_editable = ['asset_name','asset_count']
    search_fields =('asset_name','asset_type','asset_sn','asset_band','asset_specification','asset_unit','asset_image','asset_limit_nu','asset_limit_price','asset_if_deduct')
    fieldsets = [
       ('用户数据', {'fields': ['asset_name','asset_type','asset_sn','asset_band','asset_specification','asset_unit','asset_image','asset_ccategory','asset_limit_nu','asset_limit_price','asset_if_deduct'], 'classes': ['']}),
    ]
    list_display_links = ('asset_name',)
    list_per_page = 20


# 用户管理
@admin.register(UserInfo)
class UserInfoAdmin(ImportExportModelAdmin): 
    list_display=['id','nick_name','user_name','weixin_openid','phone_number','category','auth','address']
    search_fields =('nick_name','user_name','weixin_openid','phone_number','category','auth','address')
    fieldsets = [
       ('用户数据', {'fields': ['nick_name','user_name','weixin_openid','phone_number','category','auth','address'], 'classes': ['']}),
    ]
    list_per_page = 15


# 订单管理
@admin.register(OrderInfo)
class OrderInfoAdmin(ImportExportModelAdmin): 
    list_display=['id','order_status','order_is_special','get_order_create_time','get_desc','order_total_price','order_image','order_apartment','order_user','order_exceed_reason']
    # search_fields =('nick_name','user_name','weixin_openid','phone_number','category','auth','address')
    fieldsets = [
       ('用户数据', {'fields': ['order_status','order_is_special','order_total_price','order_image','order_apartment','order_user','order_exceed_reason'], 'classes': ['']}),
    ]
    list_per_page = 15
    # 转换订单创建时间格式
    def get_order_create_time(self, obj):
        if obj.order_create_time is not None:
            timeArray = time.localtime(int(obj.order_create_time))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return otherStyleTime
        else:
            return '-'
    get_order_create_time.short_description = "订单创建时间"

    # 获取物品清单列表
    def get_desc(self, obj):
        if obj.id is not None:
            commodity_list = [CommodityInfo.objects.filter(id = cl.commodityinfo_id) for cl in MappingCommodityToOrder.objects.filter(orderinfo_id=obj.id)]
            return [ (("%s%s%s*%s%s") % (cc[0].commodity_supplier,cc[0].commodity_name,cc[0].commodity_price,cc[0].commodity_count,cc[0].commodity_unit)) for cc in commodity_list]
        else:
            return "-"
    get_desc.short_description = "订单商品列表"
    
    actions = ["supervisor_approval",'rejectted']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if  request.user.is_superuser is not True:
            if request.user.has_perm("AppModel.supervisor_approval"):
                del actions['director_approval']
                del actions['admin_approval']
                del actions['issued_asset']
            if request.user.has_perm("AppModel.director_approval"):
                del actions['supervisor_approval']
                del actions["admin_approval"]
                del actions['issued_asset']
            if request.user.has_perm("AppModel.admin_approval"):
                del actions['director_approval']
                del actions['supervisor_approval']
        return actions

    # 批准订单
    def supervisor_approval(self, request, queryset):
        rows_updated = queryset.update(order_status='1')
        for qs in queryset:
            commodity_list = MappingCommodityToOrder.objects.filter(orderinfo_id=qs.id)
            for cl in commodity_list:
                ci = CommodityInfo.objects.get(id=cl.commodityinfo_id)
                ci.commodity_status = '0'
                ci.save()
        if rows_updated == 1:
            message_bit = "订单审批通过"
        else:
            message_bit = "%s 条订单申请" % rows_updated
        self.message_user(request, " %s 成功审批." % message_bit ,level=messages.SUCCESS)

    supervisor_approval.short_description = "批准"

    # 拒绝订单
    def rejectted(self, request, queryset):
        rows_updated = queryset.update(order_status='2')
        #部门预算金额回退
        current_month = datetime.datetime.now().month
        for orderinfo in queryset:
            budgetinfo = BudgetInfo.objects.get(category=orderinfo.order_apartment,month=current_month)
            commodity_cost_num = 0
            #通过订单查询到所有商品
            commodity_list = [CommodityInfo.objects.filter(id = cl.commodityinfo_id) for cl in MappingCommodityToOrder.objects.filter(orderinfo_id=orderinfo.id)]
            for ci in commodity_list:
                for cc in ci:
                    if cc.commodity_if_deduct == True:
                        commodity_cost_num = commodity_cost_num + float(cc.commodity_total_price)
            #根据商品是否抵扣余额减少对应花销
            #根据商品是否抵扣余额增加对应余额
            budgetinfo.cost_num = float(budgetinfo.cost_num) - float(orderinfo.order_total_price)
            budgetinfo.surplus = float(budgetinfo.surplus) + commodity_cost_num
            budgetinfo.save()
        if rows_updated == 1:
            message_bit = "1 条订单申请"
        else:
            message_bit = "%s 条订单申请" % rows_updated
        self.message_user(request," %s 成功拒绝." % message_bit, level=messages.SUCCESS)
    rejectted.short_description = "拒绝"


# 用户管理
@admin.register(StatisticsInfo)
class StatisticsInfoAdmin(ImportExportModelAdmin): 
    # list_display=['asset_name','category_name','claim_count']

    # list_per_page = 10
    change_list_template = 'admin_test.html'
 
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )
 
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
 
        metrics = {
            'days': "", # date是model累的字段
            'views_count': "", # views_count是model累的字段
            'ip_count': "", # ip_count是model累的字段
 
        }
        # response.context_data['asset_name'] = list(
        #     qs.values('asset_name').annotate(**metrics)
        # )
 
        return response



# 组织机构设置
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name','category','createtime','createuser','connected_number','slug']
    list_per_page = 10

admin.site.register(Category , MPTTModelAdmin)



# 供应商管理
@admin.register(SupplierInfo)
class SupplierInfoAdmin(ImportExportModelAdmin): 
    list_display=['id','supplier_name','supplier_short']
    search_fields =('supplier_name','supplier_short')
    fieldsets = [
       ('用户数据', {'fields': ['supplier_name','supplier_short'], 'classes': ['']}),
    ]
    list_per_page = 15

# 部门预算管理

@admin.register(BudgetInfo)
class BudgetInfoAdmin(ImportExportModelAdmin): 
    list_display=['id','category','year','month','budget','cost_num','surplus','status']
    search_fields =('category','year','month','budget','cost_num','surplus','status')
    fieldsets = [
       ('用户数据', {'fields': ['category','year','month','budget','cost_num','surplus','status'], 'classes': ['']}),
    ]
    list_per_page = 15

# 供应商库存管理
@admin.register(SupplierAssetInfo)
class SupplierAssetInfoAdmin(ImportExportModelAdmin): 
    list_display=['supplier_name','price','assetinfo','asset_num','if_off_shelf','sys_username']
    search_fields =('supplier_name__supplier_name','price','assetinfo__asset_name','asset_num','if_off_shelf','sys_username')
    fieldsets = [
       ('用户数据', {'fields': ['supplier_name','price','assetinfo','asset_num','if_off_shelf'], 'classes': ['']}),
    ]

    def get_queryset(self,request):
        qs = super(SupplierAssetInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sys_username=request.user.username)
    
    def save_model(self, request, obj, form, change):
        if obj.sys_username == request.user.username:
            super().save_model(request, obj, form, change)
        else:
            self.message_user(request,"非供应商系统用户没有权限更改商品库存" , level=messages.SUCCESS)

    list_per_page = 15
    list_display_links = ('supplier_name',)


# 供应商订单管理
@admin.register(CommodityInfo)
class CommodityInfoAdmin(admin.ModelAdmin): 
    list_display=['commodity_name','commodity_unit','commodity_image','commodity_total_price','commodity_specification','commodity_price','commodity_count','commodity_supplier','commodity_status','commodity_username','commodity_apartment','commodity_phonenum','commodity_address','sys_username']
    # search_fields =('supplier_name','price','assetinfo','asset_num','sys_username')
    fieldsets = [
       ('用户数据', {'fields': ['commodity_name','commodity_unit','commodity_image','commodity_total_price','commodity_specification','commodity_price','commodity_count','commodity_supplier','commodity_status','sys_username'], 'classes': ['']}),
    ]

    def get_queryset(self,request):
        qs = super(CommodityInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sys_username=request.user.username)
    list_per_page = 15
    list_display_links = ('commodity_name',)

admin.site.register(CommodityCategory , MPTTModelAdmin)
# @admin.register(CommodityCategory)
# class CommodityCategoryAdmin(admin.ModelAdmin):
#     list_display = ['name','parent','slug','image']
#     list_per_page = 10

admin.site.site_title = "物品申领后台管理"
admin.site.site_header = "物品申领内控版2.0.1"


