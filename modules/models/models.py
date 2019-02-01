from playhouse.postgres_ext import *
import os
from configparser import ConfigParser
PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def config(filename=f"{PATH}/config.ini", section="testpostgresql"):
    """
    Simple config parser to load database connection info
    :param filename: The name of the file to load
    :param section: The section of the file to load
    :return: Returns a dictionary of database connection info
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        parameters = parser.items(section)
        for param in parameters:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section{section} not found in the {filename} file")
    return db


params = config()
database = PostgresqlExtDatabase(database=params['database'], user=params['user'],
                                         password=params['password'], host=params['host'], register_hstore=False)


class Guild(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4())
    name = TextField(null=False)
    display_name = TextField()
    server = TextField(null=False)
    region = TextField(null=False)

    class Meta:
        database = database


class Logs(Model):
    log_id = TextField(primary_key=True)
    log_date = TextField()
    log_title = TextField()
    log_zone = IntegerField()
    guild = ForeignKeyField(Guild, null=True, on_delete='CASCADE')

    class Meta:
        database = database


class Messages(Model):
    tag_label = TextField(primary_key=True)
    tag_author = TextField()
    tag_text = TextField(null=True)

    class Meta:
        database = database


class Discord(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4())
    server_id = TextField(null=True, unique=True)
    welcome_channel_id = TextField(null=True)
    roles_channel_id = TextField(null=True)
    roles_report_channel_id = TextField(null=True)
    logs_report_channel_id = TextField(null=True)
    mythic_plus_report_channel = TextField(null=True)
    wowhead_channel_id = TextField(null=True)
    roles_assign = ArrayField(TextField, null=True)
    guild = ForeignKeyField(Guild, null=True, on_delete='CASCADE')

    class Meta:
        database = database


class GeneralBotOptions(Model):
    name = TextField()
    value = TextField()

    class Meta:
        database = database
#
#
# Guild.create_table()
# Logs.create_table()
# Messages.create_table(fail_silently=True)
# Discord.create_table()
# GeneralBotOptions.create_table()
