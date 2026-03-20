import requests
import csv

cookies = {
    'PCID': '17726070646965999973782',
    'x-coupang-target-market': 'KR',
    'x-coupang-accept-language': 'ko-KR',
    'sid': '7fa02b5efeca43f0971d09fd4b85041061534995',
    'OAuth_Token_Request_State': '09106985-8441-4c60-973d-43b2c2cbd945',
    'ak_bmsc': '517CBE222E36BE4B3E1AB592BA70867B~000000000000000000000000000000~YAAQLq0sF67rAvKcAQAAntOWCB8MenCtyadBBSt4n8zlY4IIebKougvSI2MJ1OH7qYL6iLYqu/+Wgd5WEGhKc8vBTeFEghZRm4Z8W5B4MRz8s1OdmVU/8noMBqG2JBKwvO32K3hzfaye8zrKRsdzoZTI2Ew3KKuJvYpTPxvuw72eW0rZDAZk6VTOTCSIbS6CNBehXhqowFuzWOMwx8i70v7h6ysC7Qia6WSc7nJs6bAa5TD/g+qqimrVwET0Qe/aRsk6UM5d2IInrBeVVCTYKMFjBFpXQIYYc4jJt4MKkLjBvmm9vj+xchtjZ1MTW+E67KLH+YNQVJInVwvpKPWuivcw5i3BdQL7T+JmctL/sxbfBv3HekikPvh9N17ce4fgbrDT8SK6lKM2G9zqHlnS9PVU6YhOv8k/TOkB+oX4UCKuObGlQ8bTPPg4SwiuAyW0ppU+y9v3R6z4koIrFCkI4l8=',
    'sc_vid': 'A00193388',
    'sc_lid': 'ckm00285',
    'sc_uid': 'eRXuy7/LuxetxfJ+eZl6NHnSeKo+PF1TRYzZ2Ml/Z0iYBja0YjorhEBBquNHLhc=',
    'wing-market': 'KR',
    'wing-locale': 'ko',
    'sxSessionId': 'NTU2MDA2YTUtZGE3NC00MDEwLWFlZmItZjMzNDQ1MmNkMGJl',
    'XSRF-TOKEN': 'b16f83a4-b2fb-4cd3-8294-8d2a1f7f9cf5',
    'AWSALBTG': 'SZ6e9S4qQb4/bAMqCfoRWk96IAs8Hmm13Vqf7Ur3lPe5qV4S5MxaU2Whgwwd3XS4aHRilRHK1eUuq0XU8mfvGpC9SSv33dwCbmG9xZaJsmSMkXpTt+MlS5DHW3yS+aad9ZagYkLzPlBuNkfjfWfSSrfPZaL2TLapZKnSiTKPXFbKV8lnGvE=',
    'AWSALBTGCORS': 'SZ6e9S4qQb4/bAMqCfoRWk96IAs8Hmm13Vqf7Ur3lPe5qV4S5MxaU2Whgwwd3XS4aHRilRHK1eUuq0XU8mfvGpC9SSv33dwCbmG9xZaJsmSMkXpTt+MlS5DHW3yS+aad9ZagYkLzPlBuNkfjfWfSSrfPZaL2TLapZKnSiTKPXFbKV8lnGvE=',
    'web-session-id': '2c5327dc-68f3-4aed-8dc6-5f2f9e9af819',
    'bm_ss': 'ab8e18ef4e',
    'CGSID_PARTNERADMINWEB': 'cda906caaabf4bafbbcbf00d95702230',
    '_abck': '065E9F34F28E2B1BC4EC774F65D71776~0~YAAQRbxBFwztK/6cAQAAexr0CA/YTjP/I0PDouof48YxaXI5QMre+dGa+DtmSamDhdQU5iK2Xfj/JepP3mLxYIH6hf8qQIVdzwhl5XbAlF9yg+MlB9KJ56NANTj8GstfcRNBvZo/7K3TzKGsn6C+UFdchBeOtSQBMf+H8LfcSg9KMDuPKkluw5nbcAu8AGP9SgKPHpSfZB8UfuA5HsD7g3doeFHqL6eQHIt4S9+d4lvMUKU+COS9k9z4iUPRRTZcNl+FiRR4fvHmZLRChSBR1NyTkBcpXFgOsIdl+zu247ZkJDMfZqz/FOAaONbu0P18sNWaab2M3x9ojuunOs42N4TwwfQ4+yxYDWo10FV65xsmsgxctZDVXDgJIp0A+XXoZqaLuri6GoEVByKJDhRncJoDsAXn86fveIQwXbct1Z52jl2uI/tRebDWmqLYe0E/mE5U+q5QLwcMPIt45MSnKnuQb90+SQZpkcnYmaIxQInBN1g17v48lhL/Y6ISMIzqG2wZ1rS1lEoYyVUxpo30rb/y+KeVDhiJQsSe8mQp6v9fyn2WtHouIgxmg5WXkeRoRIq1FR68RyXwdzwg/80jWgAJG3l88oWLXHoTcxLYoRWX9lXApuRYJoek7+3+TLAxGbfdwKJrMtMyb0ZRpN69/9KipuNZlX997iCqPmC2wltGEv/jm5Ee6xmcBpnfTAia1wp+t27diKPVnCQ9DI/BmoFoegxtEjHeEIu6h/Me77NlSgunJCvOmOWfjFsKBA6EVATpUCWPWDxLqOP+XYs=~-1~-1~1773975302~AAQAAAAF%2f%2f%2f%2f%2fxPc+PzGJUOX36vgXoY+qG24fHpBeVPS2tPxoTvPOF5PNZz2g6KyiC40Mw3CI7PAaS%2fMZ8+zV3ysM8cqw4kaJvMe8kfCFhyftLGnBe1E8rHAOgBlsTJ5rU1g0hooxpf9v6dhGkmO%2f1lwFYRzYqoLha3fuhtbQW+o5spJ8RxzrqcoYsxiT3K0dVsuwMx3CGWbm9CvCxAgPlZqjkSG8foG%2frn4pfow9irNLbS7rQXbC7j%2fwHY%3d~-1',
    'bigfoot_browser_session_id': 'af83e798-0cf7-4f83-bdcd-f05bf760890e',
    'bm_sz': 'A922AE1E387B5902C23D560E21F07D26~YAAQRbxBF1jbLf6cAQAAmVv3CB/wHpAFx3ilWbtNop53eIje1z7fLKIBioRu32Wy+8P4XYngTPRhLSNgByD8ZHgNtWAMBa2Rfod0tQCAyPGGyQZbKpGMCwLd+BCLz2b54YTV8KYdEVY+MjGMuKyh/lvx4D9z4DXIm2seP+CMl5EBvq4E/2Q0n69Bn1/fnNbvueHt7BD+Fewr0F+kk/XTMQMDvNPa6wriv4qvmjHSJbY+YtQK/eA2AHkxIDW5gP88hqbywphL6Do2LiVJ31tB/ojvW8AcHiZIGJye+K7JQgolzM0+hoO3EOxwP3QS2LJUJ7cor6ue80C1sW99Jmb2/hdR2ncSL65h08LIILDECIQmRl3CJRYsJvXjHhEixQzTfKkN0IGOKEWzPRBIt2PJka3wYTJugwI9d4DnMp+IES4AegpNqDnGyE0e3x2VHP1qz9ZGmDlku1tKIejpaD4Ofg==~4408388~4534835',
    'fs_uid': '#o-24BWCV-na1#3c89c560-df0c-424f-8e16-64bc370e2a48:290d3be8-5e90-4510-9fb8-336748a647fd:1773969042778::8#8afb4a58#/1804743868',
    'JSESSIONID': 'B1BE39FA7D95DBEBE43194C65EC37F35',
    'fs_lua': '1.1773972218832',
    'bm_so': '64E0F18DFB10F959BFC57D992E58FD93C82E8D5C227ED159FE8A565382BEC308~YAAQd3kyF8B3leScAQAAFZ/+CAejran+nBoDYiDgA1cf8OMpHzyyqa+wAJk2zFPjZJqom7+r7AyTgXFRz0fQ4G9eSstINcobzl/XCp4gerMOIps+YswOwPS+JTsZm0sfVhQT96Kw1CuvAU8cHySXPX5wG580xxHNM2hLVDLvhSopRdtuiOppEhWgbYOmjCLdGGdb1bcWuuP0JrzJZ6J9veFxw19ZrvKHGhB5WcN6lR49rfX53CF7Ct/emjq2wouDU9v1VWT/NqN6aGRPuns6ZsJGxFuOsiBrsTOMDkCQWoW4nXqn6oU05NPv17oNGdWUyiAg0CjVdLtvR6E60fw3WpAC0t/N+ygyXt8dy8SY+/S01BQTTdASPsjeWXOv8CQ3QdOhBCqp/dwAQzC77W45BWDM/IOgNvW7UW3ZW7koadEL3aPuRHRo5xvVFyu9KIWdmjxF/d9eZ5FWH/PwaH4MVi4=',
    'bm_sv': '8C95BFBD2D127B1D62586FEB61C06BC9~YAAQd3kyF8F3leScAQAAFZ/+CB+nHrJTxEHjnSwXHC7JbHumplDng/GDV7B0QYgHK3lDaAVuAMK6qB43303c2tVFojPnClarur2aG0a3P51F3TeGVxyAkKjVIMN8VkZds28dGkwYHo3fMzE1lk3hyp8g4TZU/FZ296qgx74nI4f6THvX8cQApXfpXkSNgPjdcloqF7VZ0P1cXwdreUA/FpgoGGTrM9aVkRK2OPHT/XAnMiJiwtbYHjb8MUgm5v84GBFz~1',
    'bm_lso': '64E0F18DFB10F959BFC57D992E58FD93C82E8D5C227ED159FE8A565382BEC308~YAAQd3kyF8B3leScAQAAFZ/+CAejran+nBoDYiDgA1cf8OMpHzyyqa+wAJk2zFPjZJqom7+r7AyTgXFRz0fQ4G9eSstINcobzl/XCp4gerMOIps+YswOwPS+JTsZm0sfVhQT96Kw1CuvAU8cHySXPX5wG580xxHNM2hLVDLvhSopRdtuiOppEhWgbYOmjCLdGGdb1bcWuuP0JrzJZ6J9veFxw19ZrvKHGhB5WcN6lR49rfX53CF7Ct/emjq2wouDU9v1VWT/NqN6aGRPuns6ZsJGxFuOsiBrsTOMDkCQWoW4nXqn6oU05NPv17oNGdWUyiAg0CjVdLtvR6E60fw3WpAC0t/N+ygyXt8dy8SY+/S01BQTTdASPsjeWXOv8CQ3QdOhBCqp/dwAQzC77W45BWDM/IOgNvW7UW3ZW7koadEL3aPuRHRo5xvVFyu9KIWdmjxF/d9eZ5FWH/PwaH4MVi4=~1773972398493',
    'bm_s': 'YAAQd3kyF0J5leScAQAAIqT+CAVLNc86SIlkHJqH7CGKrKN9mrtil/CuySfIbHl1lIO2vxSqwCACRrKbpO4dZmoWRaRA0UqfEq48e3bX74vcc6hge8LZd5XeyS6OFeMQfdVcWgzdMEyfOvuas2JZSkp4Xf7MQBjxtMXMsCiKa2IFQxkidTn5wt0rGLJ+TUZM4hqpg0uhgUTdPXZ2TsrxXRExlVlh7OyqNiqds8N53givxab24u/6uj0uPsbmf4MgomDmnKDk0BTk6dhu682Y5uoL/O+FWM95FirQknGWtj6msH7f1Xqcph7t6yWtDVKE1YfsZOY7OWPSFI2JORRwcGGZ2aerRaeXHjoze9xLMx61uJ2HBATM2DZbIxZBrdE/dHDOAFbM+EuP3mKsXfDPDAak3dklM059cGuihZyAVD28Z9Pzh2qGw62ijebTH4uFEnoxsD6HIXy0c/lvKxAzIkHSgvsIfPUowta9WLV3v/GkVNwvMp/6enGs++ZymdzwwQ36k8Gux46UEi+2MtelMGMqpbC61odWnp/VIAmTz5WJ6qTfSO+e+M9+SzV/2jvU5T+0JUKffo66dGBrT3/HrZHWZApSkG11G+QeTSlecQv3ljykaXxjxd6P7mjY+D5wvXYFn6wgSWN6dkXbUHuib/aQGfZl07YDUejnni4kAmHLUYFnkqDAvAzyvjOr/VMyG8Ehke9zxhesjpWrYN/hvBtOxe1RCykcPXmV0ytZUJ4qE5c8CzSXB2tgjADIDt5IfOb8oa6qplVjd70SwGmzoX+oqkxXBBgNDkmcckstbHpvkLz+CwPJmSdAEnLgjoQiI/Q3prg7oWPETzg7alOXxg7FzpeWbocsxmGt5rlOuPqHpvqQdALs8JppmgHW8dhvA6cCEJBc+IwZhl7apv4OMpjevTrZG8REXMN8L9cEFAVZ7pdm8s+NvYsNWI81MA==',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=f32d75da7b425b59baaa1b97acb63e642f66ca88,sentry-public_key=5f0c21cbbd20390ab64c6c3fb52d4a5f,sentry-trace_id=a12392deefdf400f82bd641d345a8538',
    'priority': 'u=1, i',
    'referer': 'https://wing.coupang.com/tenants/rfm/settlements/fee-details',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'a12392deefdf400f82bd641d345a8538-8e7d4d7ede4a06fc',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'withcredentials': 'true',
    'x-rfm-portal2-request-id': 'sm0Tkn_z7XR6Mrmk-5rXu',
    'x-xsrf-token': 'b16f83a4-b2fb-4cd3-8294-8d2a1f7f9cf5',
    # 'cookie': 'PCID=17726070646965999973782; x-coupang-target-market=KR; x-coupang-accept-language=ko-KR; sid=7fa02b5efeca43f0971d09fd4b85041061534995; OAuth_Token_Request_State=09106985-8441-4c60-973d-43b2c2cbd945; ak_bmsc=517CBE222E36BE4B3E1AB592BA70867B~000000000000000000000000000000~YAAQLq0sF67rAvKcAQAAntOWCB8MenCtyadBBSt4n8zlY4IIebKougvSI2MJ1OH7qYL6iLYqu/+Wgd5WEGhKc8vBTeFEghZRm4Z8W5B4MRz8s1OdmVU/8noMBqG2JBKwvO32K3hzfaye8zrKRsdzoZTI2Ew3KKuJvYpTPxvuw72eW0rZDAZk6VTOTCSIbS6CNBehXhqowFuzWOMwx8i70v7h6ysC7Qia6WSc7nJs6bAa5TD/g+qqimrVwET0Qe/aRsk6UM5d2IInrBeVVCTYKMFjBFpXQIYYc4jJt4MKkLjBvmm9vj+xchtjZ1MTW+E67KLH+YNQVJInVwvpKPWuivcw5i3BdQL7T+JmctL/sxbfBv3HekikPvh9N17ce4fgbrDT8SK6lKM2G9zqHlnS9PVU6YhOv8k/TOkB+oX4UCKuObGlQ8bTPPg4SwiuAyW0ppU+y9v3R6z4koIrFCkI4l8=; sc_vid=A00193388; sc_lid=ckm00285; sc_uid=eRXuy7/LuxetxfJ+eZl6NHnSeKo+PF1TRYzZ2Ml/Z0iYBja0YjorhEBBquNHLhc=; wing-market=KR; wing-locale=ko; sxSessionId=NTU2MDA2YTUtZGE3NC00MDEwLWFlZmItZjMzNDQ1MmNkMGJl; XSRF-TOKEN=b16f83a4-b2fb-4cd3-8294-8d2a1f7f9cf5; AWSALBTG=SZ6e9S4qQb4/bAMqCfoRWk96IAs8Hmm13Vqf7Ur3lPe5qV4S5MxaU2Whgwwd3XS4aHRilRHK1eUuq0XU8mfvGpC9SSv33dwCbmG9xZaJsmSMkXpTt+MlS5DHW3yS+aad9ZagYkLzPlBuNkfjfWfSSrfPZaL2TLapZKnSiTKPXFbKV8lnGvE=; AWSALBTGCORS=SZ6e9S4qQb4/bAMqCfoRWk96IAs8Hmm13Vqf7Ur3lPe5qV4S5MxaU2Whgwwd3XS4aHRilRHK1eUuq0XU8mfvGpC9SSv33dwCbmG9xZaJsmSMkXpTt+MlS5DHW3yS+aad9ZagYkLzPlBuNkfjfWfSSrfPZaL2TLapZKnSiTKPXFbKV8lnGvE=; web-session-id=2c5327dc-68f3-4aed-8dc6-5f2f9e9af819; bm_ss=ab8e18ef4e; CGSID_PARTNERADMINWEB=cda906caaabf4bafbbcbf00d95702230; _abck=065E9F34F28E2B1BC4EC774F65D71776~0~YAAQRbxBFwztK/6cAQAAexr0CA/YTjP/I0PDouof48YxaXI5QMre+dGa+DtmSamDhdQU5iK2Xfj/JepP3mLxYIH6hf8qQIVdzwhl5XbAlF9yg+MlB9KJ56NANTj8GstfcRNBvZo/7K3TzKGsn6C+UFdchBeOtSQBMf+H8LfcSg9KMDuPKkluw5nbcAu8AGP9SgKPHpSfZB8UfuA5HsD7g3doeFHqL6eQHIt4S9+d4lvMUKU+COS9k9z4iUPRRTZcNl+FiRR4fvHmZLRChSBR1NyTkBcpXFgOsIdl+zu247ZkJDMfZqz/FOAaONbu0P18sNWaab2M3x9ojuunOs42N4TwwfQ4+yxYDWo10FV65xsmsgxctZDVXDgJIp0A+XXoZqaLuri6GoEVByKJDhRncJoDsAXn86fveIQwXbct1Z52jl2uI/tRebDWmqLYe0E/mE5U+q5QLwcMPIt45MSnKnuQb90+SQZpkcnYmaIxQInBN1g17v48lhL/Y6ISMIzqG2wZ1rS1lEoYyVUxpo30rb/y+KeVDhiJQsSe8mQp6v9fyn2WtHouIgxmg5WXkeRoRIq1FR68RyXwdzwg/80jWgAJG3l88oWLXHoTcxLYoRWX9lXApuRYJoek7+3+TLAxGbfdwKJrMtMyb0ZRpN69/9KipuNZlX997iCqPmC2wltGEv/jm5Ee6xmcBpnfTAia1wp+t27diKPVnCQ9DI/BmoFoegxtEjHeEIu6h/Me77NlSgunJCvOmOWfjFsKBA6EVATpUCWPWDxLqOP+XYs=~-1~-1~1773975302~AAQAAAAF%2f%2f%2f%2f%2fxPc+PzGJUOX36vgXoY+qG24fHpBeVPS2tPxoTvPOF5PNZz2g6KyiC40Mw3CI7PAaS%2fMZ8+zV3ysM8cqw4kaJvMe8kfCFhyftLGnBe1E8rHAOgBlsTJ5rU1g0hooxpf9v6dhGkmO%2f1lwFYRzYqoLha3fuhtbQW+o5spJ8RxzrqcoYsxiT3K0dVsuwMx3CGWbm9CvCxAgPlZqjkSG8foG%2frn4pfow9irNLbS7rQXbC7j%2fwHY%3d~-1; bigfoot_browser_session_id=af83e798-0cf7-4f83-bdcd-f05bf760890e; bm_sz=A922AE1E387B5902C23D560E21F07D26~YAAQRbxBF1jbLf6cAQAAmVv3CB/wHpAFx3ilWbtNop53eIje1z7fLKIBioRu32Wy+8P4XYngTPRhLSNgByD8ZHgNtWAMBa2Rfod0tQCAyPGGyQZbKpGMCwLd+BCLz2b54YTV8KYdEVY+MjGMuKyh/lvx4D9z4DXIm2seP+CMl5EBvq4E/2Q0n69Bn1/fnNbvueHt7BD+Fewr0F+kk/XTMQMDvNPa6wriv4qvmjHSJbY+YtQK/eA2AHkxIDW5gP88hqbywphL6Do2LiVJ31tB/ojvW8AcHiZIGJye+K7JQgolzM0+hoO3EOxwP3QS2LJUJ7cor6ue80C1sW99Jmb2/hdR2ncSL65h08LIILDECIQmRl3CJRYsJvXjHhEixQzTfKkN0IGOKEWzPRBIt2PJka3wYTJugwI9d4DnMp+IES4AegpNqDnGyE0e3x2VHP1qz9ZGmDlku1tKIejpaD4Ofg==~4408388~4534835; fs_uid=#o-24BWCV-na1#3c89c560-df0c-424f-8e16-64bc370e2a48:290d3be8-5e90-4510-9fb8-336748a647fd:1773969042778::8#8afb4a58#/1804743868; JSESSIONID=B1BE39FA7D95DBEBE43194C65EC37F35; fs_lua=1.1773972218832; bm_so=64E0F18DFB10F959BFC57D992E58FD93C82E8D5C227ED159FE8A565382BEC308~YAAQd3kyF8B3leScAQAAFZ/+CAejran+nBoDYiDgA1cf8OMpHzyyqa+wAJk2zFPjZJqom7+r7AyTgXFRz0fQ4G9eSstINcobzl/XCp4gerMOIps+YswOwPS+JTsZm0sfVhQT96Kw1CuvAU8cHySXPX5wG580xxHNM2hLVDLvhSopRdtuiOppEhWgbYOmjCLdGGdb1bcWuuP0JrzJZ6J9veFxw19ZrvKHGhB5WcN6lR49rfX53CF7Ct/emjq2wouDU9v1VWT/NqN6aGRPuns6ZsJGxFuOsiBrsTOMDkCQWoW4nXqn6oU05NPv17oNGdWUyiAg0CjVdLtvR6E60fw3WpAC0t/N+ygyXt8dy8SY+/S01BQTTdASPsjeWXOv8CQ3QdOhBCqp/dwAQzC77W45BWDM/IOgNvW7UW3ZW7koadEL3aPuRHRo5xvVFyu9KIWdmjxF/d9eZ5FWH/PwaH4MVi4=; bm_sv=8C95BFBD2D127B1D62586FEB61C06BC9~YAAQd3kyF8F3leScAQAAFZ/+CB+nHrJTxEHjnSwXHC7JbHumplDng/GDV7B0QYgHK3lDaAVuAMK6qB43303c2tVFojPnClarur2aG0a3P51F3TeGVxyAkKjVIMN8VkZds28dGkwYHo3fMzE1lk3hyp8g4TZU/FZ296qgx74nI4f6THvX8cQApXfpXkSNgPjdcloqF7VZ0P1cXwdreUA/FpgoGGTrM9aVkRK2OPHT/XAnMiJiwtbYHjb8MUgm5v84GBFz~1; bm_lso=64E0F18DFB10F959BFC57D992E58FD93C82E8D5C227ED159FE8A565382BEC308~YAAQd3kyF8B3leScAQAAFZ/+CAejran+nBoDYiDgA1cf8OMpHzyyqa+wAJk2zFPjZJqom7+r7AyTgXFRz0fQ4G9eSstINcobzl/XCp4gerMOIps+YswOwPS+JTsZm0sfVhQT96Kw1CuvAU8cHySXPX5wG580xxHNM2hLVDLvhSopRdtuiOppEhWgbYOmjCLdGGdb1bcWuuP0JrzJZ6J9veFxw19ZrvKHGhB5WcN6lR49rfX53CF7Ct/emjq2wouDU9v1VWT/NqN6aGRPuns6ZsJGxFuOsiBrsTOMDkCQWoW4nXqn6oU05NPv17oNGdWUyiAg0CjVdLtvR6E60fw3WpAC0t/N+ygyXt8dy8SY+/S01BQTTdASPsjeWXOv8CQ3QdOhBCqp/dwAQzC77W45BWDM/IOgNvW7UW3ZW7koadEL3aPuRHRo5xvVFyu9KIWdmjxF/d9eZ5FWH/PwaH4MVi4=~1773972398493; bm_s=YAAQd3kyF0J5leScAQAAIqT+CAVLNc86SIlkHJqH7CGKrKN9mrtil/CuySfIbHl1lIO2vxSqwCACRrKbpO4dZmoWRaRA0UqfEq48e3bX74vcc6hge8LZd5XeyS6OFeMQfdVcWgzdMEyfOvuas2JZSkp4Xf7MQBjxtMXMsCiKa2IFQxkidTn5wt0rGLJ+TUZM4hqpg0uhgUTdPXZ2TsrxXRExlVlh7OyqNiqds8N53givxab24u/6uj0uPsbmf4MgomDmnKDk0BTk6dhu682Y5uoL/O+FWM95FirQknGWtj6msH7f1Xqcph7t6yWtDVKE1YfsZOY7OWPSFI2JORRwcGGZ2aerRaeXHjoze9xLMx61uJ2HBATM2DZbIxZBrdE/dHDOAFbM+EuP3mKsXfDPDAak3dklM059cGuihZyAVD28Z9Pzh2qGw62ijebTH4uFEnoxsD6HIXy0c/lvKxAzIkHSgvsIfPUowta9WLV3v/GkVNwvMp/6enGs++ZymdzwwQ36k8Gux46UEi+2MtelMGMqpbC61odWnp/VIAmTz5WJ6qTfSO+e+M9+SzV/2jvU5T+0JUKffo66dGBrT3/HrZHWZApSkG11G+QeTSlecQv3ljykaXxjxd6P7mjY+D5wvXYFn6wgSWN6dkXbUHuib/aQGfZl07YDUejnni4kAmHLUYFnkqDAvAzyvjOr/VMyG8Ehke9zxhesjpWrYN/hvBtOxe1RCykcPXmV0ytZUJ4qE5c8CzSXB2tgjADIDt5IfOb8oa6qplVjd70SwGmzoX+oqkxXBBgNDkmcckstbHpvkLz+CwPJmSdAEnLgjoQiI/Q3prg7oWPETzg7alOXxg7FzpeWbocsxmGt5rlOuPqHpvqQdALs8JppmgHW8dhvA6cCEJBc+IwZhl7apv4OMpjevTrZG8REXMN8L9cEFAVZ7pdm8s+NvYsNWI81MA==',
}

