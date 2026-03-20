import requests
import ssl
from requests.adapters import HTTPAdapter

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT:@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

url = "https://api.shopling.co.kr/prod/prod_gather_api.phtml?mode=2"

xml_data = """
<reqst>
    <apiProdGather>
        <login_id><![CDATA[ckm00285]]></login_id>
        <company_id><![CDATA[S0009789]]></company_id>
        <api_auth_key><![CDATA[qe2Nbci4CPoCknugVTkV]]></api_auth_key>
        <search_tp><![CDATA[등록일]]></search_tp>
        <start_dt><![CDATA[20260101]]></start_dt>
        <end_dt><![CDATA[20260319]]></end_dt>
        <prod_id><![CDATA[100401]]></prod_id>
        <prod_fields><![CDATA[goods_key]]></prod_fields>
        <opt_yn><![CDATA[Y]]></opt_yn>
        <attri_yn><![CDATA[N]]></attri_yn>
    </apiProdGather>
</reqst>
""".strip()

session = requests.Session()
session.mount("https://", TLSAdapter())

response = session.post(
    url,
    data=xml_data.encode("utf-8"),
    headers={"Content-Type": "application/xml; charset=utf-8"},
    timeout=30
)

print(response.status_code)
print(response.text)