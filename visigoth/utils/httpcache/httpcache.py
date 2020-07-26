# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without 
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or 
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
