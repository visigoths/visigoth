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

from sqlite3 import connect
import struct

from visigoth.utils.mapping import Projections

class GeopackageReader(object):

    WKB_POINT=1
    WKB_POINTZ=1001
    WKB_POINTM=2001
    WKB_POINTZM=3001

    WKB_LINESTRING=2
    WKB_LINESTRINGZ=1002
    WKB_LINESTRINGM=2002
    WKB_LINESTRINGZM=3002

    WKB_POLYGON=3
    WKB_POLYGONZ=1003
    WKB_POLYGONM=2003
    WKB_POLYGONZM=3003

    WKB_MULTIPOINT=4
    WKB_MULTIPOINTZ=1004
    WKB_MULTIPOINTM=2004
    WKB_MULTIPOINTZM=3004

    WKB_MULTILINESTRING=5
    WKB_MULTILINESTRINGZ=1005
    WKB_MULTILINESTRINGM=2005
    WKB_MULTILINESTRINGZM=3005

    WKB_MULTIPOLYGON=6
    WKB_MULTIPOLYGONZ=1006
    WKB_MULTIPOLYGONM=2006
    WKB_MULTIPOLYGONZM=3006

    # https://github.com/opengeospatial/ets-gpkg12/tree/master/src/test/resources/gpkg
    def __init__(self):

        self.extractors = {

            GeopackageReader.WKB_POINT: ("Point",self.extractPoint,2),
            GeopackageReader.WKB_POINTZ: ("PointZ",self.extractPoint,3),
            GeopackageReader.WKB_POINTM: ("PointM",self.extractPoint,3),
            GeopackageReader.WKB_POINTZM: ("PointZM",self.extractPoint,4),

            GeopackageReader.WKB_MULTIPOINT: ("MultiPoint",self.extractMultiPoint,2),
            GeopackageReader.WKB_MULTIPOINTZ: ("MultiPointZ",self.extractMultiPoint,3),
            GeopackageReader.WKB_MULTIPOINTM: ("MultiPointM",self.extractMultiPoint,3),
            GeopackageReader.WKB_MULTIPOINTZM: ("MultiPointZM",self.extractMultiPoint,4),

            GeopackageReader.WKB_LINESTRING: ("LineString",self.extractLineString,2),
            GeopackageReader.WKB_LINESTRINGZ: ("LineStringZ",self.extractLineString,3),
            GeopackageReader.WKB_LINESTRINGM: ("LineStringM",self.extractLineString,3),
            GeopackageReader.WKB_LINESTRINGZM: ("LineStringZM",self.extractLineString,4),

            GeopackageReader.WKB_MULTILINESTRING: ("MultiLineString",self.extractMultiLineString,2),
            GeopackageReader.WKB_MULTILINESTRINGZ: ("MultiLineStringZ",self.extractMultiLineString,3),
            GeopackageReader.WKB_MULTILINESTRINGM: ("MultiLineStringM",self.extractMultiLineString,3),
            GeopackageReader.WKB_MULTILINESTRINGZM: ("MultiLineStringZM",self.extractMultiLineString,4),

            GeopackageReader.WKB_POLYGON: ("Polygon",self.extractPolygon,2),
            GeopackageReader.WKB_POLYGONZ: ("PolygonZ",self.extractPolygon,3),
            GeopackageReader.WKB_POLYGONM: ("PolygonM",self.extractPolygon,3),
            GeopackageReader.WKB_POLYGONZM: ("PolygonZM",self.extractPolygon,4),

            GeopackageReader.WKB_MULTIPOLYGON: ("Polygon",self.extractMultiPolygon,2),
            GeopackageReader.WKB_MULTIPOLYGONZ: ("PolygonZ",self.extractMultiPolygon,3),
            GeopackageReader.WKB_MULTIPOLYGONM: ("PolygonM",self.extractMultiPolygon,3),
            GeopackageReader.WKB_MULTIPOLYGONZM: ("PolygonZM",self.extractMultiPolygon,4),
        }

    def getDouble8(self,data,littleEndian):
        fmt = "<d"
        if not littleEndian:
            fmt = ">d"
        return struct.unpack(fmt,data)[0]

    def getUINT4(self,data,littleEndian):
        fmt = "<I"
        if not littleEndian:
            fmt = ">I"
        return struct.unpack(fmt,data)[0]

    def extractEnvelope(self,envelope,blob,offset,littleEndian):
        pos = offset
        bbox = None
        if envelope:
            dims = 2
            if envelope == 2 or envelope == 3:
                dims = 3
            if envelope == 4:
                dims = 4
            mins = []
            maxes = []
            for dim in range(0,dims):
                minval = self.getDouble8(blob[pos:pos+8],littleEndian)
                mins.append(minval)
                pos += 8
                maxval = self.getDouble8(blob[pos:pos+8],littleEndian)
                maxes.append(maxval)
                pos += 8
            bbox = (tuple(mins),tuple(maxes))
        return (pos,bbox)

    def extractPoint(self,blob,littleEndian,dimCount):
        dims = []
        consumed = 0
        for dim in range(0,dimCount):
            dims.append(self.getDouble8(blob[consumed:consumed+8],littleEndian))
            consumed += 8
        dims[0:2] = self.projection.toLonLat(dims[0:2])
        return (tuple(dims),consumed)

    def extractLineString(self,blob,littleEndian,dimCount):
        points = []
        numPoints = self.getUINT4(blob[0:4],littleEndian)
        pos = 4
        for index in range(0,numPoints):
            (point,consumed) = self.extractPoint(blob[pos:],littleEndian,dimCount)
            points.append(point)
            pos += consumed
        return (points,pos)

    def extractMultiPoint(self,blob,littleEndian,dimCount):
        points = []
        numPoints = self.getUINT4(blob[0:4],littleEndian)
        pos = 4
        for index in range(0,numPoints):
            (_,linePoints,consumed) = self.extractGeometryObject(blob[pos:])
            lines.append(linePoints)
            pos += consumed
        return (lines,pos)

    def extractMultiLineString(self,blob,littleEndian,dimCount):
        lines = []
        numLines = self.getUINT4(blob[0:4],littleEndian)
        pos = 4
        for index in range(0,numLines):
            (_,linePoints,consumed) = self.extractGeometryObject(blob[pos:])
            lines.append(linePoints)
            pos += consumed
        return (lines,pos)

    def extractPolygon(self,blob,littleEndian,dimCount):
        rings = []
        numRings = self.getUINT4(blob[0:4],littleEndian)
        pos = 4
        for index in range(0,numRings):
            (linePoints,consumed) = self.extractLineString(blob[pos:],littleEndian,dimCount)
            rings.append(linePoints)
            pos += consumed
        return (rings,pos)

    def extractMultiPolygon(self,blob,littleEndian,dimCount):
        polys = []
        numPolys = self.getUINT4(blob[0:4],littleEndian)
        pos = 4
        for index in range(0,numPolys):
            (_,rings,consumed) = self.extractGeometryObject(blob[pos:])
            polys.append(rings)
            pos += consumed
        return (polys,pos)

    def extractGeometryObject(self,blob):
        gformLittle = blob[0]
        gtype = self.getUINT4(blob[1:5],gformLittle)
        if gtype in self.extractors:
            (name,extractor,dims) = self.extractors[gtype]
            (obj,consumed) = extractor(blob[5:],gformLittle>0,dims)
            return (name,obj,consumed+5)
        else:
            print("No extractor found for type=%d"%(gtype))

    def extractGeometry(self,blob):
        # http://www.geopackage.org/spec/
        m0 = blob[0]
        m1 = blob[1]
        version = blob[2]
        flags = blob[3]
        binaryType = (flags >> 5) & 1
        emptyGeometry = (flags >> 4) & 1
        envelope = (flags >> 1) & 7
        littleEndian = flags & 1
        (contentStart,bbox) = self.extractEnvelope(envelope,blob,8,littleEndian)
        return self.extractGeometryObject(blob[contentStart:])

    def getGeometriesFromTable(self,table,column,projection):
        geometries = []
        curs = self.conn.cursor()
        geodata = curs.execute("select * from %s"%(table))
        colnames = [desc[0] for desc in curs.description]
        geom_column_index = colnames.index(column)
        for geodata_row in geodata:
            props = {}
            if projection in Projections.knownProjections:
                self.projection=Projections.knownProjections[projection]
                (name,obj,consumed) = self.extractGeometry(geodata_row[geom_column_index])
                for idx in range(len(colnames)):
                    if idx != geom_column_index:
                        props[colnames[idx]] = geodata_row[idx]
                geometries.append((name,obj,props))
            else:
                print("Unable to import gemoetry with projection %s"%(projection))
        return geometries

    def getGeometries(self):
        geometries = []
        curs = self.conn.cursor()
        metadata = curs.execute("select table_name,column_name,srs_id from gpkg_geometry_columns").fetchall()
        for metadata_row in metadata:

            table = metadata_row[0]
            column = metadata_row[1]
            projection = str(metadata_row[2])
            geometries += self.getGeometriesFromTable(table,column,projection)

        return geometries

    def extract(self,path):
        self.path = path
        self.conn = connect(self.path)
        geometries = self.getGeometries()
        points = []
        lines = []
        polygons = []
        for (name,obj,props) in geometries:
            if name.startswith("Point"):
                points.append((props,[obj]))
            elif name.startswith("MultiPoint"):
                points.append((props,obj))
            elif name.startswith("Line"):
                lines.append((props,[obj]))
            elif name.startswith("MultiLine"):
                lines.append((props,obj))
            elif name.startswith("Polygon"):
                polygons.append((props,obj))
            elif name.startswith("MultiPolygon"):
                polygons.append((props,obj))
        return (points,lines,polygons)

