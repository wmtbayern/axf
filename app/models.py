from django.db import models

# Create your models here.


#基础类
class BaseModel(models.Model):
    img=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    trackid=models.CharField(max_length=10)

    class Meta:
        abstract=True


#注意表名字要一样
#cosolo  选中sql语句   可以执行mysql语句
class Wheel(BaseModel):
    class Meta:
        db_table='axf_wheel'

class Nav(BaseModel):
    class Meta:
        db_table='axf_nav'

class Mustbuy(BaseModel):
    class Meta:
        db_table='axf_mustbuy'

class Shop(BaseModel):
    class Meta:
        db_table='axf_shop'


class Mainshow(models.Model):
    trackid=models.CharField(max_length=10)
    name=models.CharField(max_length=100)
    img=models.CharField(max_length=100)
    categoryid=models.CharField(max_length=10)
    brandname=models.CharField(max_length=100)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = 'axf_mainshow'

class Foodtype(models.Model):
    typeid=models.CharField(max_length=10)
    typename=models.CharField(max_length=100)
    childtypenames=models.CharField(max_length=200)
    typesort=models.IntegerField()
    class Meta:
        db_table='axf_foodtypes'

class Goods(models.Model):
    #商品的id
    productid=models.CharField(max_length=10)
   #商品图片
    productimg=models.CharField(max_length=100)
    #商品名字
    productname=models.CharField(max_length=100)
    #商品详细介绍
    productlongname=models.CharField(max_length=256)
    #是否精选商品
    isxf=models.IntegerField()
    #是否买一送一
    pmdesc=models.IntegerField()
    #商品规格
    specifics=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    marketprice=models.DecimalField(max_digits=6,decimal_places=2)
    #分类的ID
    categoryid=models.CharField(max_length=100)
    #子分类的id
    childcid=models.IntegerField()
    #子分类的名字
    childcidname=models.CharField(max_length=100)

    dealerid=models.CharField(max_length=10)
    storenums=models.IntegerField()  ##排序
    #销量排序
    productnum=models.IntegerField()
    class Meta:
        db_table='axf_goods'


#用户模型
class User(models.Model):
    #邮箱
    email=models.CharField(max_length=40,unique=True)
    #密码
    password=models.CharField(max_length=256)

    name=models.CharField(max_length=100)
    img=models.CharField(max_length=40,default='axf.png')
    #等级
    rank=models.IntegerField(default=1)

    class Meta:
        db_table='axf_user'

#购物车模型
class Cart(models.Model):
    #使用关联字段就可以了
    #不用都把数据拿过来
    #用户(添加的商品属于哪个用户)
    user=models.ForeignKey(User)
    #商品(添加的是哪个属性)
    goods=models.ForeignKey(Goods)

    #商品的规格,有哪些字段是要显示的(颜色,内存,版本,大小)

    #商品数量
    number=models.IntegerField()
    #是否选中
    isselect=models.BooleanField(default=True)
    #是否删除   (逻辑删除)
    isdelete=models.BooleanField(default=False)

    class Meta:
        db_table='axf_cart'




