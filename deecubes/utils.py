URL_ENCODE_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"


def base64_encode(num):
  if num == 0:
    return URL_ENCODE_CHARS[0]
  else:
    arr = []
    base = len(URL_ENCODE_CHARS)
    while num:
      num, rem = divmod(num, base)
      arr.append(URL_ENCODE_CHARS[rem])
      arr.reverse()
  return ''.join(arr)
