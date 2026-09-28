import json, re, os
winners=json.load(open('winners.json'))
GH='lldaydayhappy'; REPO='venera-sources'; BR='main'
RAW=f'https://raw.githubusercontent.com/{GH}/{REPO}/{BR}'

out=[]
for k,w in winners.items():
    p=f"sources/{w['fileName']}"
    s=open(p,encoding='utf-8').read()
    g=lambda pat:(re.search(pat,s).group(1) if re.search(pat,s) else None)
    real_ver=g(r'version\s*=\s*["\']([^"\']+)') or w['version']
    out.append({
        "name": w['name'],
        "fileName": w['fileName'],
        "key": w['key'],
        "version": real_ver,
        "minAppVersion": g(r'minAppVersion\s*=\s*["\']([^"\']+)') or "1.0.0",
        "url": f"{RAW}/{w['fileName']}",
        # 额外字段，方便使用者核对（Venera 会忽略未知字段）
        "officialVersion": w['official_ver'],
        "upstream": w['repo'].split('/')[0],
    })
out.sort(key=lambda x: x['name'].lower())
json.dump(out, open('index.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"index.json 生成完毕，共 {len(out)} 个源\n")
print(f"{'源':<20} {'官方':<10} {'本仓库':<10} {'minApp':<8} 上游")
print('-'*80)
for x in out:
    print(f"{x['name']:<20} v{x['officialVersion']:<9} v{x['version']:<9} {x['minAppVersion']:<8} {x['upstream']}")
