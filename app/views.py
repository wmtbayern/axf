import hashlib
import random
import time

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from AXF import settings
from app.models import Wheel, Nav, Mustbuy, Foodtype, Shop, Mainshow, Goods, User


def upfile(request):
    return render(request,'upfile.html')
import os
def savefile(request):
    if request.method=='POST':
        file=request.FILES['file']
        filepath=os.path.join(settings.MEDIA_ROOT,file.name)
        with open (filepath,'wb') as fp:
            for info in file.chunks():
                fp.write(info)
        return HttpResponse('文件上传成功哦')

def home(request):
    #首页主要是获取数据,展示数据
    # 注意样式的问题,
    wheels=Wheel.objects.all()
    navs=Nav.objects.all()
    mustbuys=Mustbuy.objects.all()
    shops=Shop.objects.all()
    shophead = shops[0]
    shoptabs=shops[1:3]
    shop_lists=shops[3:7]
    shopcommend=shops[7:11]
    mains=Mainshow.objects.all()
    response_dir={
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        'shoptabs':shoptabs,
        'shop_lists':shop_lists,
        'shopcommend':shopcommend,
        'mains':mains
    }
    return render(request, 'home/home.html',response_dir)


def market(request,childid='0',sortid='0'):
    #获取分类信息
    foodtypes=Foodtype.objects.all()
    # good_list=Goods.objects.all[0:8]

    #客户端记录点击的分类id,等同于index
    index=int(request.COOKIES.get('index','0'))
    #获取到商品的分类信息
    categoryid=foodtypes[index].typeid

    if childid=='0':
        goods_list=Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list=Goods.objects.filter\
            (categoryid=categoryid).filter(childid=childid)
    if sortid=='1':
        goods_list=goods_list.order_by('-productnum')
    elif sortid == '2':
        goods_list = goods_list.order_by('price')
    elif sortid == '3':
        goods_list = goods_list.order_by('-price')

    childtypenames = foodtypes[index].childtypenames
    # 存储子类信息 列表
    childtype_list = []
    # 将对应的子类拆分出来
    for item in childtypenames.split('#'):
        # item  >> 全部分类:0
        # item  >> 子类名称: 子类ID
        item_arr = item.split(':')
        temp_dir = {
            'name': item_arr[0],
            'id': item_arr[1]
        }

        childtype_list.append(temp_dir)

    #获取子类信息
    response_dir={
        'foodtypes':foodtypes,
        'goods_list':goods_list,
        'childtype_list':childtype_list,
        'childid': childid,

    }
    return render(request, 'market/market.html',context=response_dir)


def cart(request):
    return render(request, 'cart/cart.html')

def mine(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = None
    if userid:
        user = User.objects.get(pk=userid)

    return render(request, 'mine/mine.html',
        context={'user': user})


def login(request):
    # if request.method == 'GET':
    #     return render(request, 'mine/login.html')
    # elif request.method == 'POST':
    #     name = request.POST.get('name')
    #     password = generate_password(request.POST.get('password'))
    #     users = User.objects.filter(name=name, password=password)


    return render(request,'mine/login.html')


def logout(request):
    request.session.flush()

    return render(request,'mine/mine.html')

def generate_password(params):
    md5=hashlib.md5()
    md5.update(params.encode('utf-8'))
    return md5.hexdigest()

def generate_token():
    #时间戳+随机数+
    token=str(time.time())+str(random.random)
    md5=hashlib.md5()
    md5.update(token.encode('utf-8'))
    return md5.hexdigest()

def register(request):
    if request.method=='GET':
        return  render(request,'mine/register.html')
    elif request.method=='POST':
        #获取数据

        email = request.POST.get('email')
        name = request.POST.get('name')
        password = generate_password(request.POST.get('password'))
        # 存入数据库

        user = User()
        user.email = email
        user.password = password
        user.name = name
        user.save()

        #生成token
        token=generate_token()
        #注意cache导入包的问题  在cache里面设置token
        cache.set(token, user.id, 60 * 60 * 24 * 3)
        #记得把token给到客户端
        request.session['token']=token

        return redirect('axf:mine')