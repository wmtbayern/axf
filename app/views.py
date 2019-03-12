import hashlib
import random
import time

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from AXF import settings
from app.models import Wheel, Nav, Mustbuy, Foodtype, Shop, Mainshow, Goods, User, Cart, Order, OrderGoods


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
            (categoryid=categoryid).filter(childcid=childid)
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

    carts=Cart.objects.all()

    return render(request, 'cart/cart.html',context={'carts':carts})

def mine(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = None
    if userid:
        user = User.objects.get(pk=userid)

    return render(request,'mine/mine.html',
        context={'user': user})


def login(request):
    if request.method == 'GET':
         return render(request, 'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = User.objects.filter(email=email)
        if users.exists():
            user=users.first()
            if user.password==generate_password(password):
                token=generate_token()   # 更新token

                cache.set(token,user.id,60*60*24*3) #设置token

                request.session['token']=token  #token给到客户端

                return redirect('axf:mine')
            else:
                return render(request, 'mine/login.html', context={
                    'pwd_err': '密码错误'
                })
        else:  #用户不存在
            return render(request,'mine/login.html',context={
                'user_err':'用户不存在'
            })
    # return render(request,'mine/mine.html')

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


def checkemail(request):
    email=request.GET.get('email')
    users=User.objects.filter(email=email)
    if users.exists():
        response_data={
            'status':0,
            'msg':'账户已占用'
        }
    else:
        response_data ={
            'status': 1,
            'msg': '账户可用'
        }
    return JsonResponse(response_data)

def addcart(request):
    #把商品添加到购物车.要获取用户和商品信息,分别处理
    # ,根据token 获取用户.   user goods 这两个是一对多的关系
    # ,可以由user 表获取商品的信息
    token=request.session.get('token')
    response_data={}
    if token:
        userid=cache.get(token)
        if userid:
            #登陆对象中获取商品信息goodsid
            #再通过goodsid去商品表goods中获取商品
            user=User.objects.get(pk=userid)
            #ajax里面是get 请求,   所以这里是get
            # ,goodsid 由客户端ajax请求发起的时候传递过来的

            goodsid=request.GET.get('goodsid')
            goods=Goods.objects.get(pk=goodsid)
            #由以上两个条件获取购物车信息
            carts=Cart.objects.filter(user=user).filter(goods=goods)
            #判断是否有购物车
            if carts.exists():
                cart=carts.first()
                #html 里面展示的数据是购物车里面的数据
                cart.number=cart.number + 1
                cart.save()
            else:    # 购物车不存在, 实际就是实例化一个购物车对象
                cart=Cart()
                cart.user=user
                cart.goods=goods
                cart.number= 1
                cart.save()
            #传输数据回到客户端进行展示
            response_data['status']=1
            response_data['number'] = cart.number
            response_data['msg']='添加{}到购物车成功,数量:{}'.format(cart.goods.productlongname,cart.number)

            return JsonResponse(response_data)
    #没有登陆的返回信息
    response_data['status']=-1
    response_data['msg']='请登陆'

    return JsonResponse(response_data)


def subcart(request):
    #获取用户
    token=request.session.get('token')
    userid = cache.get(token)
    user=User.objects.get(pk=userid)
    #获取商品
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)

    #由用户和商品获取购物车的信息
    carts = Cart.objects.filter(user=user).filter(goods=goods)
    cart = carts.first()  #注意这里的结果集问题,first()处理一下
    #点击减号    数量减1
    cart.number = cart.number-1
    #对购物车的操作都要记得保存
    cart.save()
    #记得返回数据给到客户端
    #两种写法,字典的写法,
    response_data={
        'status':1,
        'msg':'删除商品成功',
        'number':cart.number
    }
    return JsonResponse(response_data)


def changecartselect(request):

    cartid=request.GET.get('cartid')
    cart=Cart.objects.get(pk=cartid)
    cart.isselect=not cart.isselect
    cart.save()
    response_data={
        'msg':'修改成功',
        'status': 1 ,
        'isselect':cart.isselect,
    }


    return JsonResponse(response_data)

def changecartall(request):
    #根据ajax的请求获取
    isall=request.GET.get('isall')

    token=request.session.get('token')

    userid=cache.get(token)
    user=User.objects.get(pk=userid)
    #根据用户获取哪一个购物车
    carts=user.cart_set.all()
    #取反
    if isall=='true':
        isall=True
    else:
        isall=True
    for cart in carts:
        cart.isselect=isall
        cart.save()
    response_data={
        'msg':'操作成功',
        'status':'1',
    }
    return JsonResponse(response_data)

def generate_identifier():
    temp = str(time.time()) + str(random.randrange(100,1000))
    return temp

def generateorder(request):
    #都要获取用户
    token = request.session.get('token')

    userid = cache.get(token)

    user = User.objects.get(pk=userid)

    # 订单生成,保存
    order = Order()
    order.user = user
    order.identifier = generate_identifier()
    order.save()
    carts=user.cart_set.filter(isselect=True)
    #创建订单商品(实际就是购物车中选中的商品挪过来,生成新的表单)
    for cart in carts:
        orderGoods=OrderGoods()
        orderGoods.order=order
        orderGoods.goods=cart.goods
        orderGoods.number=cart.number
        orderGoods.save()
        #提交到订单后购物车的商品不再显示
        cart.delete()

    return render(request,'order/orderdetail.html',context={'order':order})


def orderlist(request):
    token = request.session.get('token')

    userid = cache.get(token)

    user = User.objects.get(pk=userid)

    #通过user获取订单,user 是主表,可以通过_set的方式获取从表的信息
    orders=user.order_set.all()
    status_list=['未付款','待付款','待发货','待收货','待评价','已评价']

    return render(request,'order/orderlist.html',context={
        'orders':orders,
        'status_list':status_list
    })

def orderdetail(request,identifier):
    token = request.session.get('token')

    userid = cache.get(token)

    user = User.objects.get(pk=userid)
    #由传入的参数获取订单详情,结果集,就算只有一个也是结果集,所以要加first

    order=Order.objects.filter(identifier=identifier).first()
    #返回给模板渲染
    return render(request,'order/orderdetail.html',context={
        'order':order
    })