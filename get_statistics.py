from sqlalchemy.orm import sessionmaker
from sqlalchemy import String, Integer, Float
from sqlalchemy import text, bindparam

from models.db_structures import ENGINE
from models.db_structures import mapper_registry
from models.data_structures import LoggedTest


def get_weekly_statistics(year: int, week: int) -> int:
    # Connect to DB
    engine = ENGINE
    conn = engine.connect()

    ran_week_value = str(year) + "W" + str(week).zfill(2)

    # Query
    q = """SELECT api_name, method, ran_week, count(method_exec_time) as total_tests, 
                sum(method_exec_time) as total_time, avg(method_exec_time) as avg_time
                
               FROM logged_tests
               WHERE ran_week=:ran_week_value
               GROUP BY api_name, method, ran_week
               ORDER BY api_name, method, ran_week
    """

    stmt = text(q)
    stmt = stmt.columns(api_name=String, method=String, ran_week=String, total_tests=Integer, sum=Float, avg=Float)
    stmt = stmt.bindparams(bindparam("ran_week_value", type_=String), )
    result = conn.execute(stmt, {"ran_week_value": ran_week_value})

    data = result.fetchall()
    print("\n***")
    print("Weekly Statistics:")
    if data:
        for row in data:
            print(f"API: {row.api_name}, Method: {row.method}, Week: {row.ran_week},"
                  f"Total Tests: {row.total_tests}, Total Time: {row.total_time}, Avg. Time: {row.avg_time}")
    else:
        print(f"No data available for year: {year}, week: {week}")

    # Get statistics
    conn.close()
    print("***")
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="Year, when tests where performed.", type=int)
    parser.add_argument("week", help="Week, when tests where performed", type=int)
    args = parser.parse_args()
    year = args.year
    week = args.week

    get_weekly_statistics(year, week)
    exit(0)

