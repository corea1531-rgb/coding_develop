import requests

cookies = {
    'PCID': '17688188793930533978558',
    'bm_ss': 'ab8e18ef4e',
    'OAuth_Token_Request_State': 'ef9f96fa-55ca-4ce4-bdea-0da8f64abe3c',
    'web-session-id': 'd12f2c67-a6c5-4c08-b3e3-3669f19e7901',
    'ak_bmsc': 'BBA8A205A76BAC893771473E7F69CDB0~000000000000000000000000000000~YAAQBKPBFxUmQf2cAQAAHJeoBR+TvlKpP3VhgI6NiBa4f8LixwYlNabBXS3ky4BRrFIVUp07ChtHMKnzj9dQm+Ci5mR9m+kvxd0hIik4287aSjwygfk+iMeQd6KKA6RIfQfHjVMYREqj2BUzWQvB+Oj+ebEIALLQwLM7tgrtrRV7zVdJjK08HOvxrvQQcviomNcEek0JBmhhvY1OEIsmhGe+BXP6Z/xnM0A4tTj4FVwGJ6jkO/YTJPY0HcMNNbKPE3elTDwIcSUiS8brIHFcJ3Rwf94QpJtq2UXMHHSzyrPUNoTLIhwLzrrOC165SQmMZB/UXPFmLIVA7Xz3+S6Mta13OayIQph3QPhAOPqW8koyYKChrYDI8AGEEeqGGIwct9iAQSMDOqOHWBIip+viRKPHQE9OGIwsvhvejVIoil8i3IxckeEDT0Rzrx1oK/rbQpLio4/4rfE28l/iI62t3ew=',
    'sc_vid': 'A00193388',
    'sc_lid': 'ckm00285',
    'sc_uid': 'x8dmRgcExm1MBVyrx6NlbpMIt1VPUdo4Xf44XIvlSV/Kyt7o52mE83905tbPFak=',
    'wing-market': 'KR',
    'wing-locale': 'ko',
    'sxSessionId': 'MWI5M2RjZWYtMDkzMy00YTgxLTgwOWEtNDdhZTY2OGMyNjlk',
    '_abck': 'CE1E22F8963A3209A45B400D51072544~0~YAAQd3kyF5+HReScAQAAaKCoBQ8NrN0eKb5NRvKcq0KtIaeY/ZwR6xWGUD+HyrVa5sc3KiDWTzaKI5GBGU4eDlojS/74/SRpJfVXHtNDXRInY4qmtFoB7ALfDoPN+NzfboIPUKKCrc7WbE9NdUCgF2dlL5wkinRG2kDvKJOSOrqcvvLwsrWGaxpre64vYrR1MBgFcRBfRNejbQjenWUZjbdKYswuJcCY/3KrAXl1qc9MDlFeilKGtTMk+fhPG7KLi4qDNJc6BUW9ITb9Q6xnQcVVqNGoX+8Pk6yW6OEAw08XGWBN6xW6wd0Xss8urHpHWZRwFmxVb9xFNTCeC1APGnuGXNfB9jUf52AxxVlZV6IUncBEQUbw2ao8luGyNStRmYBzbXW3aIZF2DEmH/r5e1oqjyWrNQSvINQbpD/pZrNRfT0e5hfnmvWbavW8gr8+h5fqGO1gizRhkwvTd//APo1fkZBM1V4iSkUPk2vr764txe10FKJSjUu7l+Z4nVLSb1TPwf4X/WGKBOxhqln92EolgwFf4tjjCbQJuuBRsZzFUPLrGGKFX03Nk5UGNymxjuh0QSR2RHM45eo2AXFCoMWUGsNb3naKkwSQ1yTj5e2mATqjj0VxtMm4Zo07~-1~-1~1773920028~AAQAAAAF%2f%2f%2f%2f%2f%2fn%2fqH8ZVzoxv+8HEhlPXql7+O2od6K1qCh9hHRKiNbFBh%2f10YBuNcF+sqoGDBZpXHiHoWn2wNJ3uhQagEp4Io2Mo1jh1M93UBEu~-1',
    'XSRF-TOKEN': '5be4597e-786e-49d5-a299-0ba379f662d8',
    'HOME_CARD_LIFE_NudgingSmsMfa': 'DISMISS',
    'AWSALBTG': 'nIUKxdvVpYlzH6B24oo5Ym99lAidHoY6JEfd7O9K5XvngVnDDDg8Dcwz2Wafw7EV9hHmXm3NbCs1Zm0+A6V7QEQSxunuVIcTGfls24AtIrfOdclhltQs0OPJp/R9L9B+Wf3BrCAMuWm1Cn/IyJXCJbkC7smLfjL9QqC+wY8J3kStcZVCtSY=',
    'AWSALBTGCORS': 'nIUKxdvVpYlzH6B24oo5Ym99lAidHoY6JEfd7O9K5XvngVnDDDg8Dcwz2Wafw7EV9hHmXm3NbCs1Zm0+A6V7QEQSxunuVIcTGfls24AtIrfOdclhltQs0OPJp/R9L9B+Wf3BrCAMuWm1Cn/IyJXCJbkC7smLfjL9QqC+wY8J3kStcZVCtSY=',
    'bigfoot_browser_session_id': '1dcae90e-18c2-4cc7-aded-16de499ce3f2',
    'CGSID_PARTNERADMINWEB': 'ea126f52e92941bfa1d041db888afe20',
    'fs_uid': '#o-24BWCV-na1#77613ef4-b161-4803-8576-2a50f91e8c67:48c1975a-8afd-49bb-95a9-7d250a67ab0b:1773916442359::1#8afb4a58#/1805288007',
    'fs_lua': '1.1773917642378',
    'bm_so': '2BC9036E71CCDA9D21D1412B2F1A25092C33D92ED69421F47D729013ADF54245~YAAQXXkyFwmJzumcAQAAqnG7BQf/Gf10JZhJellN10uV3C0On1IWdcleA8a0X3PFNBoKdE+uEJR6e+eBEAZnPWREQJHiwcnrskCo4MKB9OrlWg8bbyPF+IRyzlzIClBKVob8g0MTvhqRzTzGZy7oEwexbixBXFRiFji12NRz7XDYufwEfMnhIybYNKAXYXF4ebXXJmO+8SxeIOuoR16oJhCBAyufHD/YGrrb4jIKzZGu6IKnwoERtuTupXyZXcbxCqb9SA1BHoLjuCEmgPFnuPfqDkPdv7Xm2fbt5Gld6MHThgLwx146R3ssTHypxCkWi+Vc8/9FXNQ8LlRsXcKQqX4vLmBCsyRCvMcFyF5r2wf3HI533+FEpBE1/6ByapU9ZIcbNmlbmBRXTrv9A3+sF2iO+n5bppoPXlTphRghXYQDi1jvoXSSKdQDsxB1nlkgfpX2nphbePHEU8s5mTUlxrM=',
    'bm_sz': '514C439A779C48F2B849753A00AF8F64~YAAQXXkyFwuJzumcAQAAq3G7BR/qlSMHLgTgArzunze+43ebd7LKaQWqmoFTjOUVub7pQsXw7/Uf3P7WCR05/qrMamPuSEAK881fCi+kmQrwaBJbdy1gn7gzILxe+OQP4xM1DI3rFbuR6euvmqSwvJZySRC0U6pyp4z67lLpy+F0BBpDkaHDz5juL7KjlyHVkhU0M1qwrrGyFhpbN7rxPETX11TX2hjG+zTL80JVTy1WEHrfjR19/93g7AIIlZtoSX3r2NPIY6oOEV7blOP8VyLadyIvBQBND/Sf5/AZPgy7q5Pu5jwCPeJ2l5czL5yzes9iacGz4Kfd5rsribf53I3Z8VG7V0SaN/IvIW/OMqLJhRUaF5ZGiTu8YydBBRYVfE2XA++vLzRZzuDjbREw7/iKRlfIZh+eun0mrlr4TjSuMYPSPlVNAAW6//LZB4DItl5AAKfHG+yZ/2m4aaC0LBmeojBB3jhJI+8MYP5tFJ4b/Fe1rCzQ1SQ=~3621687~3490883',
    'bm_lso': '2BC9036E71CCDA9D21D1412B2F1A25092C33D92ED69421F47D729013ADF54245~YAAQXXkyFwmJzumcAQAAqnG7BQf/Gf10JZhJellN10uV3C0On1IWdcleA8a0X3PFNBoKdE+uEJR6e+eBEAZnPWREQJHiwcnrskCo4MKB9OrlWg8bbyPF+IRyzlzIClBKVob8g0MTvhqRzTzGZy7oEwexbixBXFRiFji12NRz7XDYufwEfMnhIybYNKAXYXF4ebXXJmO+8SxeIOuoR16oJhCBAyufHD/YGrrb4jIKzZGu6IKnwoERtuTupXyZXcbxCqb9SA1BHoLjuCEmgPFnuPfqDkPdv7Xm2fbt5Gld6MHThgLwx146R3ssTHypxCkWi+Vc8/9FXNQ8LlRsXcKQqX4vLmBCsyRCvMcFyF5r2wf3HI533+FEpBE1/6ByapU9ZIcbNmlbmBRXTrv9A3+sF2iO+n5bppoPXlTphRghXYQDi1jvoXSSKdQDsxB1nlkgfpX2nphbePHEU8s5mTUlxrM=~1773917664495',
    'JSESSIONID': 'A8D44F5D49455A6385495B6620DB0278',
    'bm_s': 'YAAQXXkyF6qNzumcAQAA83i7BQWC0H/uuilhBZJuEVZ9npY+DhNA3URvLVd//HRPeCSV1g9WOSt/9KcSV6YZmWYl3gf8RzgsUZXvAFjRKy89s14gER/H9GE6RirRKqj3rAcQrX3dTKJ99UBtBq8LX4MKl8O6WxQm/XIVrkSHxpJ2t4BBDpcTd/Lrgl72ekrU2wMKap1GCQypkB+z9B/cdhImuwC5GV4RlHpYOUWDInIFKgjPHeP+CaijbK82ufLjIHreGwFWzlvg2ARjl177CNUpxX/wAyzneMr//MiYNRGxXIQ4yAZQ6koT3SF0yl645FK5I3yDJiye/DKBi1BxOS6sxyQwPDyKFdLP/Dj9B1zi+H3yDe1vVyOREhP1I3v66En4q0AeQuF7yJcNoGq4bGWs8sjDouybXWUK1frdhPwC/kpeX6qvHjA19oaRJBd+MLxOKtlczso8/W4Mhp3qvZmek/QNHS8m7bui8v/Quq3rvM19Kb6fbsLjLVoapvaxNop1o/ebVOoM95BGb2eHvISVb0fk2j6AFFhePb66qUkBXWu3uXlD3RZ01PgBeyniDrptI5gAw8htYQDeDth8aqB1a5LkiPibMYn2aCVcWPYtAlYzp6uqrqIP6cJzh2brTivcKulMVqd0odhEc3tXN06jJDToPcGgynlpk+nYpzRgfgMeDyd7INWJFNfFTvc9tTCqeRk7vsovkINZANIHJwEkl4iSACqg3+EzW48TM2fF0Yp/BhgVlhm/dMZ61UwIIsDEj+tJofBASrdWilgw/GD5lIwM9WmEXPlSzFpSg/12p1+6sEOwGjtus/MN44cJES8scN1zDUA4uvC7TDmGDk9MjPTlLZDxFfc2d70HKqMONCDYmm/1us3kw9kTCF+62oHeV7nr+LHSvy1DVjA99ltiAZ7+j8UOymE6uOgPqTJiHO2j3PCSaG3PyjvNQQ3SDms7EINoPsrmrFn5Pd+LjvoCZrMq',
    'bm_sv': '4A0AB5D15ADFFC6B06B6CC3BAAFA34CC~YAAQXXkyFy2XzumcAQAAqoW7BR9oUhiEU0janOO62rVhE1V8NXGFJj0G9SxgC0J1BV+HUQyStzIqn0qOn2CLzkVO8Bc3okeXKXdG/UY2zcDqO5pnXuP4QWHQ2lz6MC+PmoHH0s72f2Q0eX1hXqRY7RVDETTlb7WY68Q0d9v5oquDf607Vu5GjYQSEEyzWcvxRROWCui/w9DMqeoFWQyCPCU581txXE+R8yOJrkYg6+h18v69sJcbJNzPaAxOAMVDIas=~1',

}

headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6,en;q=0.5,ja;q=0.4',
    'content-type': 'application/json',
    'origin': 'https://wing.coupang.com',
    'referer': 'https://wing.coupang.com/tenants/rfm-inventory/management/list',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

json_data = {
    'paginationRequest': {
        'pageSize': 10,
        'pageNumber': 0,
        'searchAfterSortValues': None,
    },
    'hiddenStatus': 'VISIBLE',
    'sort': [
        {
            'sortParameter': 'ORDERABLE_QUANTITY',
            'sortDirection': 'DESCENDING',
        },
    ],
}

response = requests.post(
    'https://wing.coupang.com/tenants/rfm-inventory/inventory-health-dashboard/excel-report',
    cookies=cookies,
    headers=headers,
    json=json_data,
    timeout=60,
)

print('status_code:', response.status_code)
print('content-type:', response.headers.get('Content-Type'))
print('content-disposition:', response.headers.get('Content-Disposition'))
print('size:', len(response.content))

if response.status_code == 200 and response.content:
    filename = 'inventory_health.xlsx'

    content_disposition = response.headers.get('Content-Disposition', '')
    if 'filename=' in content_disposition:
        filename = content_disposition.split('filename=', 1)[1].strip().strip('"').rstrip(';')

    with open(filename, 'wb') as f:
        f.write(response.content)

    print('저장 완료:', filename)
else:
    print('다운로드 실패')
    print(response.text[:1000])