import mysql.connector
from datetime import datetime
import config

def add_user(email, username):
  insert_sql = """INSERT INTO qa_users(email, handle, createip, created) VALUES (%s, %s, %s, %s)"""

  try:
    cursor = mydb.cursor()
    cursor.execute(insert_sql, (email, username, '127.0.0.1', datetime.now()))
    mydb.commit()
    cursor.close()
  except mysql.connector.Error as error:
    print("Failed to insert user {}".format(error))


def add_question(userid, title, content):
  insert_sql = """INSERT INTO qa_posts(type, userid, title, content, created) VALUES (%s, %s, %s, %s, %s)"""

  try:
    cursor = mydb.cursor()
    cursor.execute(insert_sql, ('Q', userid, title, content, datetime.now()))
    q_id = cursor.lastrowid
    mydb.commit()
    cursor.close()
  except mysql.connector.Error as error:
    print("Failed to insert user {}".format(error))
  return q_id

def add_answer(userid, question_id, content):
  insert_sql = """INSERT INTO qa_posts(type, userid, parentid, content, created) VALUES (%s, %s, %s, %s, %s)"""
  update_sql = """UPDATE qa_posts SET acount = acount + 1 WHERE postid = %s"""

  try:
    cursor = mydb.cursor()
    cursor.execute(insert_sql, ('A', userid, question_id, content, datetime.now()))
    a_id = cursor.lastrowid

    cursor.execute(update_sql, (question_id, ))

    mydb.commit()
    cursor.close()

  except mysql.connector.Error as error:
    print("Failed to insert user {}".format(error))
  return a_id


mydb = mysql.connector.connect(
  host=config.DB_HOST,
  user=config.DB_USER,
  database=config.DB_NAME,
  password=config.DB_PASSWD
)


#add_user("test@solidcharity.com", "testuser2")
q_id = add_question(4, "Wie installiere ich q2a", "Das wäre schon wichtig, denke ich.")
a_id = add_answer(4, q_id, "Nimm doch einfach Ansible")
if mydb.is_connected():
     mydb.close()



# DONE: add answers
# TODO parse json files
# TODO: increase points
# TODO: add votes
# TODO: add tags
# TODO: use original dates
