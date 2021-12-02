from typing import Pattern
import requests
import re
import os
import time

class LoveCrawlerCtrl:
  def __init__(self, main):
    self.MainSelf = main
    self.matchSuffix = main.matchSuffix
    self.customRegexp = main.customRegexp
    self.isSaveToFile = main.isSaveFile
    self.isAllUrlChecked = main.isAllUrlChecked
    print(self.isSaveToFile)

  def getWebContent(self, url):
    matchResults = []
    resp = requests.get(url)
    if self.isAllUrlChecked:
      matchResults += self.matchWebUrls(resp.text)
    else:
      if self.matchSuffix:
        # 快速匹配
        matchResults += self.matchWebUrls(resp.text, self.matchSuffix)
      # 自定义匹配
      if self.customRegexp:
        matchResults += self.matchWebText(self.customRegexp, resp.text)
    
    # print(matchResults)
    
    # 保存到文件
    if self.isSaveToFile and matchResults:
      self.saveToFile(matchResults)

    # print(result)
  
  def saveToFile(self, urls):
    save_path = self.formatPath(self.MainSelf.savePath)
    print(f"保存路径：{save_path}")
    for (url, name) in urls:
      print(f'{url},{name}')
      try:
        resp = requests.get(url, timeout=60)
        resp_content_type = resp.headers.get("content-type")
        if re.match(r'(image)+',resp_content_type, re.I):
          if name == None:
            matchRes = self.matchWebText(r'\/([^\s\/]+(?:\.[\w\d]+))?[^\/]*?$', url)
            name = matchRes[0] or str((int(time.time())))
            print(matchRes)
            print(resp.headers.get("content-type"))
            print(resp.headers.keys())

          if '.' not in name:
            name = f'{name}.jpg'
            
          with open(f'{name}', 'wb+') as f:
            f.write(resp.content)

      except Exception as err:
        print(err)
        print(f"{url}保存失败")

  # 匹配所有url
  # exact="mp4|mp3|png"
  def matchWebUrls(self, text, exact=None):
    _exclude = '[^\s\"\'\?]'
    exact = "()" if exact == None else f"\/(.*?\.(?:{exact}))"
    # http://abc
    # exact: http://abc/abc.jpg
    pattern1 = r'((?:http[s]?:)?\/\/[^\s\>\<\;\"\:\']+{}(?:\?[^\s]+)?)'.format(exact)
    # href="/abc" src="/abc"
    pattern2 = r'(?:href|src)=[\"\']({}*\/({}*?))(?:\?[^\s]+)?[\"\']'.format(_exclude,_exclude)
    # href="abc" src="abc.jpg"
    pattern3 = r'(?:href|src)=[\"\'](([^\/]*?))[\"\'](?:\?[^\s]+)?'

    results = self.matchWebText(pattern1, text)
    results += self.matchWebText(pattern2, text)
    results += self.matchWebText(pattern3, text)

    return list(set(results))

  def matchWebText(self, pattern, text):
    if pattern:
      patternObj = re.compile(pattern)
      matchResult = patternObj.findall(text)
      return matchResult or []
    return []
  
  def formatPath(self, path):
    return path.replace(r'\/'.replace(os.sep, ''), os.sep)
