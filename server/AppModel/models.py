# -*- coding:UTF-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.admin import DraggableMPTTAdmin
from feincms.module.page.models import Page
import datetime
from django.utils.html import format_html
from AppModel import *


class UserInfo(models.Model):
    AUTH_CHOICES = [
    ('0', '员工'),
    ('1', '主管'),
    ('2', '主任'),
    ('3', '管理员'),
    ]
    nick_name = models.CharField(max_length=200,verbose_name='微信名')
    user_name = models.CharField(max_length=200,verbose_name='用户名')
    weixin_openid = models.CharField(max_length=200,verbose_name='微信ID')
    phone_number = models.CharField(max_length=200,verbose_name='手机号')
    category = TreeForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True,verbose_name='所属部门')
    auth = models.CharField(max_length=200, choices=AUTH_CHOICES,verbose_name='用户权限')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
    
    def __str__(self):
        return self.user_name


class AssetInfo(models.Model):
    asset_name = models.CharField(max_length=200,verbose_name='物品名称')
    asset_sn = models.CharField(max_length=200,verbose_name='物品编码')
    asset_type = models.CharField(max_length=200,verbose_name='物品型号')
    asset_count = models.CharField(max_length=200,verbose_name='物品库存')
    asset_band = models.CharField(max_length=200,verbose_name='物品品牌')
    asset_specification = models.CharField(max_length=200,verbose_name='物品规格')
    asset_band = models.CharField(max_length=200,verbose_name='物品品牌')
    asset_unit = models.CharField(max_length=200,verbose_name='计量单位')
    asset_image = models.ImageField(u'物品图片',null=True, blank=True, upload_to='asset_image')
    asset_ccategory = models.ForeignKey('CommodityCategory',on_delete=models.CASCADE,null=True,blank=True,verbose_name='类别标签')
    asset_limit_nu = models.CharField(max_length=200,verbose_name='申领数量限制')



    class Meta:
        verbose_name = '物品信息'
        verbose_name_plural = '物品信息'
    

class Claimlist(models.Model):
    claim_count = models.CharField(max_length=200,verbose_name='申领数量')
    claim_name = models.CharField(max_length=200,verbose_name='物品名称')
    claim_unit =  models.CharField(max_length=200,verbose_name='物品名称')

    def __str__(self):
        return (("%s %s%s") % (self.claim_name,self.claim_count,self.claim_unit))

    class Meta:
        verbose_name = '物品清单'
        verbose_name_plural = '物品清单'

class ClaimRecord(models.Model):
    STATUS_CHOICES = [
    ('0', '待主管审批'),
    ('1', '待主任审批'),
    ('2', '待管理员审批'),
    ('3', '审批完成'),
    ('4', '已发放'),
    ('5', '未批准'),
    ]
    # claim_username = models.CharField(max_length=200,verbose_name='申领人')
    claim_weixin_openid = models.CharField(max_length=200,verbose_name='申领人微信OPENID')
    # claim_count = models.CharField(max_length=200,verbose_name='申领数量')
    # claim_phone_num = models.CharField(max_length=200,verbose_name='申领人手机')
    # claim_name = models.CharField(max_length=200,verbose_name='物品名称')
    # id = models.CharField(max_length=200,verbose_name='订单id',primary_key=True)
    claim_list = models.ManyToManyField(Claimlist) 
    claim_date = models.DateField(default=datetime.datetime.now(),verbose_name='申领时间')
    category = TreeForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True,verbose_name='所属部门')
    approval_status = models.CharField(max_length=200, choices=STATUS_CHOICES,verbose_name='审批状态')
    desc =  models.CharField(max_length=200, verbose_name='申请理由',default="无理由")
    if_exceed_standard = models.BooleanField(verbose_name='是否超标',default="False") 

    class Meta:
        verbose_name = '领用记录'
        verbose_name_plural = '领用记录'
        # 自定义的权限，两参数分别是权限的名字和权限的描述
        permissions = (
            ("supervisor_approval", "第一主管审批"),
            ("director_approval", "办公室主任审批"),
            ("admin_approval", "管理员审批通过，等待发放"),
            ("issued_asset", "发放审批"),
            ("rejectted", "审批不通过"), 
        )


class MappingClaimLisToRecord(models.Model):
    claimlist = models.ForeignKey(Claimlist, models.DO_NOTHING,verbose_name='物品清单')
    claimrecord = models.ForeignKey(ClaimRecord, models.DO_NOTHING,verbose_name='申领记录')

    class Meta:
        managed = False
        db_table = 'AppModel_claimrecord_claim_list'
        unique_together = (('claimlist', 'claimrecord'),)


# 组织机构详细信息
class Post(models.Model):
      name = models.CharField(max_length=120,verbose_name='单位名称')
      category = TreeForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True,verbose_name='上级部门')
      createtime = models.CharField(max_length=200,verbose_name='创建时间')
      createuser = models.CharField(max_length=200,verbose_name='创建者')
      connected_number = models.CharField(max_length=200,verbose_name='联系电话')
      slug = models.SlugField(verbose_name='标签')
      
      def __str__(self):
          return self.name

#物品分类
class CommodityCategory(MPTTModel):
      name = models.CharField(max_length=50, unique=True,verbose_name='名称')
      parent = TreeForeignKey('self' ,null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True,verbose_name='上级分类')
      slug = models.SlugField(verbose_name='标签')
      image = models.ImageField(u'物品图片',null=True, blank=True, upload_to='asset_image')
    
      class MPTTMeta:
        order_insertion_by = ['name']
    
      class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'
        verbose_name = '物品分类'
    
      def get_slug_list(self):
        try:
          ancestors = self.get_ancestors(include_self=True)
        except:
          ancestors = []
        else:
          ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
          slugs.append('/'.join(ancestors[:i+1]))
        return slugs
    
      def __str__(self):
        return self.name



# 组织机构
class Category(MPTTModel):
      name = models.CharField(max_length=50, unique=True,verbose_name='名称')
      parent = TreeForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True,verbose_name='上级部门')
      slug = models.SlugField(verbose_name='标签')
    
      class MPTTMeta:
        order_insertion_by = ['name']
    
      class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'
        verbose_name = '组织机构'
    
      def get_slug_list(self):
        try:
          ancestors = self.get_ancestors(include_self=True)
        except:
          ancestors = []
        else:
          ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
          slugs.append('/'.join(ancestors[:i+1]))
        return slugs
    
      def __str__(self):
        return self.name


class WeixinSessionKey(models.Model):
    weixin_openid = models.CharField(max_length=200,verbose_name='openid')
    weixin_sessionkey = models.CharField(max_length=200,verbose_name='sessionkey')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        verbose_name = '微信用户SK'
        verbose_name_plural = '微信用户SK'

# 统计查询
class StatisticsInfo(models.Model):
  asset_name = models.CharField(max_length=120,verbose_name='物品名称')
  category_name = models.CharField(max_length=120,verbose_name='部门名称')
  claim_count = models.CharField(max_length=120,verbose_name='领用数量')