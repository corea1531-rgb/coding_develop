import json
import csv
import time
import requests
import pandas as pd

# =========================================================
# 0. 쿠키 / 헤더
# =========================================================
cookies = {
    'PCID': '17726070646965999973782',
    'x-coupang-target-market': 'KR',
    'x-coupang-accept-language': 'ko-KR',
    'sid': '7fa02b5efeca43f0971d09fd4b85041061534995',
    'OAuth_Token_Request_State': '09106985-8441-4c60-973d-43b2c2cbd945',
    'sc_vid': 'A00193388',
    'sc_lid': 'ckm00285',
    'sc_uid': 'eRXuy7/LuxetxfJ+eZl6NHnSeKo+PF1TRYzZ2Ml/Z0iYBja0YjorhEBBquNHLhc=',
    'wing-market': 'KR',
    'wing-locale': 'ko',
    'sxSessionId': 'NTU2MDA2YTUtZGE3NC00MDEwLWFlZmItZjMzNDQ1MmNkMGJl',
    'XSRF-TOKEN': 'b16f83a4-b2fb-4cd3-8294-8d2a1f7f9cf5',
    'CGSID_PARTNERADMINWEB': 'cda906caaabf4bafbbcbf00d95702230',
    'bm_mi': '5A635F85708CB97B8E54A5AF97C0B9EA~YAAQZnkyF0MWU/mcAQAA5C0FCR8OCPo4VHO8hLT6tv+0tCBEcI6VFBIpInbhRpH3+VHaaokKZXjiCYDj4wlFAL6KWQvTOzgk1FFu5IpHZswf5RddOrg58riaVQ5sv3N+a+1jCM3zWQGQ6bGW/+3MP8RFCCN4FWKsmu0PelbBCw54+jcfi2RMjr+QUh69Zc39P+ylFYtcfmiNTAV4P7MfRYatR15k4wYHniEGhPnbuwQs/MtMhLSXbYCdbfFVxYohFWDoH021rbBv1qzIHDAFQPEMrZMOD2FqJ7mguMymu5N7OJGFiDfUc0OHYm2SwJyKrsA9v5c4i2tKO38HnmPZPfQMNRrfZ68FUWbJMCF8YASLTBc=~1',
    'ak_bmsc': 'E7586FECFC0789AE9699BE7168A116C1~000000000000000000000000000000~YAAQZnkyFxwXU/mcAQAAwzEFCR/Er+mcYVXjBak+OqtZno85/GQtfnSYjuNzs9RqAxQmf+jHlBi0pkza/bgw9tPG20QUxLSSJ7QVIi1Zl9ZsLP/VxgA0tvRh5q4Jl9aTtrAbMB0VDJxrJXBg88cC8UQaGOkphaQVmKAKU80g177yPbFyODpOXVMoq6BW4idOhPISkJrvZ133zn54S3w8v5NW6WxUkTvOLPfCFF9iWTGCRRxx6bgX2GQcaEIj2kVNiwpovhlo4cg88gJxBAQFlscAMMmxOG09HLyGmDluLOsqqyWQ5qBFUN2k/m4794BUDe8YrOgF6auWEyS7Ly3YXtg2eBkMQJ8imOYU6qqwQzlmIiVJPsrEZ/+rzxwMH4tyHQ9cd8tzn2z92ggaUyE/INfD8IxuQay0blrJ3vUxP0KjBdajSoVoil9bxrZEfkfB61YniOqcQLKErEFsMKKaHpPYQhPlBluXhO1wB1s8V7M/5uufyrOXrlmL93wiBTGXMHwNeCww29v83xQ9vf7QlMR7duAphhLe',
    'bm_ss': 'ab8e18ef4e',
    'web-session-id': 'f44e2d46-f265-415b-a41e-b0fd278aa55b',
    '_abck': '065E9F34F28E2B1BC4EC774F65D71776~0~YAAQXbxBF9eYs/GcAQAA1kdiCQ+qbqBcUZMnm145OiRnZStW3s4ap9o+buuZeEzemcolPRVrudnf48S8/LR0QdDdm6+xx1BfTNoxMgpn3N8Y00eWCb+My/s1iPiLzCn5nzO6+YZoZdD8r9fbAGltS4DfSx0aMM9nKF3+FpJS3kVZrkvRQtx7/+A6EHdpHSVF1yNPnSJP/VbMtrRERnN3Sc0VN9RsG1EQCmN/vXUwhPQgTiQFkZwMGtkCWG3fosiu2iIEvx+Xc+LwYBcHN7fmdoUhq8r+gTXAo//PFvbGwINcYyeyQhbNd/o4HXTKZl556nD7M3MvBUhSjU2ehV76wNM326V438DoHxQwHt9PdlRkmtjItkyU09neqrhOeafAe1kzl1acl3LlvVwYKBVE2AdUh6OxHWUhBAQ6XGfP06hDqu+x5FFHwXffSGdSvMQ5hf9s2Drlr9QPWU9h8KffjD2fqRKnnu1OhehygvLtBPwdmpawvLSHPQxnFRhzm06k5XV3mojYEATYvenb6gvV41mKQhgGO2MfgiY1Jp8Db6F7V0df3UsHb/i63OEL+TNr6LTYLluhkVJQnjxjycSvSLoCZmYXZvz60/OYi1OfJU3dz+iinwSmVcjSyPszgIk2pdgpy9BdvS9Z9iWQzwRwFWtjFvDdNEBBH/UTqEN7lzc4GZh+5Lv6mr6FmoSiKbJSIJRdYiuoGXtof+y+zHjRtety0nwTDxx2VzUvxiKf+ypP/VRyEHgAKvoxYmfcpHf1oLb6ize/f2OAIvlZ2BY=~-1~-1~1773982449~AAQAAAAF%2f%2f%2f%2f%2f4deOMVbkxTJuKtKe+37EGk%2fihkthzhpGNiqdgxJZUIZMaiaKXWDbNCaUxepszYW35Kg3hy3G+tuJMUqt26rgGj60Yn9RTG+aOlSw0vGQW9d67Hh9TN0vS6N+nI1GtWoHSboNOi%2fGdrPw%2fLgJkjIpHRQwIOO9epej2dQgvWLhq33GMp8mpX7Ouuqtbile22glGuftqpR0AOc4mryZZyUHIoYfH1BfCuOMrhBiHH57wGcAVU%3d~-1',
    'HOME_CARD_LIFE_NudgingSmsMfa': 'DISMISS',
    'AWSALBTG': 's0oRsuTUPMKhbQBu16g1MSj2J7IJU8yhU+a8NyRF1MGgvKB0e95NE/5+qcSETnkw9xGuGRs5FYScO8oD7HHVGoxJA40DJVlwylIrq0Pr43/eLpzTMYRY2dsvDHLMJtZRU/kRcH2nqJpWo6/8dqmKWOfpDy4nhS10NIRYWJi0cqyef9blZd0=',
    'AWSALBTGCORS': 's0oRsuTUPMKhbQBu16g1MSj2J7IJU8yhU+a8NyRF1MGgvKB0e95NE/5+qcSETnkw9xGuGRs5FYScO8oD7HHVGoxJA40DJVlwylIrq0Pr43/eLpzTMYRY2dsvDHLMJtZRU/kRcH2nqJpWo6/8dqmKWOfpDy4nhS10NIRYWJi0cqyef9blZd0=',
    'bigfoot_browser_session_id': 'b5ca5d2f-2000-4a26-9e95-70e9989d8471',
    'bm_so': '54804B0E0CE407811D131CFBB214F9694C6642F759B5F4DF2548915967E641E8~YAAQbXkyFyfwsOicAQAAt7lsCQdUJpu8dApIDHsoLaQvMsFN1i71ZE4LzP+rCi9hXyBzgm/GMEdKs/ogymw1HZkzg1jCbz1qbQcxbkjlQtX7y92W5b53zSsp4/4hZX/Xown1hpi54cJ+qjN24ai8MK1qXGez8SrhlnGyILuJqzgiqYnWlIWlr3Bm1+KaDC+s52EvMy2GmEbFCwLCGQreTomAkt+EYJfPTJKXPCQDh3vEkWPCQjn7lU9/W4pAZU+nIbC3HPEJq9gVEPuz3X4I5Nu8hIb93i5mAPntp363xiEIdmlTc4vKd5BtxN9cTaVHOGGy7uYsvC58BGyIYgMSK0v3uiIeNO/Qs86wU5KxdlUVbUJyRLGHGPMFs8LcC+mfpyNCCAPmtYgeKtqn8iaDUNcYxhWfSEec2vPvxPbJsbISW7pGDUEg2Gsry50oO0liEaT/3sN9dOYjH+vlp4PlBTk=',
    'bm_lso': '54804B0E0CE407811D131CFBB214F9694C6642F759B5F4DF2548915967E641E8~YAAQbXkyFyfwsOicAQAAt7lsCQdUJpu8dApIDHsoLaQvMsFN1i71ZE4LzP+rCi9hXyBzgm/GMEdKs/ogymw1HZkzg1jCbz1qbQcxbkjlQtX7y92W5b53zSsp4/4hZX/Xown1hpi54cJ+qjN24ai8MK1qXGez8SrhlnGyILuJqzgiqYnWlIWlr3Bm1+KaDC+s52EvMy2GmEbFCwLCGQreTomAkt+EYJfPTJKXPCQDh3vEkWPCQjn7lU9/W4pAZU+nIbC3HPEJq9gVEPuz3X4I5Nu8hIb93i5mAPntp363xiEIdmlTc4vKd5BtxN9cTaVHOGGy7uYsvC58BGyIYgMSK0v3uiIeNO/Qs86wU5KxdlUVbUJyRLGHGPMFs8LcC+mfpyNCCAPmtYgeKtqn8iaDUNcYxhWfSEec2vPvxPbJsbISW7pGDUEg2Gsry50oO0liEaT/3sN9dOYjH+vlp4PlBTk=~1773979614597',
    'bm_s': 'YAAQbXkyF4D6sOicAQAAluNsCQXjm+DGTBcUBwu4Pf5b/pISIFujPOo84FJUvPzpvGvghKICpR7RNjX8gIYC4WVZ91wt3pLzG9kP51fV+zcerJIe7OkC2Z1tCTB4E2szu6pf1CeslX6+4bF0hbC66E/48vVkjeKGttyfpCO0oCpcHvueD/u3khy6XKF33wr8b4qHA77K9Jwntx4O9z/Yl4pgMMGmrDnMUVMmoGzNK2O6WJh9EWfcUT6306iju1SGmZ+X/3XpzTiDA1CN5SJjTfrYiX8kv9+MUYo9HWUyI8Folhg+hjK6YPNVmH+16mu/9npAz2+klHk6zmmaEu+PvCyVoxihYMrZNzfxc1kURUd/9XCuQ3Sx+z5sdhNaTg8Agg99io+nSCoPirv3voCNm6ITex4MzSnyW9E68ursUI2OkXCfKm4Ek4yi5YE9BRcTksXQOXMJZNwDh+CR9CJ02iT2I9R9WaMeZfa627vM94JTLv0Mod/RoQ3s0R8cdYA94HgDv09oZburpfCzI0HZR773+7a6b/O9KW0pmVn0WkKRLQZ+IS4ttuApioNbpQtLXf+FFL7XSSWYn7FtnB9v+7I9yCHoLCvC2Hz81/HvHdYEeVG5wVp635Qe/mvLuBcU2IF6uRpwzCnWB91OEwAI/LxiOej7bUa4BioOr4EjliPpD4JtJ6H0EWyIdvZpEsnEtgGPkRSI2gkZjnlz04geN6CVABNaIizeXC+xFWPVtClHiw3wYpQxR4fqnXUO7crKr9WdJXtGt6acjqbJqNHNCfz2h7AclyfAAFEWNFBnAelWGWg5XK/+Jlcmh1jFpSM0zIKsCSXUss/UxOaccm1a9q8Qb9zj62L37aJWBGcsI60u6Dy9DGhZGLxDQo0WpUMpz/DZ+O03C+Hu7pnYFyZzkl69oBrzGZ1Yn513iiNsjk3VD8OdAmVgNRIQaVh00g==',
    'bm_sz': 'A922AE1E387B5902C23D560E21F07D26~YAAQbXkyF4L6sOicAQAAluNsCR/RQu0YU3gBYZuDiUilzFrM5kFqOmyuh+canacGcAGDDhAbIYpXdXfPIQsafDa350lpya53YfactKXvsqq83jOcXRwT4X1PjthUfDm1MWAgRgFJ1ij2E/8Tocp+F8te1ENsdg0VoUd58/uAQsMHLmSNiKgNdPFF0D/Ijoh7ZIHL+TxBbvz6OEJZYLGvrfe8KqVW2z8mP83K0ZjehnRUAdEJhPDOYIOMsyW6ApN/0NWHu/TUnk0iPWcZ+QF9ai8uGM2d8g/A2i9DvDUFGnj2keBE/YevCv6nu2h3nzlr6wM5DDO0c2/aMEQyqvPeMd7B/EeetL+N/wOFKNAl8tHvnStW7PEDzlRmDQq9nI7PtWsSGMwDVcnr9n8ISmDpuEprJhagrjf88AnjpGkDqiKASP3zVmlW6B7zVfbqjCGwNmQP0J2emaNLkWWAw0c4ls5/4JCPnTOZyhilF2iHF1SlzigpPsBNAGl7D9GDpeESjpZZGco+P97NEOhXo3abB4kk/uop4X9KhcTdqOvgMKHvgG0e69vqbDrL3FI=~4408388~4534835',
    'fs_lua': '1.1773979624815',
    'fs_uid': '#o-24BWCV-na1#3c89c560-df0c-424f-8e16-64bc370e2a48:227267ae-243b-4eaf-8280-2d16c59924e7:1773978568025::6#8afb4a58#/1804743907',
    'JSESSIONID': '2A095A4A0F1F0CF1E9A5910733908F1D',
    'bm_sv': '46AC3BC3EF8C36FFD8E3B2EFCAD36CA8~YAAQbXkyF2QIseicAQAAJCBtCR/NrYL1znlF0uSO/ZibjLmuDtzOFCTsH6GupggIzONbl2IRn3bUs/sbCGl9Bkwy1pI1XNZibXtH8mb/sXktmzJ1ew2ucz3j6+SEK8Mo3NJGroQggQc43mtjA2hsZ1t6gAihsTXOO+Zvwaj+KgoNIm3HWDMCKI2Va0B3x5EiwIsGvQfpPISyRt4rEnnrVjFwiIB1Df3yNuhtOUM9lEuR17OonHxJnTVRU8SvbydK1Vur~1',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=f32d75da7b425b59baaa1b97acb63e642f66ca88,sentry-public_key=5f0c21cbbd20390ab64c6c3fb52d4a5f,sentry-trace_id=a7ad044e33a14de191b68612225c9570',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'origin': 'https://wing.coupang.com',
    'priority': 'u=1, i',
    'referer': 'https://wing.coupang.com/tenants/rfm/settlements/fee-details',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'a7ad044e33a14de191b68612225c9570-af399a6013039f5a',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'withcredentials': 'true',
    'x-rfm-portal2-request-id': 'IlTH2ac-5D1tJqV1K-sje',
    'x-xsrf-token': 'b16f83a4-b2fb-4cd3-8294-8d2a1f7f9cf5',
    # 'cookie': 'PCID=17726070646965999973782; x-coupang-target-market=KR; x-coupang-accept-language=ko-KR; sid=7fa02b5efeca43f0971d09fd4b85041061534995; OAuth_Token_Request_State=09106985-8441-4c60-973d-43b2c2cbd945; sc_vid=A00193388; sc_lid=ckm00285; sc_uid=eRXuy7/LuxetxfJ+eZl6NHnSeKo+PF1TRYzZ2Ml/Z0iYBja0YjorhEBBquNHLhc=; wing-market=KR; wing-locale=ko; sxSessionId=NTU2MDA2YTUtZGE3NC00MDEwLWFlZmItZjMzNDQ1MmNkMGJl; XSRF-TOKEN=b16f83a4-b2fb-4cd3-8294-8d2a1f7f9cf5; CGSID_PARTNERADMINWEB=cda906caaabf4bafbbcbf00d95702230; bm_mi=5A635F85708CB97B8E54A5AF97C0B9EA~YAAQZnkyF0MWU/mcAQAA5C0FCR8OCPo4VHO8hLT6tv+0tCBEcI6VFBIpInbhRpH3+VHaaokKZXjiCYDj4wlFAL6KWQvTOzgk1FFu5IpHZswf5RddOrg58riaVQ5sv3N+a+1jCM3zWQGQ6bGW/+3MP8RFCCN4FWKsmu0PelbBCw54+jcfi2RMjr+QUh69Zc39P+ylFYtcfmiNTAV4P7MfRYatR15k4wYHniEGhPnbuwQs/MtMhLSXbYCdbfFVxYohFWDoH021rbBv1qzIHDAFQPEMrZMOD2FqJ7mguMymu5N7OJGFiDfUc0OHYm2SwJyKrsA9v5c4i2tKO38HnmPZPfQMNRrfZ68FUWbJMCF8YASLTBc=~1; ak_bmsc=E7586FECFC0789AE9699BE7168A116C1~000000000000000000000000000000~YAAQZnkyFxwXU/mcAQAAwzEFCR/Er+mcYVXjBak+OqtZno85/GQtfnSYjuNzs9RqAxQmf+jHlBi0pkza/bgw9tPG20QUxLSSJ7QVIi1Zl9ZsLP/VxgA0tvRh5q4Jl9aTtrAbMB0VDJxrJXBg88cC8UQaGOkphaQVmKAKU80g177yPbFyODpOXVMoq6BW4idOhPISkJrvZ133zn54S3w8v5NW6WxUkTvOLPfCFF9iWTGCRRxx6bgX2GQcaEIj2kVNiwpovhlo4cg88gJxBAQFlscAMMmxOG09HLyGmDluLOsqqyWQ5qBFUN2k/m4794BUDe8YrOgF6auWEyS7Ly3YXtg2eBkMQJ8imOYU6qqwQzlmIiVJPsrEZ/+rzxwMH4tyHQ9cd8tzn2z92ggaUyE/INfD8IxuQay0blrJ3vUxP0KjBdajSoVoil9bxrZEfkfB61YniOqcQLKErEFsMKKaHpPYQhPlBluXhO1wB1s8V7M/5uufyrOXrlmL93wiBTGXMHwNeCww29v83xQ9vf7QlMR7duAphhLe; bm_ss=ab8e18ef4e; web-session-id=f44e2d46-f265-415b-a41e-b0fd278aa55b; _abck=065E9F34F28E2B1BC4EC774F65D71776~0~YAAQXbxBF9eYs/GcAQAA1kdiCQ+qbqBcUZMnm145OiRnZStW3s4ap9o+buuZeEzemcolPRVrudnf48S8/LR0QdDdm6+xx1BfTNoxMgpn3N8Y00eWCb+My/s1iPiLzCn5nzO6+YZoZdD8r9fbAGltS4DfSx0aMM9nKF3+FpJS3kVZrkvRQtx7/+A6EHdpHSVF1yNPnSJP/VbMtrRERnN3Sc0VN9RsG1EQCmN/vXUwhPQgTiQFkZwMGtkCWG3fosiu2iIEvx+Xc+LwYBcHN7fmdoUhq8r+gTXAo//PFvbGwINcYyeyQhbNd/o4HXTKZl556nD7M3MvBUhSjU2ehV76wNM326V438DoHxQwHt9PdlRkmtjItkyU09neqrhOeafAe1kzl1acl3LlvVwYKBVE2AdUh6OxHWUhBAQ6XGfP06hDqu+x5FFHwXffSGdSvMQ5hf9s2Drlr9QPWU9h8KffjD2fqRKnnu1OhehygvLtBPwdmpawvLSHPQxnFRhzm06k5XV3mojYEATYvenb6gvV41mKQhgGO2MfgiY1Jp8Db6F7V0df3UsHb/i63OEL+TNr6LTYLluhkVJQnjxjycSvSLoCZmYXZvz60/OYi1OfJU3dz+iinwSmVcjSyPszgIk2pdgpy9BdvS9Z9iWQzwRwFWtjFvDdNEBBH/UTqEN7lzc4GZh+5Lv6mr6FmoSiKbJSIJRdYiuoGXtof+y+zHjRtety0nwTDxx2VzUvxiKf+ypP/VRyEHgAKvoxYmfcpHf1oLb6ize/f2OAIvlZ2BY=~-1~-1~1773982449~AAQAAAAF%2f%2f%2f%2f%2f4deOMVbkxTJuKtKe+37EGk%2fihkthzhpGNiqdgxJZUIZMaiaKXWDbNCaUxepszYW35Kg3hy3G+tuJMUqt26rgGj60Yn9RTG+aOlSw0vGQW9d67Hh9TN0vS6N+nI1GtWoHSboNOi%2fGdrPw%2fLgJkjIpHRQwIOO9epej2dQgvWLhq33GMp8mpX7Ouuqtbile22glGuftqpR0AOc4mryZZyUHIoYfH1BfCuOMrhBiHH57wGcAVU%3d~-1; HOME_CARD_LIFE_NudgingSmsMfa=DISMISS; AWSALBTG=s0oRsuTUPMKhbQBu16g1MSj2J7IJU8yhU+a8NyRF1MGgvKB0e95NE/5+qcSETnkw9xGuGRs5FYScO8oD7HHVGoxJA40DJVlwylIrq0Pr43/eLpzTMYRY2dsvDHLMJtZRU/kRcH2nqJpWo6/8dqmKWOfpDy4nhS10NIRYWJi0cqyef9blZd0=; AWSALBTGCORS=s0oRsuTUPMKhbQBu16g1MSj2J7IJU8yhU+a8NyRF1MGgvKB0e95NE/5+qcSETnkw9xGuGRs5FYScO8oD7HHVGoxJA40DJVlwylIrq0Pr43/eLpzTMYRY2dsvDHLMJtZRU/kRcH2nqJpWo6/8dqmKWOfpDy4nhS10NIRYWJi0cqyef9blZd0=; bigfoot_browser_session_id=b5ca5d2f-2000-4a26-9e95-70e9989d8471; bm_so=54804B0E0CE407811D131CFBB214F9694C6642F759B5F4DF2548915967E641E8~YAAQbXkyFyfwsOicAQAAt7lsCQdUJpu8dApIDHsoLaQvMsFN1i71ZE4LzP+rCi9hXyBzgm/GMEdKs/ogymw1HZkzg1jCbz1qbQcxbkjlQtX7y92W5b53zSsp4/4hZX/Xown1hpi54cJ+qjN24ai8MK1qXGez8SrhlnGyILuJqzgiqYnWlIWlr3Bm1+KaDC+s52EvMy2GmEbFCwLCGQreTomAkt+EYJfPTJKXPCQDh3vEkWPCQjn7lU9/W4pAZU+nIbC3HPEJq9gVEPuz3X4I5Nu8hIb93i5mAPntp363xiEIdmlTc4vKd5BtxN9cTaVHOGGy7uYsvC58BGyIYgMSK0v3uiIeNO/Qs86wU5KxdlUVbUJyRLGHGPMFs8LcC+mfpyNCCAPmtYgeKtqn8iaDUNcYxhWfSEec2vPvxPbJsbISW7pGDUEg2Gsry50oO0liEaT/3sN9dOYjH+vlp4PlBTk=; bm_lso=54804B0E0CE407811D131CFBB214F9694C6642F759B5F4DF2548915967E641E8~YAAQbXkyFyfwsOicAQAAt7lsCQdUJpu8dApIDHsoLaQvMsFN1i71ZE4LzP+rCi9hXyBzgm/GMEdKs/ogymw1HZkzg1jCbz1qbQcxbkjlQtX7y92W5b53zSsp4/4hZX/Xown1hpi54cJ+qjN24ai8MK1qXGez8SrhlnGyILuJqzgiqYnWlIWlr3Bm1+KaDC+s52EvMy2GmEbFCwLCGQreTomAkt+EYJfPTJKXPCQDh3vEkWPCQjn7lU9/W4pAZU+nIbC3HPEJq9gVEPuz3X4I5Nu8hIb93i5mAPntp363xiEIdmlTc4vKd5BtxN9cTaVHOGGy7uYsvC58BGyIYgMSK0v3uiIeNO/Qs86wU5KxdlUVbUJyRLGHGPMFs8LcC+mfpyNCCAPmtYgeKtqn8iaDUNcYxhWfSEec2vPvxPbJsbISW7pGDUEg2Gsry50oO0liEaT/3sN9dOYjH+vlp4PlBTk=~1773979614597; bm_s=YAAQbXkyF4D6sOicAQAAluNsCQXjm+DGTBcUBwu4Pf5b/pISIFujPOo84FJUvPzpvGvghKICpR7RNjX8gIYC4WVZ91wt3pLzG9kP51fV+zcerJIe7OkC2Z1tCTB4E2szu6pf1CeslX6+4bF0hbC66E/48vVkjeKGttyfpCO0oCpcHvueD/u3khy6XKF33wr8b4qHA77K9Jwntx4O9z/Yl4pgMMGmrDnMUVMmoGzNK2O6WJh9EWfcUT6306iju1SGmZ+X/3XpzTiDA1CN5SJjTfrYiX8kv9+MUYo9HWUyI8Folhg+hjK6YPNVmH+16mu/9npAz2+klHk6zmmaEu+PvCyVoxihYMrZNzfxc1kURUd/9XCuQ3Sx+z5sdhNaTg8Agg99io+nSCoPirv3voCNm6ITex4MzSnyW9E68ursUI2OkXCfKm4Ek4yi5YE9BRcTksXQOXMJZNwDh+CR9CJ02iT2I9R9WaMeZfa627vM94JTLv0Mod/RoQ3s0R8cdYA94HgDv09oZburpfCzI0HZR773+7a6b/O9KW0pmVn0WkKRLQZ+IS4ttuApioNbpQtLXf+FFL7XSSWYn7FtnB9v+7I9yCHoLCvC2Hz81/HvHdYEeVG5wVp635Qe/mvLuBcU2IF6uRpwzCnWB91OEwAI/LxiOej7bUa4BioOr4EjliPpD4JtJ6H0EWyIdvZpEsnEtgGPkRSI2gkZjnlz04geN6CVABNaIizeXC+xFWPVtClHiw3wYpQxR4fqnXUO7crKr9WdJXtGt6acjqbJqNHNCfz2h7AclyfAAFEWNFBnAelWGWg5XK/+Jlcmh1jFpSM0zIKsCSXUss/UxOaccm1a9q8Qb9zj62L37aJWBGcsI60u6Dy9DGhZGLxDQo0WpUMpz/DZ+O03C+Hu7pnYFyZzkl69oBrzGZ1Yn513iiNsjk3VD8OdAmVgNRIQaVh00g==; bm_sz=A922AE1E387B5902C23D560E21F07D26~YAAQbXkyF4L6sOicAQAAluNsCR/RQu0YU3gBYZuDiUilzFrM5kFqOmyuh+canacGcAGDDhAbIYpXdXfPIQsafDa350lpya53YfactKXvsqq83jOcXRwT4X1PjthUfDm1MWAgRgFJ1ij2E/8Tocp+F8te1ENsdg0VoUd58/uAQsMHLmSNiKgNdPFF0D/Ijoh7ZIHL+TxBbvz6OEJZYLGvrfe8KqVW2z8mP83K0ZjehnRUAdEJhPDOYIOMsyW6ApN/0NWHu/TUnk0iPWcZ+QF9ai8uGM2d8g/A2i9DvDUFGnj2keBE/YevCv6nu2h3nzlr6wM5DDO0c2/aMEQyqvPeMd7B/EeetL+N/wOFKNAl8tHvnStW7PEDzlRmDQq9nI7PtWsSGMwDVcnr9n8ISmDpuEprJhagrjf88AnjpGkDqiKASP3zVmlW6B7zVfbqjCGwNmQP0J2emaNLkWWAw0c4ls5/4JCPnTOZyhilF2iHF1SlzigpPsBNAGl7D9GDpeESjpZZGco+P97NEOhXo3abB4kk/uop4X9KhcTdqOvgMKHvgG0e69vqbDrL3FI=~4408388~4534835; fs_lua=1.1773979624815; fs_uid=#o-24BWCV-na1#3c89c560-df0c-424f-8e16-64bc370e2a48:227267ae-243b-4eaf-8280-2d16c59924e7:1773978568025::6#8afb4a58#/1804743907; JSESSIONID=2A095A4A0F1F0CF1E9A5910733908F1D; bm_sv=46AC3BC3EF8C36FFD8E3B2EFCAD36CA8~YAAQbXkyF2QIseicAQAAJCBtCR/NrYL1znlF0uSO/ZibjLmuDtzOFCTsH6GupggIzONbl2IRn3bUs/sbCGl9Bkwy1pI1XNZibXtH8mb/sXktmzJ1ew2ucz3j6+SEK8Mo3NJGroQggQc43mtjA2hsZ1t6gAihsTXOO+Zvwaj+KgoNIm3HWDMCKI2Va0B3x5EiwIsGvQfpPISyRt4rEnnrVjFwiIB1Df3yNuhtOUM9lEuR17OonHxJnTVRU8SvbydK1Vur~1',
}


