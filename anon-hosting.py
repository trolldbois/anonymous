#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cymrudns
from cymrudns import DNSClient
import urllib,re


def getAnonOpsIp(url):
  ips=[]
  page = ''.join( urllib.urlopen(url).readlines() )
  ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', page)
  return ips

def resolveHosting(ips):
  res=[]
  c = DNSClient()
  res=[ (ip,c.lookup(ip)) for ip in ips]
  return [(ip,c.lookup(data.asn,'ASN')) for ip,data in res]

def main():
  url="http://anonops.eu/irc.html"
  ips=getAnonOpsIp(url)
  res=resolveHosting(ips)
  
  results=[(ip, data.cc,data.owner) for ip,data in res ]
  resSorted=sorted(results, key = lambda results: results[1])
  for ip,cc,owner in resSorted:
    print "%s : %s -> %s"%(ip, cc,owner)

if __name__ == "__main__":
    main()
