import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from parsers.log_parser import parse_logfile_path, get_api_server_name
from parsers.log_parser import parse_request_data_string, parse_response_time_string
from models.db_structures import ENGINE
from models.db_structures import mapper_registry
from models.data_structures import Logfile, LoggedTest, JsonRpcRequest


def save_logged_tests_to_db(log_file: str) -> int:
    # Check if the log file exists
    if not os.path.isfile(log_file):
        print(f"Error: The log file not found:\\t{log_file}")
        return 1

    # Start db session
    mapper_registry.metadata.create_all(bind=ENGINE)
    Session = sessionmaker(bind=ENGINE)
    db_session = Session()
    db_session.begin()

    # Parse log file data
    print(f"Processing the file: {log_file}");
    try:
        lf_obj: Logfile = parse_logfile_path(log_file)
    except ValueError:
        print("Error: Log file name doesn't match the pattern. Data processing stopped.")
        return 1
    # Save log file data to db
    try:
        db_session.add(lf_obj)
        db_session.commit()
    except IntegrityError:
        print("WARNING: The logfile is already saved to the database.")
        db_session.rollback()
        # getting object id
        lf_obj.id = db_session.query(Logfile.id).filter(Logfile.path == lf_obj.path,
                                                        Logfile.created == lf_obj.created,
                                                        Logfile.hostname == lf_obj.hostname,
                                                        ).first()[0]
    except Exception as err:
        print("ERROR:Unexpected error has occurred while saving log file data to the database.")
        print(err.args)
        db_session.rollback()
        db_session.close()
        print("Exiting the program")
        return 1

    # Get api server name
    api_server_name = get_api_server_name(log_file)

    # Process log file data
    with open(log_file, "r") as lf:
        line = lf.readline()
        while line:
            if not line.startswith("Sending "):
                line = lf.readline()
                continue
            request_string = line
            response_string = lf.readline()
            line = response_string

            # Parse response string
            try:
                jsonRpcRequestObject: JsonRpcRequest = parse_request_data_string(request_string)
            except ValueError as err:
                print("WARNING: Invalid request data string.")
                print(response_string)
                print(err.args)
                continue
            # Parse response time string
            try:
                response_time = parse_response_time_string(response_string)
            except ValueError as err:
                print("WARNING: Invalid response time data string.")
                print(response_string)
                print(err.args)
                continue

            # Create LoggedTest object
            test_obj = LoggedTest(
                app_server=str(api_server_name),
                api_name=str(jsonRpcRequestObject.method.split(".")[0]),
                method=str(jsonRpcRequestObject.method.split(".")[1]),
                parameters=str(jsonRpcRequestObject.params),
                ran_at=lf_obj.created,
                method_exec_time=response_time,
                logfile_id=lf_obj.id
            )
            # Save test data to db
            db_session.add(test_obj)

    try:
        db_session.commit()
    except IntegrityError as err:
        print("WARNING: The test is already in the database")
        print(err.args)
        db_session.rollback()
    db_session.close()
    print(f"INFO: The file has been processed successfully and its data is in the database now:\n\t{log_file}")
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to log file you want to parse.", type=str)
    args = parser.parse_args()
    path_to_log_file = args.path
    save_logged_tests_to_db(path_to_log_file)

