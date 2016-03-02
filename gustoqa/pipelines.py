# -*- coding: utf-8 -*-
import os
import hashlib
import base64
import uuid

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.utils.project import get_project_settings
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
