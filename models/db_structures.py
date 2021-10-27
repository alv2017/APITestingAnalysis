from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, Index
from sqlalchemy.orm import registry, relationship

from models.data_structures import Logfile, LoggedTest

ENGINE = create_engine('sqlite:///api_tests.sqlite3', echo=False)
meta = MetaData()
mapper_registry = registry(metadata=meta)

# Logfiles
logfiles = Table('logfiles', mapper_registry.metadata,
                 Column('id', Integer, primary_key=True),
                 Column('path', String(255), nullable=False),
                 Column('created', DateTime, nullable=False),
                 Column('hostname', String(32), nullable=False),
                 Column('parse_time', DateTime),

                 UniqueConstraint('path', 'created', 'hostname', name='lf_unique_idx')
                 )

# LoggedTests
logged_tests = Table('logged_tests', mapper_registry.metadata,
                     Column('id', String, primary_key=True),
                     Column('app_server', String(32), nullable=False),
                     Column('api_name', String(32), nullable=False),
                     Column('method', String(255), nullable=False),
                     Column('parameters', String(512)),
                     Column('ran_at', DateTime),
                     Column('ran_week', String(7)),
                     Column('method_exec_time', Float, nullable=False),
                     Column('logfile_id', Integer),

                     Index("api_method_idx", "api_name", "method"),

                     ForeignKeyConstraint(
                         ['logfile_id'],
                         ['logfiles.id'],
                         onupdate="CASCADE", ondelete="SET NULL"
                     ),
                     )

mapper_registry.map_imperatively(Logfile, logfiles,
                                 properties={
                                     'logged_tests': relationship(LoggedTest, backref='logfiles',
                                                                  order_by=logged_tests.c.id)
                                 })
mapper_registry.map_imperatively(LoggedTest, logged_tests)


def start_mappers(mapper):
    mapper.map_imperatively(Logfile, logfiles,
                            properties={
                                'logged_tests': relationship(LoggedTest, backref='logfiles',
                                                             order_by=logged_tests.c.id)
                            })
    mapper.map_imperatively(LoggedTest, logged_tests)


if __name__ == "__main__":
    mapper_registry.metadata.create_all(ENGINE)
