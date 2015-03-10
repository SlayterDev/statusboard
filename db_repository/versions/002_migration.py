from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
todo = Table('todo', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('description', String(length=280)),
    Column('assigned', String(length=64)),
    Column('timestamp', DateTime),
    Column('creator', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['todo'].columns['assigned'].create()
    post_meta.tables['todo'].columns['creator'].create()
    post_meta.tables['todo'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['todo'].columns['assigned'].drop()
    post_meta.tables['todo'].columns['creator'].drop()
    post_meta.tables['todo'].columns['timestamp'].drop()
