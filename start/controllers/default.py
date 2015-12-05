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
    board_id_new = gluon_utils.web2py_uuid()
    return dict(board_id_new=board_id_new, user_id=user_id)

def load_boards():
    """Loads all boards."""
    board_list = db().select(db.board.ALL)
    board_dict = {}
    for b in board_list:
        board_dict[b.board_id] = {
            'author': b.author,
            'board_name': b.board_name}
    return response.json(dict(board_dict=board_dict))

@auth.requires_signature()
def add_board():
    db.board.update_or_insert((db.board.board_id == request.vars.board_id),
            board_id=request.vars.board_id,
            board_name=request.vars.board_name)
    return "ok"

def posts():
    board_id = request.args(0)
    board = db(db.board.board_id == board_id).select().first()
    board_name = board.board_name
    post_list = db(db.posts.board_id == board_id).select()
    post_id_new = gluon_utils.web2py_uuid()
    user_id = auth.user_id
    return dict (board_id=board_id, board_name=board_name, post_list=post_list, post_id_new=post_id_new, user_id=user_id)

def load_posts():
    """Loads all posts."""
    post_list = db(db.posts.board_id == request.vars.board_id).select()
    post_dict = {}
    for p in post_list:
        post_dict[p.post_id] = {
            'author': p.author,
            'post_title':p.post_title,
            'post_time_js':p.post_time_js,
            'post_time':p.post_time,
            'post_description':p.post_description
        }
    return response.json(dict(post_dict=post_dict))

@auth.requires_signature()
def add_post():
    print ("post_id?", request.vars.post_id)
    db.posts.update_or_insert((db.posts.post_id == request.vars.post_id),
            post_id=request.vars.post_id,
            board_id=request.vars.board_id,
            post_title=request.vars.post_title,
            post_description=request.vars.post_description,
            post_time_js=request.vars.post_time_js,
            post_time=js_to_python_utctime(request.vars.post_time_js))
    return "ok"

@auth.requires_signature()
def delete_post():
    delete_array=request.vars.get('delete_array[]', None)
    if (type(delete_array) is str):
        delete_array=[delete_array]
    print ("delete_array", delete_array)
    for post_id in delete_array:
        print ("post_id", post_id)
        db(db.posts.post_id == post_id).delete()
    return "ok"

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