# =========================================================
# 1. URL
# =========================================================
META_CATEGORY_URL = "https://wing.coupang.com/tenants/rfm/api/product/meta/category/{}"
WAREHOUSING_FEE_URL = "https://wing.coupang.com/tenants/rfm/accounting-fee/lowasp/warehousing-fee"
FULFILLMENT_FEE_URL = "https://wing.coupang.com/tenants/rfm/accounting-fee/lowasp/fulfillment-fee"


# =========================================================
# 2. 공통 함수
# =========================================================
def to_int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None

def get_json_with_retry(method, url, *, cookies, headers, json_data=None, max_retries=3, timeout=30):
    """
    GET/POST 요청 공통 재시도 함수
    - ConnectionError, Timeout 시 재시도
    """
    for attempt in range(1, max_retries + 1):
        try:
            if method.upper() == "GET":
                response = requests.get(
                    url,
                    cookies=cookies,
                    headers=headers,
                    timeout=timeout,
                )
            elif method.upper() == "POST":
                response = requests.post(
                    url,
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                    timeout=timeout,
                )
            else:
                raise ValueError(f"지원하지 않는 method: {method}")

            response.raise_for_status()
            return response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"[재시도 {attempt}/{max_retries}] {method} {url} / {type(e).__name__}")
            if attempt == max_retries:
                raise
            time.sleep(2)

        except requests.exceptions.RequestException:
            raise


