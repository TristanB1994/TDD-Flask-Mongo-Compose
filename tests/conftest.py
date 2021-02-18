import pytest

from application.app import create_app
# from application.models import db, ALIAS
from mongoengine.context_managers import switch_db
from flask_mongoengine import MongoEngine
from mongoengine import connect, disconnect

@pytest.fixture
def app():

    app = create_app("testing")
    # app.db.disconnect
    return app


@pytest.fixture(scope="function")
def database(app):
    with app.app_context():
        
        db = app.db.get_db('testing')
        # db = MongoEngine(app) #.get_db('testing')
        # db = connect('testing', host='0.0.0.0', username='admin', password='password', alias='testing')

        print(f"db {db}")
        
    yield db

    with app.app_context():

        colls = db.list_collection_names()
        for i in colls:
            db.drop_collection(i)
        print(f"list collections: {db.list_collection_names()}")

    db = app.db.disconnect()


# ['HOST', 'PORT', '_BaseObject__codec_options', '_BaseObject__read_concern', '_BaseObject__read_preference', '_BaseObject__write_concern', '_MongoClient__all_credentials', '_MongoClient__cursor_manager', '_MongoClient__default_database_name', '_MongoClient__index_cache', '_MongoClient__index_cache_lock', '_MongoClient__kill_cursors_queue', '_MongoClient__lock', '_MongoClient__options', '_MongoClient__start_session', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_cache_credentials', '_cache_index', '_cached', '_close_cursor', '_close_cursor_now', '_constructor_args', '_database_default_options', '_encrypter', '_end_sessions', '_ensure_session', '_event_listeners', '_get_server_session', '_get_socket', '_get_topology', '_handle_getlasterror', '_is_writable', '_kill_cursors', '_kill_cursors_executor', '_process_kill_cursors', '_process_periodic_tasks', '_process_response', '_purge_credentials', '_purge_index', '_read_preference_for', '_repr_helper', '_retry_internal', '_retry_with_session', '_retryable_read', '_retryable_write', '_return_server_session', '_run_operation_with_response', '_select_server', '_send_cluster_time', '_server_property', '_slaveok_for_server', '_socket_for_reads', '_socket_for_writes', '_tmp_session', '_topology', '_topology_settings', '_write_concern_for', 'address', 'arbiters', 'close', 'close_cursor', 'codec_options', 'database_names', 'drop_database', 'event_listeners', 'fsync', 'get_database', 'get_default_database', 'is_locked', 'is_mongos', 'is_primary', 'kill_cursors', 'list_database_names', 'list_databases', 'local_threshold_ms', 'max_bson_size', 'max_idle_time_ms', 'max_message_size', 'max_pool_size', 'max_write_batch_size', 'min_pool_size', 'next', 'nodes', 'primary', 'read_concern', 'read_preference', 'retry_reads', 'retry_writes', 'secondaries', 'server_info', 'server_selection_timeout', 'set_cursor_manager', 'start_session', 'unlock', 'watch', 'write_concern']
