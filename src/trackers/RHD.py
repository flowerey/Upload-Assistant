# -*- coding: utf-8 -*-
from typing import Any, Dict
from src.trackers.COMMON import COMMON
from src.trackers.UNIT3D import UNIT3D

class RHD(UNIT3D):
    def __init__(self, config):
        super().__init__(config, tracker_name='RHD')
        self.config = config
        self.common = COMMON(config)
        self.tracker = 'RHD'
        self.source_flag = 'RocketHD'
        self.base_url = 'https://rocket-hd.cc'
        self.id_url = f'{self.base_url}/api/torrents/'
        self.upload_url = f'{self.base_url}/api/torrents/upload'
        self.requests_url = f'{self.base_url}/api/requests/filter'
        self.search_url = f'{self.base_url}/api/torrents/filter'
        self.torrent_url = f'{self.base_url}/torrents/'
        self.banned_groups = [
            "1XBET",
            "MEGA",
            "MTZ",
            "Whistler",
            "WOTT",
            "Taylor.D",
            "HELD",
            "FSX",
            "FuN",
            "MagicX",
            "w00t",
            "PaTroL",
            "BB",
            "266ers",
            "GTF",
            "JellyfinPlex",
            "2BA",
            "Mic",
            "LD",
            "CAM",
            "TS",
        ]
        self.allowed_imghosts = []
        pass

    def _detect_german(self, meta: Dict[str, Any]) -> str:
        mi = meta.get("mediainfo", {})
        if not mi:
            return ""
        tracks = mi.get("media", {}).get("track", [])
        if not isinstance(tracks, list):
            tracks = []

        german_audio = False
        other_audio_langs = set()
        german_text = False

        for t in tracks:
            typ = t.get("@type", "").lower()
            lang = str(t.get("Language", "")).lower()
            title = str(t.get("Title", "")).lower()

            is_commentary = "comment" in title or "review" in title
            is_nonverbal = lang == "zxx" or "score" in title

            if typ == "audio" and not is_commentary and not is_nonverbal:
                if lang in {"de", "ger", "deu"} or "german" in title:
                    german_audio = True
                else:
                    other_audio_langs.add(lang)

            if typ == "text":
                if lang in {"de", "ger", "deu"} or "german" in title:
                    german_text = True

        if german_text and not german_audio:
            return "GERMAN SUBBED"
        if german_audio:
            if len(other_audio_langs) >= 2:
                return "GERMAN ML"
            elif len(other_audio_langs) == 1:
                return "GERMAN DL"
            else:
                return "GERMAN"
        return ""

    def _build_overrides(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        overrides: Dict[str, Any] = {}

        overrides["lang"] = self._detect_german(meta)

        if meta.get("original_language") == "de":
            overrides["title"] = meta.get("original_title") or meta.get("Title", "")

        else:
            akas = meta.get("imdb_info", {}).get("akas", [])
            ger_title = None

            for aka in akas:
                if aka.get("language") == "de":
                    ger_title = aka["title"]
                    break

            if ger_title:
                main_title = meta.get("original_title", "")
                if ger_title.strip().lower() != main_title.strip().lower():
                    overrides["title"] = f"{ger_title} AKA {main_title}"
                else:
                    overrides["title"] = ger_title
            else:
                aka = meta.get("aka", "")
                if aka:
                    aka = f" AKA {aka}"
                overrides["title"] = f"{meta.get('original_title', '')}{aka}"

        tag = meta.get("tag", "")
        if not tag:
            tag = "NOGRP"
        overrides["tag"] = tag

        return overrides

    async def get_name(self, meta: Dict[str, Any]) -> Dict[str, str]:
        rhd_name = meta['name']
        lang_tag = self._detect_german(meta)

        if lang_tag:
            resolution = meta.get('resolution', '')
            if resolution and resolution in rhd_name:
                rhd_name = rhd_name.replace(resolution, f"{lang_tag} {resolution}", 1)
            else:
                rhd_name = f"{lang_tag} {rhd_name}"

        overrides = self._build_overrides(meta)
        if 'title' in overrides:
            original_title = meta.get('title', '')
            new_title = overrides['title']
            if original_title and new_title:
                rhd_name = rhd_name.replace(original_title, new_title, 1)

        rhd_name = ' '.join(rhd_name.split())

        return {'name': rhd_name}

    async def get_category_id(self, meta):
        category_id = {
            'MOVIE': '1',
            'TV': '2',
        }.get(meta['category'], '0')
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
            '720p': '5',
            '576p': '12',
            '576i': '13',
            '480p': '11',
            '384p': '14'
        }.get(meta['resolution'], '10')
        return {'resolution_id': resolution_id}

    async def get_additional_data(self, meta):
        data = {
            'modq': await self.get_flag(meta, 'modq'),
        }

        return data
