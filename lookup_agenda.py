import sys
from db_table import db_table
import re


# Get sessions, speakers, speaker_for_session tables
def get_tables():
    sessions = db_table("sessions", {"id": "integer PRIMARY KEY", "date": "text NOT NULL", "startTime": "text NOT NULL",
                                     "endTime": "text NOT NULL", "parentSession": "integer NOT NULL",
                                     "title": "text NOT NULL",
                                     "location": "text", "description": "text"})
    speakers = db_table("speakers", {"id": "integer PRIMARY KEY", "name": "text NOT NULL"})
    speaker_for_session = db_table("speaker_for_session", {"id": "integer PRIMARY KEY", "sessionId": "integer NOT NULL",
                                                           "speakerId": "integer NOT NULL"})
    return sessions, speakers, speaker_for_session


# For the given column and field, find the corresponding records in the database
# The column has to be one of the following: date, time_start, time_end, title, location, description, speaker
# It has to be exact match, so the look up function is case sensitive
def find_result(sessions, speakers, speaker_for_session, column, value):
    if column != "date" and column != "time_start" and column != "time_end" and column != "title" \
            and column != "location" and column != "description" and column != "speaker":
        print("The column has to be one of the following: date, time_start, time_end, "
              "title, location, description, speaker")
        exit()

    list = []
    if column == "date":
        list = sessions.select(['id', 'parentSession'], {'date': value})
    elif column == "time_start":
        list = sessions.select(['id', 'parentSession'], {'startTime': value})
    elif column == "time_end":
        list = sessions.select(['id', 'parentSession'], {'endTime': value})
    elif column == "title":
        list = sessions.select(['id', 'parentSession'], {'title': convert_apos(value)})
    elif column == "location":
        list = sessions.select(['id', 'parentSession'], {'location': value})
    elif column == "description":
        list = sessions.select(['id', 'parentSession'], {'description': extract_web(convert_apos(value))})
    elif column == "speaker":
        speaker_ids = speakers.select(['id'], {'name': convert_apos(value)})
        session_ids = []
        for i in range(len(speaker_ids)):
            session_id_list = speaker_for_session.select(['sessionId'], {'speakerId': speaker_ids[i]['id']})
            for item in session_id_list:
                session_ids.append(item['sessionId'])
        for k in session_ids:
            cur_list = sessions.select(['id', 'parentSession'], {'id': k})
            for item in cur_list:
                list.append(item)

    session_set = set()
    for item in list:
        session_set.add(item['id'])

    for item in list:
        if item['parentSession'] == -1:
            subset = sessions.select(['id', 'parentSession'], {'parentSession': item['id']})
            for sub_item in subset:
                session_set.add(sub_item['id'])

    print("The results are:")
    for sid in session_set:
        print(sessions.select(['id', 'date', 'startTime', 'endTime', 'title', 'location'],
                              {'id': sid}))


# Remove useless web tag from the input
def extract_web(text):
    tar = re.compile(r'<[^>]+>')
    return tar.sub('', text)


# Change the ' to be @ so that the sql insert statement can be executed
def convert_apos(str):
    return str.replace("'", "@")


if __name__ == '__main__':
    sessions, speakers, speaker_for_session = get_tables()
    column = sys.argv[1]
    value = sys.argv[2]
    find_result(sessions, speakers, speaker_for_session, column, value)