response = requests.get(
    'https://wing.coupang.com/tenants/rfm/api/product/meta/category/64224',
    cookies=cookies,
    headers=headers,
)

meta_category_id = 64224

# 1. 메타 카테고리 → fee categoryId 변환
response1 = requests.get(
    f"https://wing.coupang.com/tenants/rfm/api/product/meta/category/{meta_category_id}",
    cookies=cookies,
    headers=headers,
    timeout=30,
)

meta_data = response1.json()

fee_category_id = meta_data[0]["categoryId"]
category_name = meta_data[0]["name"]

print("meta_category_id:", meta_category_id)
print("category_name:", category_name)
print("fee_category_id:", fee_category_id)

# 2. fee 조회
json_data = {
    "agreementScope": "PRODUCTION",
    "leafKanCategoryIds": [fee_category_id],
    "unit1Unit2CategoryNames": [],
}

response2 = requests.post(
    "https://wing.coupang.com/tenants/rfm/accounting-fee/lowasp/warehousing-fee",
    cookies=cookies,
    headers=headers,
    json=json_data,
    timeout=30,
)

fee_data = response2.json()

rows = []

for item in fee_data.get("feeRatesBySingleCategoryResponseV1", []):
    for fee_group in item.get("calculatedFeesAfterPromotion", {}).get("calculatedFees", []):
        capacity_type = fee_group.get("capacityType")

        for price_row in fee_group.get("feeByMinPrice", []):
            rows.append({
                "metaCategoryId": meta_category_id,
                "categoryName": category_name,
                "feeCategoryId": fee_category_id,
                "capacityType": capacity_type,
                "minPrice": price_row.get("minPrice", {}).get("amount"),
                "configuredAmount": price_row.get("configuredFee", {}).get("amount", {}).get("amount"),
                "finalAmount": price_row.get("configuredFee", {}).get("finalAmount", {}).get("amount"),
            })

for row in rows[:10]:
    print(row)

with open("coupang_fee_64224.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "metaCategoryId",
            "categoryName",
            "feeCategoryId",
            "capacityType",
            "minPrice",
            "configuredAmount",
            "finalAmount",
        ]
    )
    writer.writeheader()
    writer.writerows(rows)

print("저장 완료: coupang_fee_64224.csv")