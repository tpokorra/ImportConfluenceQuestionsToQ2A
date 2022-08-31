from datetime import datetime
import json
import codecs
from q2a_models import *
from types import SimpleNamespace
import os

def add_user(orig_id, email, username, date_created):
    user = QaUsers.get_or_none(handle = username)
    if not user:
        user = QaUsers.create(createip = orig_id, handle=username, email=email, created=date_created)
    else:
        user.email = email
        user.handle = username
        user.save()
    return user.userid


def add_question(orig_id, userid, title, content, date_created):
    question = QaPosts.get_or_none(createip = orig_id)
    if not question:
        question = QaPosts.create(createip = orig_id, type='Q', userid = userid, title=title, format='html', content=content, created=date_created)
    else:
        question.title = title
        question.content = content
        question.save()
    return question.postid

def add_answer(orig_id, userid, question_id, content, date_created):
    answer, created = QaPosts.get_or_create(createip = orig_id, defaults =
            {'type': 'A',
             'userid': userid,
             'parentid': question_id,
             'format': 'html',
             'content': content,
             'created': date_created})

    if not created:
        answer.content = content
        answer.save()
    else:
        # increase answer count
        question = QaPosts.get(postid=answer.parentid)
        question.acount += 1
        question.save()

    return answer.postid


def add_tag(name):
    word, created = QaWords.get_or_create(word=name, defaults={'tagwordcount': 1, 'tagcount': 1})
    if created:
        word.tagwordcount += 1
        word.tagcount += 1
        word.save()
    return word.wordid


def link_tag_to_post(q_id, t_id, name):
    tw, created = QaTagwords.get_or_create(postid=q_id, wordid=t_id)
    pt, created = QaPosttags.get_or_create(postid=q_id, wordid=t_id, defaults={'postcreated': datetime.now()})
    post = QaPosts.get(postid=q_id)
    if post.tags is not None and name in post.tags.split(","):
        return
    if post.tags is None:
        post.tags = ""
    else:
        post.tags += ','
    post.tags+=name
    post.save()


def set_votes(p_id, up, down):
    if up or down:
        post = QaPosts.get(postid=p_id)
        post.upvotes = up
        post.downvotes = down
        post.netvotes = up - down
        post.save()


def quick_test():
    u_id = add_user(1234, "test@solidcharity.com", "testuser2", datetime.now())
    q_id = add_question(123, u_id, "Wie installiere ich q2a", "Das wäre schon wichtig, denke ich.", datetime.now())
    a_id = add_answer(124, u_id, q_id, "Nimm doch einfach Ansible", datetime.now())


def pseudo_json_to_json(code, attributes):
    # drop leading @
    code = code[1:]
    # replace quotes
    code = code.replace('"', "&quot;")

    for attribute in attributes:
        # not first attributes
        code = code.replace('; ' + attribute + '=', '", "' + attribute + '": "')
        # first attribute
        code = code.replace(attribute + '=', '"' + attribute + '": "')

    # add last quote for value
    code = code[:-1] + '"}'

    # replace backslash with double backslash
    code = code.replace("\\", "\\\\")

    return code

def import_from_json_file(filename):

    if "samples" in filename:
        f = open(filename)
        content = f.read()
        f.close()
    else:
        # see https://stackoverflow.com/questions/22459020/python-decode-utf-16-file-with-bom
        encoded_text = open(filename, 'rb').read()
        bom = codecs.BOM_UTF16_LE
        assert encoded_text.startswith(bom)
        encoded_text = encoded_text[len(bom):]
        content = encoded_text.decode('utf-16')

    data = json.loads(content, object_hook=lambda d: SimpleNamespace(**d))

    u_id = add_user(data.author.userKey, data.author.email, data.author.name, datetime.now())
    q_id = add_question(data.id, u_id, data.title, data.body.content, datetime.fromtimestamp(data.dateAsked/1000))
    set_votes(q_id, int(data.votes.up), int(data.votes.down))
    for answer in data.answers:
        author_str = pseudo_json_to_json(answer.author, {'name', 'fullName', 'avatarDownloadPath', 'email', 'userKey'})
        author = json.loads(author_str, object_hook=lambda d: SimpleNamespace(**d), strict=False)
        body_str = pseudo_json_to_json(answer.body, {'content', 'bodyFormat'})
        body = json.loads(body_str, object_hook=lambda d: SimpleNamespace(**d), strict=False)
        a_u_id = add_user(author.userKey, author.email, author.name, datetime.now())
        a_id = add_answer(answer.id, a_u_id, q_id, body.content, datetime.fromtimestamp(answer.dateAnswered/1000))
        votes_str = pseudo_json_to_json(answer.votes, {'up', 'down', 'total', 'upVoted', 'downVoted'})
        votes = json.loads(votes_str, object_hook=lambda d: SimpleNamespace(**d), strict=False)
        set_votes(a_id, int(votes.up), int(votes.down))
        if answer.accepted:
            # selected answer
            question = QaPosts.get(postid=q_id)
            question.selchildid = a_id
            question.save()
    for topic in data.topics:
        print(topic)
        t_id = add_tag(topic.name)
        link_tag_to_post(q_id, t_id, topic.name)

#quick_test()
#import_from_json_file("samples/sample01.json")

if os.path.isdir('questions'):
    dirs = os.listdir('questions')
    for file in dirs:
        print(file)
        import_from_json_file('questions/' + file)

# DONE: add answers
# DONE parse json files
# DONE: use original dates
# DONE: add votes
# DONE: add tags
# TODO: increase points
