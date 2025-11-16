# -*- coding: utf-8 -*-
from src.trackers.COMMON import COMMON
from src.trackers.UNIT3D import UNIT3D


class IHD(UNIT3D):
    def __init__(self, config):
        super().__init__(config, tracker_name='IHD')
        self.config = config
        self.common = COMMON(config)
        self.tracker = 'IHD'
        self.source_flag = 'InfinityHD'
        self.base_url = 'https://infinityhd.net'
        self.id_url = f'{self.base_url}/api/torrents/'
        self.upload_url = f'{self.base_url}/api/torrents/upload'
        self.search_url = f'{self.base_url}/api/torrents/filter'
        self.torrent_url = f'{self.base_url}/torrents/'
        self.banned_groups = [""]

    async def get_category_id(self, meta):
        if meta.get('anime', False) and meta.get('category', '').upper() == 'MOVIE':
            return {'category_id': '4'}

        if meta.get('anime'):
            return {'category_id': '3'}

        category_id = {
            'MOVIE': '1',
            'TV': '2',
            'Anime': '3',
        }.get(meta.get('category'), '0')

        return {'category_id': category_id}


    async def get_type_id(self, meta):
        type_id = {
            'DISC': '1',
            'REMUX': '2',
            'WEBDL': '4',
            'WEBRIP': '5',
            'HDTV': '6',
            'ENCODE': '3'
        }.get(meta['type'], '0')
        return {'type_id': type_id}

    async def get_resolution_id(self, meta):
        resolution_id = {
            '4320p': '1',
            '2160p': '2',
            '1080p': '3',
            '1080i': '4',
        }.get(meta['resolution'], '10')
        return {'resolution_id': resolution_id}
