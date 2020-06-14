# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from urllib import request
import urllib.parse
import os
import json
import sys
import tempfile
import os.path

import hashlib
import ssl

ctx = ssl.create_default_context()
ctx.set_ciphers("DEFAULT:@SECLEVEL=1")

from visigoth.utils.term.progress import Progress

class HttpCache(object):

    cache_dir = os.path.join(tempfile.gettempdir(),"visigothis_cache")

    @staticmethod
    def configureCacheDirectory(cache_dir):
        HttpCache.cache_dir = cache_dir

    @staticmethod
    def meteredFetch(label,url,path,data=None):
        p = Progress("Downloading")
        def hook(a,b,c):
            progress_frac = a*b / c
            p.report("",progress_frac)
        try:
            urllib.request.urlretrieve(url,path,hook,data)
            sys.stdout.write("\n")
        except Exception as ex:
            if str(ex).find("signature type") > 0:
                p.report("", 0.0)
                with urllib.request.urlopen(url, None, context=ctx) as u:
                    response = u.read()
                    with open(path, "wb") as fout:
                        fout.write(response)
                p.report("", 1.0)
                sys.stdout.write("\n")
            else:
                raise ex


    @staticmethod
    def fetch(url,data=None,mimeType='application/json',suffix="",returnPath=False):
        cachepath = url.replace("/","_")
        cachepath = cachepath.replace(":","_")
        cachepath = cachepath.replace("?","_")
        cachepath = cachepath.replace("&","_")
        cachepath = cachepath.replace("=","_")

        if data:
            if mimeType == 'application/json':
                enc_data = json.dumps(data).encode("ascii")
            else:
                enc_data = data.encode("utf-8")
            hash_object = hashlib.md5(enc_data)
            cachepath += "."+hash_object.hexdigest()

        if not os.path.exists(HttpCache.cache_dir):
            os.mkdir(HttpCache.cache_dir)

        cachekey_digest = hashlib.md5(bytes(cachepath,"utf-8")).hexdigest()
        cachepath = os.path.join(HttpCache.cache_dir,cachekey_digest)

        if suffix:
            cachepath += suffix

        if not os.path.exists(cachepath):
            if not data:
                HttpCache.meteredFetch("Downloading...",url,cachepath)
            else:
                # req = urllib.request.Request(url,context=ctx)
                # req.add_header('Content-Type', mimeType)

                with urllib.request.urlopen(url,enc_data,context=ctx) as u:
                    response=u.read()
                    with open(cachepath,"wb") as fout:
                        fout.write(response)
        if returnPath:
            return cachepath
        else:
            with open(cachepath,"rb") as f:
                return f.read()
