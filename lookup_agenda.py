from db_table import db_table
import re


def get_tables():
    sessions = db_table("sessions", {"id": "integer PRIMARY KEY", "date": "text NOT NULL", "startTime": "text NOT NULL",
                                     "endTime": "text NOT NULL", "parentSession": "integer NOT NULL",
                                     "title": "text NOT NULL",
                                     "location": "text", "description": "text"})
    speakers = db_table("speakers", {"id": "integer PRIMARY KEY", "name": "text NOT NULL"})
    speaker_for_session = db_table("speaker_for_session", {"id": "integer PRIMARY KEY", "sessionId": "integer NOT NULL",
                                                           "speakerId": "integer NOT NULL"})
    return sessions, speakers, speaker_for_session


def find_result(sessions, speakers, speaker_for_session, column, value):
    list = []
    if column == "date":
        list = sessions.select(['id', 'parentSession'], {'date': value})
    elif column == "time_start":
        list = sessions.select(['id', 'parentSession'], {'startTime': value})
    elif column == "time_end":
        list = sessions.select(['id', 'parentSession'], {'endTime': value})
    elif column == "title":
        list = sessions.select(['id', 'parentSession'], {'title': value})
    elif column == "location":
        list = sessions.select(['id', 'parentSession'], {'location': value})
    elif column == "description":
        list = sessions.select(['id', 'parentSession'], {'description': extract_web(value)})
    elif column == "speaker":
        speaker_ids = speakers.select(['id'], {'name': value})
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

    print(session_set)


def extract_web(text):
    tar = re.compile(r'<[^>]+>')
    return tar.sub('', text)


def convert_apos(str):
    return str.replace("'", "@")


if __name__ == '__main__':
    sessions, speakers, speaker_for_session = get_tables()
    column = "speaker"
    value = "Jiaqi Zhang"
    find_result(sessions, speakers, speaker_for_session, column, value)
