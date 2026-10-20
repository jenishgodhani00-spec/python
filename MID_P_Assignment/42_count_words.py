txt = 'hello world hello'
print({w: txt.split().count(w) for w in set(txt.split())})