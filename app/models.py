# coding: utf-8
from app import db


class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = (
        db.Index('comments_order_idx', 'domain_id', 'modified_at'),
        db.Index('comments_nametype_index', 'name', 'type')
    )

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.ForeignKey('domains.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                          index=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    modified_at = db.Column(db.Integer, nullable=False)
    account = db.Column(db.String(40), server_default=db.FetchedValue())
    comment = db.Column(db.String(65535), nullable=False)

    domain = db.relationship('Domain', primaryjoin='Comment.domain_id == Domain.id', backref='comments')


class Cryptokey(db.Model):
    __tablename__ = 'cryptokeys'

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.ForeignKey('domains.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                          index=True)
    flags = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean)
    content = db.Column(db.Text)

    domain = db.relationship('Domain', primaryjoin='Cryptokey.domain_id == Domain.id', backref='cryptokeys')


class Domainmetadatum(db.Model):
    __tablename__ = 'domainmetadata'

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.ForeignKey('domains.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                          index=True)
    kind = db.Column(db.String(32))
    content = db.Column(db.Text)

    domain = db.relationship('Domain', primaryjoin='Domainmetadatum.domain_id == Domain.id', backref='domainmetadata')


class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    master = db.Column(db.String(128), server_default=db.FetchedValue())
    last_check = db.Column(db.Integer, server_default=db.FetchedValue())
    type = db.Column(db.String(6), nullable=False)
    notified_serial = db.Column(db.Integer, server_default=db.FetchedValue())
    account = db.Column(db.String(40), server_default=db.FetchedValue())


class Record(db.Model):
    __tablename__ = 'records'
    __table_args__ = (
        db.Index('nametype_index', 'name', 'type'),
    )

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.ForeignKey('domains.id', ondelete='CASCADE', onupdate='CASCADE'), index=True,
                          server_default=db.FetchedValue())
    name = db.Column(db.String(255), index=True, server_default=db.FetchedValue())
    type = db.Column(db.String(10), server_default=db.FetchedValue())
    content = db.Column(db.String(65535), server_default=db.FetchedValue())
    ttl = db.Column(db.Integer, server_default=db.FetchedValue())
    prio = db.Column(db.Integer, server_default=db.FetchedValue())
    disabled = db.Column(db.Boolean, server_default=db.FetchedValue())
    ordername = db.Column(db.String(255), index=True)
    auth = db.Column(db.Boolean, server_default=db.FetchedValue())

    domain = db.relationship('Domain',
                             primaryjoin='Record.domain_id == Domain.id',
                             backref='records',
                             )


t_supermasters = db.Table(
    'supermasters',
    db.Column('ip', db.String(64), nullable=False),
    db.Column('nameserver', db.String(255), nullable=False),
    db.Column('account', db.String(40), nullable=False),
    db.Index('ip_nameserver_pk', 'ip', 'nameserver')
)


class Tsigkey(db.Model):
    __tablename__ = 'tsigkeys'
    __table_args__ = (
        db.Index('namealgoindex', 'name', 'algorithm'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    algorithm = db.Column(db.String(50))
    secret = db.Column(db.String(255))
