import json

# 你的原始数据
old_data = [
  {"id":"bk070","name":"grafana","url":"http://10.124.49.36:3000/?orgId=1","category":"lab"},
  {"id":"bk068","name":"grafana cloud","url":"https://fangqingwei123.grafana.net/a/cloud-home-app/onboarding-flow/start","category":"lab"},
  {"id":"bk067","name":"qingfang DL-cml 20.9 sdwan","url":"https://10.124.49.28/#/banner","category":"lab"},
  {"id":"bk066","name":"qingfang eve New","url":"http://10.124.49.24/#!/login","category":"lab"},
  {"id":"bk065","name":"Anyconnect lab 2","url":"https://networklessons.com/cisco/asa-firewall/cisco-asa-anyconnect-remote-access-vpn","category":"lab"},
  {"id":"bk064","name":"ccie anyconnect lab","url":"https://www.packetswitch.co.uk/cisco-asa-anyconnect-vpn/","category":"lab"},
  {"id":"bk063","name":"qingfang cml sdwan","url":"https://172.18.121.104:12768/","category":"lab"},
  {"id":"bk062","name":"qingfang RTP sdwan 20.9 多租户","url":"https://172.18.121.103:12297/","category":"lab"},
  {"id":"bk061","name":"qingfang 东京sdwan 20.6","url":"https://10.70.79.140/#/app/dashboard","category":"lab"},
  {"id":"bk060","name":"qingfang大连sdwan20.14","url":"https://10.124.41.101/","category":"lab"},
  {"id":"bk059","name":"qingfang cml","url":"https://172.18.121.104:11983/login","category":"lab"},
  {"id":"bk058","name":"六哥cml","url":"https://junnyang-lab.cisco.com/login","category":"lab"},
  {"id":"bk057","name":"qingfang eve","url":"http://10.124.49.59/","category":"lab"},
  {"id":"bk049","name":"netflow","url":"http://qingfang:8060/apiclient/ember/index.jsp#/Settings/Discovery/ExportFlow","category":"工具"},
  {"id":"bk028","name":"ASR1K license tool","url":"https://software.cisco.com/software/swift/sltui/viewIntPubKeyGen.action?keytype=PUBLICINTERNAL&subGroup=ASR1KFEAT","category":"工具"},
  {"id":"bk027","name":"license local","url":"https://software.cisco.com/software/swift/lrp/#/devices","category":"license"},
  {"id":"bk023","name":"Pisces 看代码","url":"https://wwwin-pisces.cisco.com/search/keyword?defaultFilterLoaded=&lang=all","category":"CASE"},
  {"id":"bk022","name":"sdwan token master","url":"https://token-master.cisco.com/","category":"CASE"},
  {"id":"bk021","name":"开bug cdet","url":"https://cdetsng.cisco.com/webui/#main","category":"CASE"},
  {"id":"bk020","name":"RTP 地址转换","url":"http://172.18.121.107/","category":"lab"},
  {"id":"bk019","name":"查看on shift engineer and duty manager","url":"https://schedule.cisco.com/","category":"CASE"},
  {"id":"bk017","name":"RDMT","url":"https://gtcroutingops.cloudapps.cisco.com/RDMT/","category":"CASE"},
  {"id":"bk016","name":"CCWR","url":"https://ccrc.cisco.com/ccwr/","category":"CASE"},
  {"id":"bk015","name":"RMA","url":"https://ibpm.cisco.com/rma/home/","category":"CASE"},
  {"id":"bk014","name":"cisco pnp device","url":"https://software.cisco.com/software/pnp/devices","category":"license"},
  {"id":"bk013","name":"cisco gpt","url":"https://onesearch.cisco.com/ciscoit/chatgpt/home","category":"工具"},
  {"id":"bk012","name":"cisco box","url":"https://cisco.app.box.com/folder/0","category":"工具"},
  {"id":"bk011","name":"IOS-XE EFA check","url":"https://www-plmprd.cisco.com/Agile/","category":"lab"},
  {"id":"bk010","name":"IOS-XE CCO update 更新时间","url":"https://wiki.cisco.com/display/RELENG/Polaris+XE17.6.6+Release","category":"lab"},
  {"id":"bk009","name":"IOS-XE smart decoder","url":"https://smartdecoder.cisco.com/","category":"工具"},
  {"id":"bk008","name":"working 权限申请","url":"https://edsart.cloudapps.cisco.com/myAccess","category":"工具"},
  {"id":"bk007","name":"模块兼容性","url":"https://tmgmatrix.cisco.com/?dr=1","category":"工具"},
  {"id":"bk006","name":"cve漏洞查询","url":"https://tools.cisco.com/security/center/cvr","category":"工具"},
  {"id":"bk005","name":"SNMP OID","url":"https://snmp.cloudapps.cisco.com/Support/SNMP/do/BrowseOID.do?local=en","category":"工具"},
  {"id":"bk004","name":"画图","url":"https://asciiflow.com/#/","category":"lab"},
  {"id":"bk003","name":"PNP account","url":"https://software.cisco.com/software/csws/ws/platform/home#pnp-devices","category":"license"},
  {"id":"bk002","name":"CSSM smart license account","url":"https://software.cisco.com/software/csws/ws/platform/home?locale=en_US","category":"license"},
  {"id":"bk001","name":"IOS-XE software download","url":"https://software.cisco.com/download/home","category":"lab"},
  {"id":"mp3g34hn6pdmlukwk","name":"xr techzone","url":"https://scripts.cisco.com/app/RP_Techzone/","category":"知识库"},
  {"id":"mp3gt8svjil9hsp5u","name":"Github","url":"https://github.com/dnGrep/dnGrep/releases/tag/v4.2.121.0","category":"工具"},
  {"id":"mp3gtt4p9bccjextd","name":"Directory","url":"https://directory.cisco.com/find-people/search","category":"cisco 官方"},
  {"id":"mp3gu3y437hs1kaxn","name":"cisco 开case","url":"https://mycase.cloudapps.cisco.com/case","category":"cisco 官方"},
  {"id":"mp3gwxo2pp572vznx","name":"Team shift","url":"https://shifts.cisco.com/APT-GC-RP1/schedule?date=2026-05-13&all_sources=true&weeks=1","category":"cisco 官方"},
  {"id":"mp3gyw7le5epsdelm","name":"排班表","url":"https://scripts.cisco.com/app/gcrpshift/#/","category":"日常"},
  {"id":"mp3gzcdptmzuvmrol","name":"dlsp 加班申请","url":"http://dlsp.5work.com/om/login.aspx","category":"日常"},
  {"id":"mp3h19orgxt2kxfwn","name":"我的视频库","url":"http://10.124.49.67:8096/web/#/home","category":"知识库"},
  {"id":"mp3h3nbpkd4hemg5h","name":"techzone","url":"https://techzone.cisco.com/","category":"知识库"},
  {"id":"mp3hbwzu1zd33lv6b","name":"overwatch 订阅","url":"https://scripts.cisco.com/app/overwatch_c4c/","category":"CASE"},
  {"id":"mp3hcsyrb2wt2bkpm","name":"xingxu 博客","url":"https://imxing.info/","category":"知识库"},
  {"id":"mp3hdgg4c7xh6bbp1","name":"软件版本进度查询","url":"https://wwwin-irt.cisco.com/trainstation/jmp?&-p=polaris","category":"cisco 官方"},
  {"id":"mp3hejzg58lq0spkk","name":"deventsandbox","url":"https://devnetsandbox.cisco.com/DevNet","category":"lab"},
  {"id":"mp3hg13p3kuaf9i6x","name":"video  cast","url":"https://app.vidcast.io/","category":"知识库"},
  {"id":"mp3hx98veaq4wej4u","name":"Devnet NSO lab","url":"https://developer.cisco.com/learning/tracks/get_started_with_nso/nso-labs/learn-nso-with-netsim/setting-up-nso/","category":"知识库"},
  {"id":"mp3hy02c50wq20d6v","name":"GISO","url":"https://pims-web.cisco.com/pims-home/fcgi-bin/CCTReport/CCTOtherReports.cgi?menu=golden_iso_menu","category":"工具"},
  {"id":"mp3hyffji22hdecg2","name":"cisco live","url":"https://www.ciscolive.com/on-demand/on-demand-library.html#/","category":"知识库"},
  {"id":"mp3hzimze57gbdlux","name":"路由产品性能对比","url":"https://ccapp.cisco.com/routing-scale","category":"cisco 官方"},
  {"id":"mp3i34euhql5rjtzf","name":"sdwan 升级步骤查看","url":"https://www.cisco.com/c/dam/en/us/td/docs/Website/enterprise/catalyst-sdwan-upgrade-matrix/index.html","category":"cisco 官方"},
  {"id":"mp3i43cpp4o229mjg","name":"兼容性sdwan compatibility","url":"https://www.cisco.com/c/dam/en/us/td/docs/Website/enterprise/catalyst_sdwan_compatibility_matrix/index.html","category":"cisco 官方"},
  {"id":"mp3i631li0vh52071","name":"packet dump decode","url":"https://hpd.gasmi.net/","category":"工具"},
  {"id":"mp3i6q6rz4zxukp6q","name":"时差查看网站","url":"https://www.timebie.com/cn/beijingnewyork.php","category":"工具"},
  {"id":"mp3j5ubt8jd1xn62k","name":"cisco 官方holiday","url":"https://www.cisco.com/c/r/team-development/benefits/china/en/holidays-shutdown.html","category":"cisco 官方"},
  {"id":"mp3j8d0wex17gr3hr","name":"snmp mib owner","url":"https://wiki.cisco.com/display/MANAGE/IOS%20MIB%20Owners","category":"cisco 官方"},
  {"id":"mp3j949vox81stmi1","name":"wwwin","url":"https://wwwin.cisco.com/c/cec/bridge.html/home","category":"cisco 官方"},
  {"id":"mp3j9ren9fkjrhbh1","name":"epc packet decode","url":"https://cway.cisco.com/capture-gen-analyzer/","category":"工具"},
  {"id":"mp3jr90ry131v6f9h","name":"Tac SR collection","url":"https://community.cisco.com/t5/tkb-tac-tips-%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/%E3%82%88%E3%81%8F%E3%81%82%E3%82%8B%E8%B3%AA%E5%95%8F%E3%81%A8%E8%A7%A3%E6%B1%BA%E6%96%B9%E6%B3%95-tac-sr-collection/ta-p/3215391","category":"cisco 官方"},
  {"id":"mp3js3p2dk701l2y1","name":"AutoPod","url":"https://cx-labs.cisco.com/pods","category":"工具"},
  {"id":"mp3jt46g88sz36wba","name":"XE root shell","url":"https://sso-dbbfec7f.sso.duosecurity.com/oidc/DITJRYR8FIQ64ARR2V46/authorize?client_id=DITJRYR8FIQ64ARR2V46&response_type=code&scope=openid+offline_access+pr","category":"工具"},
  {"id":"mp3jti4chfh9kx5ru","name":"CALO","url":"https://calo-new.cisco.com/#/tools/lab_cases","category":"cisco 官方"},
  {"id":"mp3ju8bxe4zcyk61d","name":"qingfang ISE","url":"https://10.124.49.58/","category":"lab"},
  {"id":"mp3jvuvzqyxqwxict","name":"Topic","url":"https://topic.cisco.com/home","category":"cisco 官方"},
  {"id":"mp3jxrj7p9g8i0od7","name":"ECDP 查看销售 htom","url":"https://ecdp.cisco.com/httsmd#/","category":"cisco 官方"},
  {"id":"mp3jzi359m1bh0vjv","name":"Pisces 看代码","url":"https://wwwin-pisces.cisco.com/search/keyword?defaultFilterLoaded=&lang=all","category":"cisco 官方"},
  {"id":"mp3k03jt3k38iu9ro","name":"开bug cdet","url":"https://cdetsng.cisco.com/webui/#main","category":"cisco 官方"}
]

# Extract unique categories
cat_names = sorted(set(item["category"] for item in old_data))
categories = [{"id": i+1, "name": name} for i, name in enumerate(cat_names)]

# Build name->id map
cat_map = {c["name"]: c["id"] for c in categories}

# Convert bookmarks
bookmarks = []
for item in old_data:
    bookmarks.append({
        "id": len(bookmarks) + 1,
        "title": item["name"],
        "url": item["url"],
        "category_id": cat_map.get(item["category"]),
        "created_at": item.get("createdAt", "")
    })

# Output
output = {
    "categories": categories,
    "bookmarks": bookmarks
}

with open("bookmarks_import.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"转换完成！共 {len(categories)} 个分类，{len(bookmarks)} 条书签")
print("文件已保存为: bookmarks_import.json")
