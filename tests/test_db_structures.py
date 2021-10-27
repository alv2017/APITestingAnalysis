import unittest
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from models.data_structures import Logfile, LoggedTest
from models.db_structures import logfiles, logged_tests
from models.db_structures import mapper_registry


class TestMappings(unittest.TestCase):
    def setUp(self):
        self.db_name = "db.sqlite3"
        self.engine = create_engine(f"sqlite:///{self.db_name}", echo=False)
        mapper_registry.metadata.create_all(bind=self.engine)
        session = sessionmaker(bind=self.engine)
        self.db_session = session()

    def tearDown(self):
        if self.db_session:
            self.db_session.close()
        if self.engine:
            del self.engine
        if os.path.isfile(self.db_name):
            os.remove(self.db_name)

    def test_mappings(self):
        self.assertEqual(Logfile.__table__, logfiles)
        self.assertEqual(LoggedTest.__table__, logged_tests)

    def test_create_logfile_in_db(self):
        lf = Logfile(
            path='path/to/some.log',
            created=datetime(year=2021, month=1, day=4, hour=15, minute=0, second=0),
            hostname='localhost',
            parse_time=datetime(year=2021, month=1, day=4, hour=15, minute=15, second=0),
        )
        self.db_session.add(lf)
        self.db_session.commit()
        result = self.db_session.query(Logfile).first()
        self.assertEqual(result, lf)

    def test_create_logged_test_in_db(self):
        lt = LoggedTest(
            app_server="app_server",
            api_name="api-1",
            method="some_method",
            parameters=str({"x": 1, "y":"Hello, World!"}),
            ran_at=datetime(year=2021, month=1, day=1, hour=14, minute=15, second=5),
            method_exec_time=0.3254,
            logfile_id=1
        )
        self.db_session.add(lt)
        self.db_session.commit()
        result = self.db_session.query(LoggedTest).first()
        self.assertEqual(result, lt)