def extract_fee_map(fee_data):
    """
    fee 응답에서 MINI, SMALL만 뽑아서
    (capacityType, minPrice) -> 금액 dict 로 변환
    """
    fee_map = {}

    items = fee_data.get("feeRatesBySingleCategoryResponseV1", [])

    for item in items:
        calc_after = item.get("calculatedFeesAfterPromotion", {})
        calculated_fees = calc_after.get("calculatedFees", [])

        for fee_group in calculated_fees:
            capacity_type = str(fee_group.get("capacityType", "")).upper()

            # MINI, SMALL만 추출
            if capacity_type not in ["MINI", "SMALL"]:
                continue

            for price_row in fee_group.get("feeByMinPrice", []):
                min_price = price_row.get("minPrice", {}).get("amount")
                configured_amount = (
                    price_row.get("configuredFee", {})
                    .get("amount", {})
                    .get("amount")
                )
                final_amount = (
                    price_row.get("configuredFee", {})
                    .get("finalAmount", {})
                    .get("amount")
                )

                fee_map[(capacity_type, min_price)] = {
                    "configuredAmount": configured_amount,
                    "finalAmount": final_amount,
                }

    return fee_map


# =========================================================
# 3. coupang_categories.json 읽기
# =========================================================
with open("coupang_categories.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# =========================================================
# 4. 말단 카테고리 추출
# =========================================================
leaf_rows = []

def walk(node):
    dto = node.get("displayItemCategoryDto", {})
    children = node.get("child", [])

    if not children:
        leaf_rows.append({
            "displayItemCategoryId": dto.get("displayItemCategoryId"),
            "displayItemCategoryCode": dto.get("displayItemCategoryCode"),
            "treeCategoryName": dto.get("name"),
            "categoryPath": dto.get("categoryPath"),
        })

    for child in children:
        walk(child)

walk(data)

print("전체 말단 카테고리 수:", len(leaf_rows))


# =========================================================
# 5. 공구 카테고리만 필터
# =========================================================
leaf_rows = [row for row in leaf_rows if "공구" in row["categoryPath"]]

print("공구 카테고리 수:", len(leaf_rows))
print("공구 카테고리 샘플 5개:")
for row in leaf_rows[:5]:
    print(row)


# =========================================================
# 6. 수집 시작
# =========================================================
all_rows = []

empty_meta_ids = []
dns_error_meta_ids = []
other_error_meta_ids = []

total_count = len(leaf_rows)

for idx, leaf in enumerate(leaf_rows, start=1):
    meta_category_id = leaf["displayItemCategoryCode"]

    try:
        # -------------------------------------------------
        # 6-1. metaCategoryId -> feeCategoryId 변환
        # -------------------------------------------------
        meta_url = META_CATEGORY_URL.format(meta_category_id)
        meta_data = get_json_with_retry(
            "GET",
            meta_url,
            cookies=cookies,
            headers=headers,
            max_retries=3,
            timeout=30,
        )

        if not meta_data:
            empty_meta_ids.append(meta_category_id)
            print(f"[건너뜀] {idx}/{total_count} meta={meta_category_id} 응답 없음")
            continue

        fee_category_id = meta_data[0].get("categoryId")
        fee_category_name = meta_data[0].get("name", "")

        if not fee_category_id:
            empty_meta_ids.append(meta_category_id)
            print(f"[건너뜀] {idx}/{total_count} meta={meta_category_id} fee_category_id 없음")
            continue

        # -------------------------------------------------
        # 6-2. payload
        # -------------------------------------------------
        json_data = {
            "agreementScope": "PRODUCTION",
            "leafKanCategoryIds": [fee_category_id],
            "unit1Unit2CategoryNames": [],
        }

        # -------------------------------------------------
        # 6-3. 입출고비 조회
        # -------------------------------------------------
        warehousing_data = get_json_with_retry(
            "POST",
            WAREHOUSING_FEE_URL,
            cookies=cookies,
            headers=headers,
            json_data=json_data,
            max_retries=3,
            timeout=30,
        )

        # -------------------------------------------------
        # 6-4. 배송비 조회
        # -------------------------------------------------
        fulfillment_data = get_json_with_retry(
            "POST",
            FULFILLMENT_FEE_URL,
            cookies=cookies,
            headers=headers,
            json_data=json_data,
            max_retries=3,
            timeout=30,
        )

        warehousing_map = extract_fee_map(warehousing_data)
        fulfillment_map = extract_fee_map(fulfillment_data)

        all_keys = sorted(
            set(warehousing_map.keys()) | set(fulfillment_map.keys()),
            key=lambda x: (x[0], int(x[1]) if x[1] is not None else -1)
        )

        if not all_keys:
            empty_meta_ids.append(meta_category_id)
            print(f"[건너뜀] {idx}/{total_count} meta={meta_category_id} fee 데이터 없음")
            continue

        for capacity_type, min_price in all_keys:
            wh = warehousing_map.get((capacity_type, min_price), {})
            fu = fulfillment_map.get((capacity_type, min_price), {})

            category_path = leaf["categoryPath"]
            if category_path.startswith("ROOT>"):
                category_path = category_path[len("ROOT>"):]

            all_rows.append({
                "displayItemCategoryId": leaf["displayItemCategoryId"],
                "metaCategoryId": meta_category_id,
                "treeCategoryName": leaf["treeCategoryName"],
                "feeCategoryName": fee_category_name,
                "feeCategoryId": fee_category_id,
                "categoryPath": category_path,
                "capacityType": capacity_type,
                "minPrice": to_int(min_price),
                "warehousingConfiguredAmount": to_int(wh.get("configuredAmount")),
                "warehousingFinalAmount": to_int(wh.get("finalAmount")),
                "fulfillmentConfiguredAmount": to_int(fu.get("configuredAmount")),
                "fulfillmentFinalAmount": to_int(fu.get("finalAmount")),
            })


        print(f"[완료] {idx}/{total_count} / meta={meta_category_id} / {leaf['treeCategoryName']}")

        # 너무 빠르게 치지 않게 약간 쉬기
        time.sleep(0.5)

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        dns_error_meta_ids.append(meta_category_id)
        print(f"[오류] {idx}/{total_count} / meta={meta_category_id} / {type(e).__name__} / {e}")

    except Exception as e:
        other_error_meta_ids.append(meta_category_id)
        print(f"[오류] {idx}/{total_count} / meta={meta_category_id} / {type(e).__name__} / {e}")


# =========================================================
# 7. 최종 xlsx 저장
# =========================================================
df = pd.DataFrame(all_rows)
df.to_excel("coupang_fee_tool_mini_small_with_fulfillment.xlsx", index=False)

print("엑셀 저장 완료: coupang_fee_tool_mini_small_with_fulfillment.xlsx")
print("총 행 수:", len(df))


# =========================================================
# 8. 실패 목록 저장
# =========================================================
with open("empty_meta_ids.txt", "w", encoding="utf-8") as f:
    for x in empty_meta_ids:
        f.write(str(x) + "\n")

with open("dns_error_meta_ids.txt", "w", encoding="utf-8") as f:
    for x in dns_error_meta_ids:
        f.write(str(x) + "\n")

with open("other_error_meta_ids.txt", "w", encoding="utf-8") as f:
    for x in other_error_meta_ids:
        f.write(str(x) + "\n")

print("실패 목록 저장 완료:")
print("- empty_meta_ids.txt")
print("- dns_error_meta_ids.txt")
print("- other_error_meta_ids.txt")