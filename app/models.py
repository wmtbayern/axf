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




