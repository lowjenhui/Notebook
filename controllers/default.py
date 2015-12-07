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
    note_id_new = gluon_utils.web2py_uuid()
    return dict(note_id_new=note_id_new, user_id=user_id)

@auth.requires_login()
def load_notes():
    """Loads all notes by or shared to the current user."""
    note_list = db((db.notes.note_author==auth.user_id) | (db.shared_notes.shared_author==auth.user_id)).select(
        db.notes.ALL, left=db.shared_notes.on(db.notes.note_id==db.shared_notes.note_id))
    notes_dict = {}
    for n in note_list:
        notes_dict[n.note_id] = {
            'note_author': n.note_author,
            'note_time': python_utctime_to_js(n.note_time),
            'note_title': n.note_title,
            'note_description': n.note_description,
            'note_image_url': n.note_image_url,
            'note_list': n.note_list,
            'note_colour': n.note_colour,
            'note_size': n.note_size}
    return response.json(dict(notes_dict=notes_dict))

def js_to_python_utctime(js_time_stamp):
    return datetime.utcfromtimestamp(int(js_time_stamp)/1000)

def python_utctime_to_js(utctime):
    delta = utctime - datetime(1970, 1, 1)
    return delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**3

@auth.requires_signature()
def add_note():
    db.notes.update_or_insert((db.notes.note_id == request.vars.note_id),
            note_id=request.vars.note_id,
            note_author=request.vars.note_author,
            note_time=js_to_python_utctime(request.vars.note_time),
            note_title=request.vars.note_title,
            note_description=request.vars.note_description)
    return "ok"

@auth.requires_signature()
def change_colour_note():
    db(db.notes.note_id == request.vars.note_id).update(
            note_colour=request.vars.note_colour)
    return "ok"

@auth.requires_signature()
def delete_note():
    note_id = request.vars.note_id
    db(db.notes.note_id == note_id).delete()
    return "ok"

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


