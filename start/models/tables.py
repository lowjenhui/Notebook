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
db.define_table('board',
    Field('post_id'),
    Field('post_title', required=True),
    Field('post_time_js', 'integer'),
    Field('post_time', 'datetime'),
    Field('post_description', 'text'),
    Field('post_image_url'),
    Field('post_list'),
    Field('author', db.auth_user, default=auth.user_id),
    Field('post_colour'),
    Field('post_size'))

db.board.board_id.readable = db.board.board_id.writable = False
db.board.id.readable = db.board.id.writable = False
db.board.author.readable = db.board.author.writable = False
db.board.post_id.readable = db.board.post_id.writable = False

db.define_table('post_comments',
    Field('post_id'),
    Field('post_time', 'datetime'),
    Field('author', db.auth_user, default=auth.user_id),
    Field('content'))

db.define_table('permissions',
    Field('post_id'),
    Field('author', db.auth_user, default=auth.user_id))