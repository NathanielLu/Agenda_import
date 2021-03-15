import xlrd
from db_table import db_table
import re


def create_database():
    print("Building database")
    sessions = db_table("sessions", {"id": "integer PRIMARY KEY", "date": "text NOT NULL", "startTime": "text NOT NULL",
                                     "endTime": "text NOT NULL", "parentSession": "integer NOT NULL", "title": "text NOT NULL",
                                     "location": "text", "description": "text"})
    speakers = db_table("speakers", {"id": "integer PRIMARY KEY", "name": "text NOT NULL"})
    speaker_for_session = db_table("speaker_for_session", {"id": "integer PRIMARY KEY", "sessionId": "integer NOT NULL",
                                                           "speakerId": "integer NOT NULL"})
    return sessions, speakers, speaker_for_session


def read_file(path, row):
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)

    raw_data = []
    for i in range(row, sheet.nrows):
        raw_data.append(sheet.row_values(i))
    return raw_data


def insert_data(sessions, speakers, speaker_for_session, raw_data):
    print("Inserting...")
    prev_parent_session = -1
    for i in range(len(raw_data)):
        print(raw_data[i])
        date = raw_data[i][0]
        start = raw_data[i][1]
        end = raw_data[i][2]
        if raw_data[i][3] == "Session":
            parent_session = -1
        else:
            parent_session = prev_parent_session

        title = convert_apos(raw_data[i][4])
        location = raw_data[i][5]
        description = convert_apos(raw_data[i][6])
        speaker_list = raw_data[i][7]

        session_id = sessions.insert({"date": date, "startTime": start, "endTime": end, "parentSession": parent_session, "title": title,
                         "location": location, "description": extract_web(description)})
        if raw_data[i][3] == "Session":
            prev_parent_session = session_id
        insert_speaker(session_id, speaker_list, speakers, speaker_for_session)


def insert_speaker(session_id, speaker_list, speakers, speaker_for_session):
    allSpeaker = speaker_list.split(";")
    for speaker_name in allSpeaker:
        if(len(speaker_name) > 0):
            speaker_id = speakers.insert({"name": convert_apos(speaker_name)})
            speaker_for_session.insert({"sessionId": session_id, "speakerId": speaker_id})


def convert_apos(str):
    return str.replace("'", "@")


def extract_web(text):
    tar = re.compile(r'<[^>]+>')
    return tar.sub('', text)


if __name__ == '__main__':
    sessions, speakers, speaker_for_session = create_database()
    raw_data = read_file("agenda.xls", 15)
    insert_data(sessions, speakers, speaker_for_session, raw_data)
