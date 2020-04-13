#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 建议用exifread。
# PIL读取的部分属性名称为纯数字，没有映射名称，不易阅读。
# 但偶尔有几个特殊属性只有PIL能读到。

import os
import shutil
import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def _convert_to_degress(value):  # PIL读取到的GPS坐标换算
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def readExif(file, method='exifread'):
    # exifread方法
    if method == 'exifread':
        with open(file, 'rb') as f:
            tags = exifread.process_file(f)
        # print(file)
        for key in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            if key in tags:
                tags.pop(key)
        tagsList = sorted(tags.items(), key=lambda x: x[0].upper())
        # tagsList = tags.items()
        for tag in tagsList:
            if tag[0] in [
                    # 'EXIF ApertureValue',
                    # 'EXIF BrightnessValue',
                    # 'EXIF ColorSpace',
                    # 'EXIF ComponentsConfiguration',
                    # 'EXIF DateTimeDigitized',
                    # 'EXIF DateTimeOriginal',
                    # 'EXIF ExifImageLength',
                    # 'EXIF ExifImageWidth',
                    # 'EXIF ExifVersion',
                    # 'EXIF ExposureBiasValue',
                    # 'EXIF ExposureMode',
                    # 'EXIF ExposureProgram',
                    # 'EXIF ExposureTime',
                    # 'EXIF FNumber',
                    # 'EXIF Flash',
                    # 'EXIF FlashPixVersion',
                    # 'EXIF FocalLength',
                    # 'EXIF FocalLengthIn35mmFilm',
                    # 'EXIF ISOSpeedRatings',
                    # 'EXIF LensMake',
                    # 'EXIF LensModel',
                    # 'EXIF LensSpecification',
                    # 'EXIF MeteringMode',
                    # 'EXIF SceneCaptureType',
                    # 'EXIF SceneType',
                    # 'EXIF SensingMethod',
                    # 'EXIF ShutterSpeedValue',
                    # 'EXIF SubSecTimeDigitized',
                    # 'EXIF SubSecTimeOriginal',
                    'EXIF SubjectArea',
                    # 'EXIF WhiteBalance',
                    'GPS GPSAltitude',
                    'GPS GPSAltitudeRef',
                    'GPS GPSDate:',
                    'GPS GPSDestBearing',
                    'GPS GPSDestBearingRef',
                    'GPS GPSImgDirection',
                    'GPS GPSImgDirectionRef',
                    'GPS GPSLatitude',
                    'GPS GPSLatitudeRef',
                    'GPS GPSLongitude',
                    'GPS GPSLongitudeRef',
                    'GPS GPSSpeed',
                    'GPS GPSSpeedRef',
                    'GPS GPSTimeStamp',
                    # 'Image DateTime',
                    # 'Image ExifOffset',
                    # 'Image GPSInfo',
                    # 'Image Make',
                    # 'Image Model',
                    'Image Orientation: Rotated',
                    # 'Image ResolutionUnit',
                    # 'Image Software',
                    # 'Image XResolution',
                    # 'Image YCbCrPositioning',
                    # 'Image YResolution',
                    # 'Thumbnail Compression',
                    # 'Thumbnail JPEGInterchangeFormat',
                    # 'Thumbnail JPEGInterchangeFormatLength',
                    # 'Thumbnail ResolutionUnit',
                    # 'Thumbnail XResolution',
                    # 'Thumbnail YResolution'
            ]:
                pass
            # print('%s: %s' % tag)
        return tags

    # PIL方法 只适用于PIL能打开的文件 无法读取raw
    if method == 'PIL':
        exifinfo = {}
        img = Image.open(file)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    print('%s: %s' % (decoded, value))
                    if decoded == "GPSInfo":
                        gps_data = {}
                        for t in value:
                            sub_decoded = GPSTAGS.get(t, t)
                            if sub_decoded in ['GPSLatitude', 'GPSLongitude']:
                                gps_data[sub_decoded] = _convert_to_degress(value[t])
                            elif sub_decoded == 'GPSAltitude':
                                gps_data[sub_decoded] = value[t][0] / value[t][1]
                            else:
                                gps_data[sub_decoded] = value[t]
                        [print(': '.join(list(map(str, i)))) for i in gps_data.items()]
        return exifinfo


if __name__ == "__main__":

    root = r'D:\Downloads\photo backup'
    for path, dirs, files in os.walk(root):  # read all files
        for fn in files:
            file = os.path.join(path, fn)  # full path

            print('\n===== exifread =====')
            exif = readExif(file, method='exifread')
            [print(f'{k}: {v}') for k,v in exif.items()]

            print('\n===== PIL =====')
            exif = readExif(file, method='PIL')
            [print(f'{k}: {v}') for k,v in exif.items()]
        # break  # root only
