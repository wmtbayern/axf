from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from AXF import settings
from app.models import Wheel, Nav, Mustbuy, Foodtype, Shop, Mainshow


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
    #获取数据,展示数据
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


def market(request):
    #获取分类信息
    foodtypes=Foodtype.objects.all()
    response_dir={
        'foodtypes':foodtypes,

    }
    return render(request, 'market/market.html',response_dir)


def cart(request):
    return render(request, 'cart/cart.html')


def mine(request):
    return render(request, 'mine/mine.html')


