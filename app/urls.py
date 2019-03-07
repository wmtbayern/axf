from django.conf.urls import url

from app import views

urlpatterns=[

    url(r'^$',views.home,name='home'),
    url(r'^upfile/$',views.upfile,name='upfile'),
    url(r'^savefile/$', views.savefile, name='savefile'),
    url(r'^market/$',views.market,name='market'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^mine/$',views.mine,name='mine'),
]