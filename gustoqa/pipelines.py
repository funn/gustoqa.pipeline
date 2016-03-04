# -*- coding: utf-8 -*-
import os
import hashlib
import base64
import uuid

from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet.threads import deferToThread
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request, signals
from scrapy.utils.project import get_project_settings
from kombu.connection import Connection


SETTINGS = get_project_settings()


class GustoqaImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return os.path.join(request.meta.get('basedir'), request.meta.get('image_name'))

    def get_media_requests(self, item, info):
        basedir = os.path.join(SETTINGS['IMAGES_STORE'], base64.urlsafe_b64encode(hashlib.md5(item['url']).digest()))
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        for image_url, index in item['image_urls'].iteritems():
            yield Request(image_url, meta={'image_name': str(uuid.uuid4())+'.jpg', 'basedir': base64.urlsafe_b64encode(hashlib.md5(item['url']).digest())})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            pass  # TODO: come up with something here.
        return item


class MessageQueuePipeline(object):
    """Emit processed items to a RabbitMQ exchange/queue"""
    def __init__(self, host_name, port, userid, password, virtual_host, encoder_class):
        self.connection = Connection(hostname=host_name, port=port,
                        userid=userid, password=password,
                        virtual_host=virtual_host)
        self.encoder = encoder_class()
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_settings(cls, settings):
        host_name = settings.get('BROKER_HOST')
        port = settings.get('BROKER_PORT')
        userid = settings.get('BROKER_USERID')
        password = settings.get('BROKER_PASSWORD')
        virtual_host = settings.get('BROKER_VIRTUAL_HOST')
        encoder_class = settings.get('MESSAGE_Q_SERIALIZER', ScrapyJSONEncoder)
        return cls(host_name, port, userid, password, virtual_host, encoder_class)

    def spider_opened(self, spider):
        self.queue = self.connection.SimpleQueue(spider.name)

    def spider_closed(self, spider):
        self.queue.close()
        self.connection.close()

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        self.queue.put(self.encoder.encode(dict(item)))
        return item
