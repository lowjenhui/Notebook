#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

from datetime import datetime

# Here is a table for boards.
db.define_table('notes',
    Field('note_id', default=lambda:gluon.utils.web2py_uuid()),
    Field('note_title', required=True),
    Field('note_time', 'datetime', default=request.utcnow),
    Field('note_description', 'text'),
    Field('note_image_url'),
    Field('note_list'),
    Field('note_author', db.auth_user, default=auth.user_id),
    Field('note_colour'),
    Field('note_size'))

db.notes.note_id.readable = db.notes.note_id.writable = False
db.notes.id.readable = db.notes.id.writable = False
db.notes.note_author.readable = db.notes.note_author.writable = False

db.define_table('note_comments',
    Field('note_id'),
    Field('note_time', 'datetime'),
    Field('note_author', db.auth_user, default=auth.user_id),
    Field('note_content'))

db.define_table('shared_notes',
    Field('note_id'),
    Field('shared_author', db.auth_user))

db.define_table('tags',
    Field('note_id'),
    Field('tag'))
