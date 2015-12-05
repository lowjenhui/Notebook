# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from gluon import utils as gluon_utils
from datetime import datetime
import json
import time

def index():
    user_id = auth.user_id
    post_id_new = gluon_utils.web2py_uuid()
    return dict(post_id_new=post_id_new, user_id=user_id)

def load_posts():
    """Loads all boards."""
    board_list = db().select(db.board.ALL)
    post_dict = {}
    for b in board_list:
        post_dict[b.board_id] = {
            'author': b.author,
            'post_title': b.post_title,
            'post_time_js': b.post_time_js,
            'post_time': b.post_time,
            'post_description': b.post_description,
            'post_image_url': b.post_image_url,
            'post_list': b.post_list,
            'post_color': b.post_color,
            'post_size': b.post_size}
    return response.json(dict(post_dict=post_dict))

def js_to_python_utctime(js_time_stamp):
    return datetime.utcfromtimestamp(int(js_time_stamp)/1000)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


