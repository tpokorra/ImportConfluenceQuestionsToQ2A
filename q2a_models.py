# generated with: python -m pwiz -e mysql tim03_q2a -u tim03_q2a --password > q2a_models.py

from peewee import *
import config

database = MySQLDatabase(config.DB_NAME, **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'user': config.DB_USER, 'password': config.DB_PASSWD})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class QaBlobs(BaseModel):
    blobid = BigAutoField()
    content = TextField(null=True)
    cookieid = BigIntegerField(null=True)
    created = DateTimeField(null=True)
    createip = CharField(null=True)
    filename = CharField(null=True)
    format = CharField()
    userid = IntegerField(null=True)

    class Meta:
        table_name = 'qa_blobs'

class QaCache(BaseModel):
    cacheid = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    content = TextField()
    created = DateTimeField()
    lastread = DateTimeField(index=True)
    type = CharField()

    class Meta:
        table_name = 'qa_cache'
        indexes = (
            (('type', 'cacheid'), True),
        )
        primary_key = CompositeKey('cacheid', 'type')

class QaCategories(BaseModel):
    backpath = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    categoryid = AutoField()
    content = CharField(constraints=[SQL("DEFAULT ''")])
    parentid = IntegerField(null=True)
    position = IntegerField()
    qcount = IntegerField(constraints=[SQL("DEFAULT 0")])
    tags = CharField()
    title = CharField()

    class Meta:
        table_name = 'qa_categories'
        indexes = (
            (('parentid', 'position'), True),
            (('parentid', 'tags'), True),
        )

class QaCategorymetas(BaseModel):
    categoryid = ForeignKeyField(column_name='categoryid', field='categoryid', model=QaCategories)
    content = CharField()
    title = CharField()

    class Meta:
        table_name = 'qa_categorymetas'
        indexes = (
            (('categoryid', 'title'), True),
        )
        primary_key = CompositeKey('categoryid', 'title')

class QaUsers(BaseModel):
    avatarblobid = BigIntegerField(null=True)
    avatarheight = IntegerField(null=True)
    avatarwidth = IntegerField(null=True)
    created = DateTimeField()
    createip = CharField()
    email = CharField(index=True)
    emailcode = CharField(constraints=[SQL("DEFAULT ''")])
    flags = IntegerField(constraints=[SQL("DEFAULT 0")])
    handle = CharField(index=True)
    level = IntegerField(index=True)
    loggedin = DateTimeField()
    loginip = CharField()
    passcheck = CharField(null=True)
    passhash = CharField(null=True)
    passsalt = CharField(null=True)
    sessioncode = CharField(constraints=[SQL("DEFAULT ''")])
    sessionsource = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    userid = AutoField()
    wallposts = IntegerField(constraints=[SQL("DEFAULT 0")])
    writeip = CharField(null=True)
    written = DateTimeField(null=True)

    class Meta:
        table_name = 'qa_users'
        indexes = (
            (('created', 'level', 'flags'), False),
        )

class QaPosts(BaseModel):
    acount = IntegerField(constraints=[SQL("DEFAULT 0")])
    amaxvote = IntegerField(constraints=[SQL("DEFAULT 0")])
    categoryid = ForeignKeyField(column_name='categoryid', field='categoryid', model=QaCategories, null=True)
    catidpath1 = IntegerField(null=True)
    catidpath2 = IntegerField(null=True)
    catidpath3 = IntegerField(null=True)
    closedbyid = ForeignKeyField(column_name='closedbyid', field='postid', model='self', null=True)
    content = CharField(null=True)
    cookieid = BigIntegerField(null=True)
    created = DateTimeField()
    createip = BlobField(null=True)
    downvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    flagcount = IntegerField(constraints=[SQL("DEFAULT 0")])
    format = CharField(constraints=[SQL("DEFAULT ''")])
    hotness = FloatField(null=True)
    lastip = BlobField(null=True)
    lastuserid = IntegerField(null=True)
    lastviewip = BlobField(null=True)
    name = CharField(null=True)
    netvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    notify = CharField(null=True)
    parentid = ForeignKeyField(backref='qa_posts_parentid_set', column_name='parentid', field='postid', model='self', null=True)
    postid = AutoField()
    selchildid = IntegerField(null=True)
    tags = CharField(null=True)
    title = CharField(null=True)
    type = CharField()
    updated = DateTimeField(null=True)
    updatetype = CharField(null=True)
    upvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers, null=True)
    views = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'qa_posts'
        indexes = (
            (('categoryid', 'type', 'created'), False),
            (('categoryid', 'updated', 'type'), False),
            (('catidpath1', 'type', 'created'), False),
            (('catidpath1', 'updated', 'type'), False),
            (('catidpath2', 'type', 'created'), False),
            (('catidpath2', 'updated', 'type'), False),
            (('catidpath3', 'type', 'created'), False),
            (('catidpath3', 'updated', 'type'), False),
            (('createip', 'created'), False),
            (('flagcount', 'created', 'type'), False),
            (('lastip', 'updated', 'type'), False),
            (('lastuserid', 'updated', 'type'), False),
            (('parentid', 'type'), False),
            (('selchildid', 'type', 'created'), False),
            (('type', 'acount', 'created'), False),
            (('type', 'amaxvote', 'created'), False),
            (('type', 'created'), False),
            (('type', 'hotness'), False),
            (('type', 'netvotes', 'created'), False),
            (('type', 'views', 'created'), False),
            (('updated', 'type'), False),
            (('userid', 'type', 'created'), False),
        )

