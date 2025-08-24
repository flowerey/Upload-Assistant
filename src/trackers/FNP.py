# -*- coding: utf-8 -*-
import asyncio
import requests
import platform
import os
import glob
import httpx
import json

from src.trackers.COMMON import COMMON
from src.console import console


class FNP:
    """
    Handles all operations for the FearNoPeer (FNP) tracker.

    Includes methods for setting metadata IDs, searching for duplicates,
    and uploading torrents via the tracker's API.
    """

    def __init__(self, config):
        self.config = config
        self.tracker = 'FNP'
        self.source_flag = 'FnP'
        self.upload_url = 'https://fearnopeer.com/api/torrents/upload'
        self.search_url = 'https://fearnopeer.com/api/torrents/filter'
        self.torrent_url = 'https://fearnopeer.com/torrents/'
        self.signature = "\n[center][url=https://github.com/Audionut/Upload-Assistant]Created by Audionut's Upload Assistant[/url][/center]"
        self.banned_groups = ["4K4U", "BiTOR", "d3g", "FGT", "FRDS", "FTUApps", "GalaxyRG", "LAMA", "MeGusta", "NeoNoir", "PSA", "RARBG", "YAWNiX", "YTS", "YIFY", "x0r"]

    async def get_cat_id(self, category_name):
        category_id = {
            'MOVIE': '1',
            'TV': '2',
        }.get(category_name, '0')
        return category_id

    async def get_type_id(self, type_name):
        type_id = {
            'DISC': '1',
            'REMUX': '2',
            'WEBDL': '4',
            'WEBRIP': '5',
            'HDTV': '6',
            'SDTV': '7',
            'DVDRIP': '3',
            'ENCODE': '3',
        }.get(type_name, '0')
        return type_id

    async def get_res_id(self, resolution, disctype):
        # This mapping is used for file-based resolutions
        resolution_mapping = {
            '4320p': '1',
            '2160p': '2',
            '1080p': '3',
            '1080i': '11',
            '720p': '5',
            '576p': '6',
            '576i': '15',
            '480p': '8',
            '480i': '14',
            'DVD': '14', # DVD is hardcoded but included for clarity
        }
        
        # Prioritize physical media types first
        if disctype == 'DVD':
            return '14'
        elif disctype == 'BD':
            # This handles various Blu-ray resolutions and defaults to 1080p if not found
            return resolution_mapping.get(resolution, '3')
        
        # Fallback for all other types (e.g., WEB-DL, HD-TV)
        return resolution_mapping.get(resolution, '10')

    async def upload(self, meta, disctype):
        common = COMMON(config=self.config)
        await common.edit_torrent(meta, self.tracker, self.source_flag)

        cat_id = await self.get_cat_id(meta['category'])
        type_id = await self.get_type_id(meta['type'])
        resolution_id = await self.get_res_id(meta['resolution'], disctype)

        await common.unit3d_edit_desc(meta, self.tracker, self.signature)
        region_id = await common.unit3d_region_ids(meta.get('region'))
        distributor_id = await common.unit3d_distributor_ids(meta.get('distributor'))
        
        anon = 1 if meta.get('anon', 1) or self.config['TRACKERS'][self.tracker].get('anon', False) else 0

        with open(f"{meta['base_dir']}/tmp/{meta['uuid']}/[{self.tracker}].torrent", 'rb') as open_torrent:
            files = {'torrent': open_torrent}

            mi_dump, bd_dump = None, None
            if meta['bdinfo'] is not None:
                with open(f"{meta['base_dir']}/tmp/{meta['uuid']}/BD_SUMMARY_00.txt", 'r', encoding='utf-8') as bd_f:
                    bd_dump = bd_f.read()
            else:
                with open(f"{meta['base_dir']}/tmp/{meta['uuid']}/MEDIAINFO.txt", 'r', encoding='utf-8') as mi_f:
                    mi_dump = mi_f.read()

            with open(f"{meta['base_dir']}/tmp/{meta['uuid']}/[{self.tracker}]DESCRIPTION.txt", 'r', encoding='utf-8') as desc_f:
                desc = desc_f.read()

            nfo_file_path = os.path.join(meta['base_dir'], "tmp", meta['uuid'], "*.nfo")
            nfo_files = glob.glob(nfo_file_path)
            if nfo_files:
                with open(nfo_files[0], 'rb') as nfo_f:
                    files['nfo'] = ("nfo_file.nfo", nfo_f, "text/plain")

            data = {
                'name': meta['name'],
                'description': desc,
                'mediainfo': mi_dump,
                'bdinfo': bd_dump,
                'category_id': cat_id,
                'type_id': type_id,
                'resolution_id': resolution_id,
                'tmdb': meta['tmdb'],
                'imdb': meta['imdb'],
                'tvdb': meta['tvdb_id'],
                'mal': meta['mal_id'],
                'igdb': 0,
                'anonymous': anon,
                'stream': meta['stream'],
                'sd': meta['sd'],
                'keywords': meta['keywords'],
                'personal_release': int(meta.get('personalrelease', False)),
                'internal': 0,
                'featured': 0,
                'free': 0,
                'doubleup': 0,
                'sticky': 0,
            }

            if self.config['TRACKERS'][self.tracker].get('internal', False) and meta['tag'][1:] in self.config['TRACKERS'][self.tracker].get('internal_groups', []):
                data['internal'] = 1

            if region_id != 0:
                data['region_id'] = region_id
            if distributor_id != 0:
                data['distributor_id'] = distributor_id
            if meta.get('category') == "TV":
                data['season_number'] = meta.get('season_int', '0')
                data['episode_number'] = meta.get('episode_int', '0')

            headers = {'User-Agent': f'Upload Assistant/2.2 ({platform.system()} {platform.release()})'}
            params = {'api_token': self.config['TRACKERS'][self.tracker]['api_key'].strip()}

            if not meta['debug']:
                try:
                    response = requests.post(url=self.upload_url, files=files, data=data, headers=headers, params=params, timeout=5)
                    response.raise_for_status()

                    response_json = response.json()
                    t_id = response_json['data'].split(".")[1].split("/")[3]

                    meta['tracker_status'][self.tracker]['torrent_id'] = t_id
                    meta['tracker_status'][self.tracker]['status_message'] = "Upload successful."

                    await common.add_tracker_torrent(meta, self.tracker, self.source_flag, self.config['TRACKERS'][self.tracker].get('announce_url'), f"https://fearnopeer.com/torrents/{t_id}")
                except requests.exceptions.HTTPError as err:
                    console.print(f"[bold red]Upload failed with HTTP error: {err}[/bold red]")
                    meta['tracker_status'][self.tracker]['status_message'] = f"HTTP Error: {err}"
                except json.JSONDecodeError:
                    console.print("[bold red]Upload failed: Invalid JSON response from tracker.[/bold red]")
                    meta['tracker_status'][self.tracker]['status_message'] = "Invalid JSON response."
                except (KeyError, IndexError):
                    console.print("[bold red]Upload failed: Unexpected JSON format in response.[/bold red]")
                    meta['tracker_status'][self.tracker]['status_message'] = "Unexpected response format."
                except Exception as e:
                    console.print(f"[bold red]An unexpected error occurred during upload: {e}[/bold red]")
                    meta['tracker_status'][self.tracker]['status_message'] = f"Unexpected error: {e}"
            else:
                console.print("[cyan]Request Data:")
                console.print(data)
                meta['tracker_status'][self.tracker]['status_message'] = "Debug mode enabled, not uploading."

    async def search_existing(self, meta, disctype):
        dupes = []
        params = {
            'api_token': self.config['TRACKERS'][self.tracker]['api_key'].strip(),
            'tmdbId': meta['tmdb'],
            'categories[]': await self.get_cat_id(meta['category']),
            'types[]': await self.get_type_id(meta['type']),
            'resolutions[]': await self.get_res_id(meta['resolution'], disctype),
            'name': ""
        }

        name_parts = []
        if meta['category'] == 'TV':
            name_parts.append(meta.get('season', ''))
        if meta.get('edition', ""):
            name_parts.append(meta['edition'])
        params['name'] = " ".join(name_parts)

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url=self.search_url, params=params)
                response.raise_for_status()

                data = response.json()
                for each in data['data']:
                    result = each['attributes']['name']
                    dupes.append(result)
        except httpx.TimeoutException:
            console.print("[bold red]Search request timed out after 5 seconds.[/bold red]")
        except httpx.RequestError as e:
            console.print(f"[bold red]Unable to search for existing torrents: {e}[/bold red]")
        except json.JSONDecodeError:
            console.print("[bold red]Search failed: Invalid JSON response from tracker.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred during search: {e}[/bold red]")

        return dupes
