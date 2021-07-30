"""
    *************************** 
    --------description-------- 
 	 Description: 
 	 Version: 1.0
 	 Autor: Tu Ruwei
 	 Date: 2021-07-13 11:31:32
 	 LastEditors: Tu Ruwei
 	 LastEditTime: 2021-07-13 11:31:33

    ***************************  
"""

import hashlib
import os


class upload_in_chunks(object):
    def __init__(self):
        self.__observers = None
        self.filename = None
        self.chunksize = 0
        self.totalsize = 0
        self.readsofar = 0

    def set_file(self,filename, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)

    def register(self, observer):
        self.__observers = observer

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    self.__observers.update_message('上传完成')
                    break
                self.readsofar += len(data)
                percent = self.readsofar * 1e2 / self.totalsize
                self.__observers.update_message('MD5值计算中,进度：{:.2f}%'.format(percent))
                yield data

    def __len__(self):
        return self.totalsize

class MD5(object):
    def __init__(self) -> None:
        self.__observers = None
    
    def MD5_Strs(self, strs: str):
        md = hashlib.md5()  # 创建md5对象
        md.update(strs.encode(encoding='utf-8'))
        return md.hexdigest()

    def register(self,observer):
        self.__observers = observer

    def GetFileMd5(self, filename : str):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename,'rb')
        size = os.path.getsize(filename)/8096
        count = 0
        while True:
            b = f.read(8096)
            if not b :
                break
            myhash.update(b)
            count+=1
            self.__observers.update_message('MD5值计算中,进度：{:.2f}%'.format(count/size*100))
        f.close()
        return myhash.hexdigest()

    def GetFileMd5AandCopy(self,inputname,outputname):
        if not os.path.isfile(inputname):
            return
        inhash = hashlib.md5()
        outhash = hashlib.md5()
        size = os.path.getsize(inputname)/8096
        input = open(inputname,'rb')
        out = open(outputname,'wb')
        count = 0
        while True:
            block = input.read(8096)
            if not block :
                break
            out.write(block)
            inhash.update(block)
            outhash.update(block)
            count+=1
            self.__observers.update_message('文件拷贝中,进度：{:.2f}%'.format(count/size*100))
        input.close()
        out.close()
        return inhash.hexdigest(), outhash.hexdigest()