class QaWords(BaseModel):
    contentcount = IntegerField(constraints=[SQL("DEFAULT 0")])
    tagcount = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    tagwordcount = IntegerField(constraints=[SQL("DEFAULT 0")])
    titlecount = IntegerField(constraints=[SQL("DEFAULT 0")])
    word = CharField(index=True)
    wordid = AutoField()

    class Meta:
        table_name = 'qa_words'

class QaContentwords(BaseModel):
    count = IntegerField()
    postid = ForeignKeyField(column_name='postid', field='postid', model=QaPosts)
    questionid = IntegerField()
    type = CharField()
    wordid = ForeignKeyField(column_name='wordid', field='wordid', model=QaWords)

    class Meta:
        table_name = 'qa_contentwords'
        primary_key = False

class QaCookies(BaseModel):
    cookieid = BigAutoField()
    created = DateTimeField()
    createip = CharField()
    writeip = CharField(null=True)
    written = DateTimeField(null=True)

    class Meta:
        table_name = 'qa_cookies'

class QaIplimits(BaseModel):
    action = CharField()
    count = IntegerField()
    ip = CharField()
    period = IntegerField()

    class Meta:
        table_name = 'qa_iplimits'
        indexes = (
            (('ip', 'action'), True),
        )
        primary_key = False

class QaMessages(BaseModel):
    content = CharField()
    created = DateTimeField()
    format = CharField()
    fromhidden = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    fromuserid = ForeignKeyField(column_name='fromuserid', field='userid', model=QaUsers, null=True)
    messageid = AutoField()
    tohidden = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    touserid = ForeignKeyField(backref='qa_users_touserid_set', column_name='touserid', field='userid', model=QaUsers, null=True)
    type = CharField(constraints=[SQL("DEFAULT 'PRIVATE'")])

    class Meta:
        table_name = 'qa_messages'
        indexes = (
            (('touserid', 'type', 'created'), False),
            (('type', 'fromuserid', 'touserid', 'created'), False),
        )

class QaOptions(BaseModel):
    content = CharField()
    title = CharField(primary_key=True)

    class Meta:
        table_name = 'qa_options'

class QaPages(BaseModel):
    content = TextField(null=True)
    flags = IntegerField()
    heading = CharField(null=True)
    nav = CharField()
    pageid = AutoField()
    permit = IntegerField(null=True)
    position = IntegerField(unique=True)
    tags = CharField(index=True)
    title = CharField()

    class Meta:
        table_name = 'qa_pages'

class QaPostmetas(BaseModel):
    content = CharField()
    postid = ForeignKeyField(column_name='postid', field='postid', model=QaPosts)
    title = CharField()

    class Meta:
        table_name = 'qa_postmetas'
        indexes = (
            (('postid', 'title'), True),
        )
        primary_key = CompositeKey('postid', 'title')

class QaPosttags(BaseModel):
    postcreated = DateTimeField()
    postid = ForeignKeyField(column_name='postid', field='postid', model=QaPosts)
    wordid = ForeignKeyField(column_name='wordid', field='wordid', model=QaWords)

    class Meta:
        table_name = 'qa_posttags'
        indexes = (
            (('wordid', 'postcreated'), False),
        )
        primary_key = False

class QaSharedevents(BaseModel):
    entityid = IntegerField()
    entitytype = CharField()
    lastpostid = IntegerField()
    lastuserid = IntegerField(null=True)
    questionid = IntegerField()
    updated = DateTimeField()
    updatetype = CharField(null=True)

    class Meta:
        table_name = 'qa_sharedevents'
        indexes = (
            (('entitytype', 'entityid', 'updated'), False),
            (('questionid', 'entitytype', 'entityid'), False),
        )
        primary_key = False

class QaTagmetas(BaseModel):
    content = CharField()
    tag = CharField()
    title = CharField()

    class Meta:
        table_name = 'qa_tagmetas'
        indexes = (
            (('tag', 'title'), True),
        )
        primary_key = CompositeKey('tag', 'title')

class QaTagwords(BaseModel):
    postid = ForeignKeyField(column_name='postid', field='postid', model=QaPosts)
    wordid = ForeignKeyField(column_name='wordid', field='wordid', model=QaWords)

    class Meta:
        table_name = 'qa_tagwords'
        primary_key = False

