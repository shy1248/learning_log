'''定义learning_logs的URL模式'''

from django.conf.urls import url
from . import views

urlpatterns = [

    # 主页
    url(r'^$', views.index, name='index'),
    # 显示所有的主题
    url(r'^topics/$', views.get_all_topics, name='topics'),
    # 显示主题内容
    url(r'^topic/(?P<topic_id>\d+)/$', views.get_topic_entries, name='topic'),
    # 添加主题页面
    url(r'^new_topic/$', views.add_topic, name='new_topic'),
    # Ajax查询主题下是否有条目
    url(r'^ajax_verify_is_empty_of_topic/$', views.is_empty_topic, name='query_topic'),
    # Ajax请求删除主题
    url(r'^ajax_req_del_topic/$', views.del_topic, name='del_topic'),
    # 在某主题下添加一条记录
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.add_entry, name='new_entry'),
    # 编辑某条记录
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    # 删除某条记录
    url(r'^del_entry/$', views.del_entry, name='del_entry'),

]
