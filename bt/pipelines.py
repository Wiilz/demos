# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid
from datetime import datetime
import logging

from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, Date, Text, DateTime
from sqlalchemy.exc import DataError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class BtInfo(Base):
    __tablename__ = 'links'
    id = Column(Integer, autoincrement=True, primary_key=True)
    source_name = Column(String(255))
    create_time = Column(Date)
    source_size = Column(String(16))
    source_link = Column(String(255))
    source_list = Column(Text)
    source_hot = Column(String(8))
    old_link = Column(String(255), unique=True)
    insert_time = Column(DateTime, default=datetime.now)
    item_id = Column(String(64))

    @classmethod
    def create(cls, data):
        instance = cls()
        [setattr(instance, k, v) for k, v in data.items()]
        setattr(instance, 'item_id', str(uuid.uuid1()))
        return instance


class BtPipeline(object):

    def __init__(self):
        self.engine = create_engine('mysql+pymysql://username:password@9.7/btspider?charset=utf8mb4', echo=False)
        self.session = sessionmaker(bind=self.engine)
        self.sess = self.session()
        self.count = 0

    def process_item(self, item, spider):
        try:
            instance = BtInfo.create(item)
            self.sess.add(instance)
            self.sess.commit()
            self.count += 1
        except Exception as e:
            self.sess.rollback()
            print(e)
        print('当前数量: {}'.format(self.count))
        return item

    def close_spider(self, spider):
        self.sess.close()


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://username:password@127.0.1s:3306/btspider?charset=utf8mb4', echo=True)  # 连接数据
    Base.metadata.create_all(engine)
    p = BtPipeline()
    try:
        print('start query')
        ress = p.sess.query(BtInfo).all()
        print('query finished')
        for res in ress:
            res.item_id = str(uuid.uuid1())
            print(res.id)
        p.sess.add_all(ress)
        p.sess.commit()
    except Exception as e:
        p.sess.rollback()
        raise e