class QaTitlewords(BaseModel):
    postid = ForeignKeyField(column_name='postid', field='postid', model=QaPosts)
    wordid = ForeignKeyField(column_name='wordid', field='wordid', model=QaWords)

    class Meta:
        table_name = 'qa_titlewords'
        primary_key = False

class QaUserevents(BaseModel):
    entityid = IntegerField()
    entitytype = CharField()
    lastpostid = IntegerField()
    lastuserid = IntegerField(null=True)
    questionid = IntegerField()
    updated = DateTimeField()
    updatetype = CharField(null=True)
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_userevents'
        indexes = (
            (('questionid', 'userid'), False),
            (('userid', 'updated'), False),
        )
        primary_key = False

class QaUserfavorites(BaseModel):
    entityid = IntegerField()
    entitytype = CharField()
    nouserevents = IntegerField()
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_userfavorites'
        indexes = (
            (('entitytype', 'entityid', 'nouserevents'), False),
            (('userid', 'entitytype', 'entityid'), True),
            (('userid', 'nouserevents'), False),
        )
        primary_key = CompositeKey('entityid', 'entitytype', 'userid')

class QaUserfields(BaseModel):
    content = CharField(null=True)
    fieldid = AutoField()
    flags = IntegerField()
    permit = IntegerField(null=True)
    position = IntegerField()
    title = CharField()

    class Meta:
        table_name = 'qa_userfields'

class QaUserlevels(BaseModel):
    entityid = IntegerField()
    entitytype = CharField()
    level = IntegerField(null=True)
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_userlevels'
        indexes = (
            (('entitytype', 'entityid'), False),
            (('userid', 'entitytype', 'entityid'), True),
        )
        primary_key = False

class QaUserlimits(BaseModel):
    action = CharField()
    count = IntegerField()
    period = IntegerField()
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_userlimits'
        indexes = (
            (('userid', 'action'), True),
        )
        primary_key = False

class QaUserlogins(BaseModel):
    identifier = CharField()
    identifiermd5 = CharField()
    source = CharField()
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_userlogins'
        indexes = (
            (('source', 'identifiermd5'), False),
        )
        primary_key = False

class QaUsermetas(BaseModel):
    content = CharField()
    title = CharField()
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_usermetas'
        indexes = (
            (('userid', 'title'), True),
        )
        primary_key = CompositeKey('title', 'userid')

class QaUsernotices(BaseModel):
    content = CharField()
    created = DateTimeField()
    format = CharField()
    noticeid = AutoField()
    tags = CharField(null=True)
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_usernotices'
        indexes = (
            (('userid', 'created'), False),
        )

class QaUserpoints(BaseModel):
    adownvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    aposts = IntegerField(constraints=[SQL("DEFAULT 0")])
    aselecteds = IntegerField(constraints=[SQL("DEFAULT 0")])
    aselects = IntegerField(constraints=[SQL("DEFAULT 0")])
    aupvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    avoteds = IntegerField(constraints=[SQL("DEFAULT 0")])
    bonus = IntegerField(constraints=[SQL("DEFAULT 0")])
    cdownvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    cposts = IntegerField(constraints=[SQL("DEFAULT 0")])
    cupvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    cvoteds = IntegerField(constraints=[SQL("DEFAULT 0")])
    downvoteds = IntegerField(constraints=[SQL("DEFAULT 0")])
    points = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    qdownvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    qposts = IntegerField(constraints=[SQL("DEFAULT 0")])
    qupvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    qvoteds = IntegerField(constraints=[SQL("DEFAULT 0")])
    upvoteds = IntegerField(constraints=[SQL("DEFAULT 0")])
    userid = AutoField()

    class Meta:
        table_name = 'qa_userpoints'

class QaUserprofile(BaseModel):
    content = CharField()
    title = CharField()
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)

    class Meta:
        table_name = 'qa_userprofile'
        indexes = (
            (('userid', 'title'), True),
        )
        primary_key = False

class QaUservotes(BaseModel):
    flag = IntegerField()
    postid = ForeignKeyField(column_name='postid', field='postid', model=QaPosts)
    userid = ForeignKeyField(column_name='userid', field='userid', model=QaUsers)
    vote = IntegerField()
    votecreated = DateTimeField(null=True)
    voteupdated = DateTimeField(null=True)

    class Meta:
        table_name = 'qa_uservotes'
        indexes = (
            (('userid', 'postid'), True),
            (('votecreated', 'voteupdated'), False),
        )
        primary_key = False

class QaWidgets(BaseModel):
    place = CharField()
    position = IntegerField(unique=True)
    tags = CharField()
    title = CharField()
    widgetid = AutoField()

    class Meta:
        table_name = 'qa_widgets'

