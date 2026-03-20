import requests

url = 'https://wing.coupang.com/tenants/seller-web/excel/request/download/file'


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
    'JSESSIONID': '7E8981642034C2436DB3611DC54A944F',
    'fs_uid': '#o-24BWCV-na1#77613ef4-b161-4803-8576-2a50f91e8c67:48c1975a-8afd-49bb-95a9-7d250a67ab0b:1773916442359::1#8afb4a58#/1805288007',
    'bm_sz': '514C439A779C48F2B849753A00AF8F64~YAAQZHkyF9c/kPecAQAAl3iqBR9YZsQd3mLHkOUkjFYc6gkDPW+DdVxMmbXsEUounkVG9DFZlgR2G7/3HBz7VL2n+HVaigFhVQq2jagw/oE9mnZmzQ3YEcCZeruPUVDG1pRXLiFa+qPhdwqtEmVhoW175R5HBaN3pLSzE6PGIi16gStySm6c+qKj3x1FL+3wNRHdvH2Q4MfkJU3Y01BuDBOkihUTyxMc+/YZ6gIbAjYFsHt8pafxsnl/UGzFqvnKVQM5TMlhnbaJ9anEJxTgEY0sQEEdkQvMUEQhYXt/mwoPivctInDsG9rg+NLZa/WLzOYOx2BhHKr+HDmAhLE94pgRCP5zscuyqQZxrCowvNNs40vYRqIyQmnY3TNdhqo1DTvNx29XfE1J0jyLVuiztQLOr81qK7i56GlpKZ0jypplgVSgBtmVx+PgPiAn0SlmtrxsLkgZR1gDgTY3FCivlCH4310=~3621687~3490883',
    'fs_lua': '1.1773916700121',
    'bm_s': 'YAAQd3kyFyy3SOScAQAA25uuBQWkAjOczaRt3GHzvFx71jWKyd1Etc2ICHmsiXMlu4kjStc+7EdEAvmzF/BIiRBMuk+BzcMvuUpLhWmp4ayf9oZfnV0v/jZ/fEK50EiccIMuIglAN6XGHtOLrX4P+EV+OvHs0LUeOvORncjMaErjHFLpKoZK2J5xhVyJ9bLvlutRBJALLKfxBdJ9qg6WJB/+T1CTi3/7w0jY9AJA5zbC/esFSzZ/G3XPaqwKh9L5/6zOZdt1FytPuCZKWB7tfLT1+bQ/FoJTwvoSx3sUJcN+j+NxqMB+jZ4TjPCltpJE72knpQgPvu1SFkhHp+C2X/iQD5oD6+S0PJq9kLkozNWzU1zjIacYWrPX5h7RIRexLWGYMbXnAH41V5RnewXOOkOvDJ/lNdWZfflFRAohKZeIdxBPESzdVXFvPD8CFlErzyg3ZVPLOUvvgJw8ppGO/8uK04hGqiG9LNUzmpzY3jvBxGjc2YdAg9swIEdJndZXBnKg1kAuT9cQyXkyb8sgC+gSvdLEc8PoPSqg1Zznhll48JE4scL87hl1envy1pLJxiMxBKe/k/i1ETgt7wAusCIoccAC1025EGvKZPig7lNAsP6IXgbViC8p29YfAal1u7c3y+Wf4sHUJ1GJ0hZg/WYdZjFn2VHvOElrTdwMnCTRnlqZoECEKX0vhqrUYG89pVVQ8oWwuaTzIA/Er/+itqdGuToDtR4pPK+GOYJO0eCh0dus3ZkMss7FtLpsvd78bkcS/l1iqbzwjc1YCC/eQDZkA49WTEfrXy0ezmU/rGy+vNRUsWnKGdzB5i2Ubnz5aq5Z+HHPG+h6d6mNAyqcW6eIqt/HkqXYwCqnFh378QZYZi29ekXJ195sGN6JfSMiP/s1sPJ127m5JpszdxRoFzk5++a4aabsMH/595sMpW6rJT/7/dtKhLUD0xE/ujxDVzyoSiGqNTDIYJCjYms7Lo1/IdAZ',
    'bm_so': 'D3A5711B79EF5D09700EB131122AE5B24C52651F2D87336E572216F0A73D41DF~YAAQd3kyFy23SOScAQAA25uuBQcaOOoC+5Mb//aEaAwyhc3F+RZdlGLtssvd0OSnlODf6cdDMxmgS1hyP9ieOW5dJh5sdDb9q7/ZP+QrHCOYTGa/d5gcckP+pWLmMPBySSBdOrcDT6/n5/gvRXH6+4xUeyf/Vkm90Hc7KUY/VVKb9IIon1DODywm03+vY5mkZJoat3To303Faf4h0rNotQ3GRlvwPOu9D7fcD4JD/F6CrwHe9AU3ku4kTPZfjbLuyUOkx4LGEPIiN31LVT7+aG3cOyIVOVt95mMmgv0/RovtiWgDmnvUivfKgWDinCxIdZaMdFXtnZLdzk++gkeaYg5ksrbeZQ99/r9Iu3j301tbO9Si65Dpsd4OMjvUK8hOE+lr3THcm5t9acYCr1Eeq9k+iDkG+Lh717dZMvaB618Zf1zIQHcegiWLrkLAEvMfvezcm+g8tkdqshv0KuRfNac=',
    'bm_sv': '4A0AB5D15ADFFC6B06B6CC3BAAFA34CC~YAAQd3kyF5+3SOScAQAAqpyuBR9W3Ca7kKbxHAdiSg6+329UxlB6ZHesYniblVQOUyg/nhXPFFImEVwvBy51u4DjlBwIORbn2So9PD3C4N1x71lFMZcYkWNP9KIhfL0YdP6lelxoG9NaPc/oJtwUm3WBY3pjLoHEYIxrtQWMk1aEguM42wmubWJW5euZOA4uvnSarZDWqN3FIAY+mMDddnt4/ygtm7JCRmKqYKNroEF5WdEmdgQlTxI9f6h9Y4j66eA=~1',
    'bm_lso': 'D3A5711B79EF5D09700EB131122AE5B24C52651F2D87336E572216F0A73D41DF~YAAQd3kyFy23SOScAQAA25uuBQcaOOoC+5Mb//aEaAwyhc3F+RZdlGLtssvd0OSnlODf6cdDMxmgS1hyP9ieOW5dJh5sdDb9q7/ZP+QrHCOYTGa/d5gcckP+pWLmMPBySSBdOrcDT6/n5/gvRXH6+4xUeyf/Vkm90Hc7KUY/VVKb9IIon1DODywm03+vY5mkZJoat3To303Faf4h0rNotQ3GRlvwPOu9D7fcD4JD/F6CrwHe9AU3ku4kTPZfjbLuyUOkx4LGEPIiN31LVT7+aG3cOyIVOVt95mMmgv0/RovtiWgDmnvUivfKgWDinCxIdZaMdFXtnZLdzk++gkeaYg5ksrbeZQ99/r9Iu3j301tbO9Si65Dpsd4OMjvUK8hOE+lr3THcm5t9acYCr1Eeq9k+iDkG+Lh717dZMvaB618Zf1zIQHcegiWLrkLAEvMfvezcm+g8tkdqshv0KuRfNac=~1773916823017',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ko-KR,ko;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6,en;q=0.5,ja;q=0.4',
    'referer': 'https://wing.coupang.com/vendor-inventory/list?searchKeywordType=ALL&searchKeywords=&salesMethod=ROCKET_GROWTH&productStatus=ON_SALE&stockSearchType=ALL&shippingFeeSearchType=ALL&displayCategoryCodes=&listingStartTime=null&listingEndTime=null&saleEndDateSearchType=ALL&bundledShippingSearchType=ALL&upBundling=ALL&displayDeletedProduct=false&shippingMethod=ALL&exposureStatus=ALL&locale=ko_KR&sortMethod=SORT_BY_ITEM_LEVEL_UNIT_SOLD&countPerPage=50&page=1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': 'PCID=17688188793930533978558; bm_ss=ab8e18ef4e; OAuth_Token_Request_State=ef9f96fa-55ca-4ce4-bdea-0da8f64abe3c; web-session-id=d12f2c67-a6c5-4c08-b3e3-3669f19e7901; ak_bmsc=BBA8A205A76BAC893771473E7F69CDB0~000000000000000000000000000000~YAAQBKPBFxUmQf2cAQAAHJeoBR+TvlKpP3VhgI6NiBa4f8LixwYlNabBXS3ky4BRrFIVUp07ChtHMKnzj9dQm+Ci5mR9m+kvxd0hIik4287aSjwygfk+iMeQd6KKA6RIfQfHjVMYREqj2BUzWQvB+Oj+ebEIALLQwLM7tgrtrRV7zVdJjK08HOvxrvQQcviomNcEek0JBmhhvY1OEIsmhGe+BXP6Z/xnM0A4tTj4FVwGJ6jkO/YTJPY0HcMNNbKPE3elTDwIcSUiS8brIHFcJ3Rwf94QpJtq2UXMHHSzyrPUNoTLIhwLzrrOC165SQmMZB/UXPFmLIVA7Xz3+S6Mta13OayIQph3QPhAOPqW8koyYKChrYDI8AGEEeqGGIwct9iAQSMDOqOHWBIip+viRKPHQE9OGIwsvhvejVIoil8i3IxckeEDT0Rzrx1oK/rbQpLio4/4rfE28l/iI62t3ew=; sc_vid=A00193388; sc_lid=ckm00285; sc_uid=x8dmRgcExm1MBVyrx6NlbpMIt1VPUdo4Xf44XIvlSV/Kyt7o52mE83905tbPFak=; wing-market=KR; wing-locale=ko; sxSessionId=MWI5M2RjZWYtMDkzMy00YTgxLTgwOWEtNDdhZTY2OGMyNjlk; _abck=CE1E22F8963A3209A45B400D51072544~0~YAAQd3kyF5+HReScAQAAaKCoBQ8NrN0eKb5NRvKcq0KtIaeY/ZwR6xWGUD+HyrVa5sc3KiDWTzaKI5GBGU4eDlojS/74/SRpJfVXHtNDXRInY4qmtFoB7ALfDoPN+NzfboIPUKKCrc7WbE9NdUCgF2dlL5wkinRG2kDvKJOSOrqcvvLwsrWGaxpre64vYrR1MBgFcRBfRNejbQjenWUZjbdKYswuJcCY/3KrAXl1qc9MDlFeilKGtTMk+fhPG7KLi4qDNJc6BUW9ITb9Q6xnQcVVqNGoX+8Pk6yW6OEAw08XGWBN6xW6wd0Xss8urHpHWZRwFmxVb9xFNTCeC1APGnuGXNfB9jUf52AxxVlZV6IUncBEQUbw2ao8luGyNStRmYBzbXW3aIZF2DEmH/r5e1oqjyWrNQSvINQbpD/pZrNRfT0e5hfnmvWbavW8gr8+h5fqGO1gizRhkwvTd//APo1fkZBM1V4iSkUPk2vr764txe10FKJSjUu7l+Z4nVLSb1TPwf4X/WGKBOxhqln92EolgwFf4tjjCbQJuuBRsZzFUPLrGGKFX03Nk5UGNymxjuh0QSR2RHM45eo2AXFCoMWUGsNb3naKkwSQ1yTj5e2mATqjj0VxtMm4Zo07~-1~-1~1773920028~AAQAAAAF%2f%2f%2f%2f%2f%2fn%2fqH8ZVzoxv+8HEhlPXql7+O2od6K1qCh9hHRKiNbFBh%2f10YBuNcF+sqoGDBZpXHiHoWn2wNJ3uhQagEp4Io2Mo1jh1M93UBEu~-1; XSRF-TOKEN=5be4597e-786e-49d5-a299-0ba379f662d8; HOME_CARD_LIFE_NudgingSmsMfa=DISMISS; AWSALBTG=nIUKxdvVpYlzH6B24oo5Ym99lAidHoY6JEfd7O9K5XvngVnDDDg8Dcwz2Wafw7EV9hHmXm3NbCs1Zm0+A6V7QEQSxunuVIcTGfls24AtIrfOdclhltQs0OPJp/R9L9B+Wf3BrCAMuWm1Cn/IyJXCJbkC7smLfjL9QqC+wY8J3kStcZVCtSY=; AWSALBTGCORS=nIUKxdvVpYlzH6B24oo5Ym99lAidHoY6JEfd7O9K5XvngVnDDDg8Dcwz2Wafw7EV9hHmXm3NbCs1Zm0+A6V7QEQSxunuVIcTGfls24AtIrfOdclhltQs0OPJp/R9L9B+Wf3BrCAMuWm1Cn/IyJXCJbkC7smLfjL9QqC+wY8J3kStcZVCtSY=; bigfoot_browser_session_id=1dcae90e-18c2-4cc7-aded-16de499ce3f2; CGSID_PARTNERADMINWEB=ea126f52e92941bfa1d041db888afe20; JSESSIONID=7E8981642034C2436DB3611DC54A944F; fs_uid=#o-24BWCV-na1#77613ef4-b161-4803-8576-2a50f91e8c67:48c1975a-8afd-49bb-95a9-7d250a67ab0b:1773916442359::1#8afb4a58#/1805288007; bm_sz=514C439A779C48F2B849753A00AF8F64~YAAQZHkyF9c/kPecAQAAl3iqBR9YZsQd3mLHkOUkjFYc6gkDPW+DdVxMmbXsEUounkVG9DFZlgR2G7/3HBz7VL2n+HVaigFhVQq2jagw/oE9mnZmzQ3YEcCZeruPUVDG1pRXLiFa+qPhdwqtEmVhoW175R5HBaN3pLSzE6PGIi16gStySm6c+qKj3x1FL+3wNRHdvH2Q4MfkJU3Y01BuDBOkihUTyxMc+/YZ6gIbAjYFsHt8pafxsnl/UGzFqvnKVQM5TMlhnbaJ9anEJxTgEY0sQEEdkQvMUEQhYXt/mwoPivctInDsG9rg+NLZa/WLzOYOx2BhHKr+HDmAhLE94pgRCP5zscuyqQZxrCowvNNs40vYRqIyQmnY3TNdhqo1DTvNx29XfE1J0jyLVuiztQLOr81qK7i56GlpKZ0jypplgVSgBtmVx+PgPiAn0SlmtrxsLkgZR1gDgTY3FCivlCH4310=~3621687~3490883; fs_lua=1.1773916700121; bm_s=YAAQd3kyFyy3SOScAQAA25uuBQWkAjOczaRt3GHzvFx71jWKyd1Etc2ICHmsiXMlu4kjStc+7EdEAvmzF/BIiRBMuk+BzcMvuUpLhWmp4ayf9oZfnV0v/jZ/fEK50EiccIMuIglAN6XGHtOLrX4P+EV+OvHs0LUeOvORncjMaErjHFLpKoZK2J5xhVyJ9bLvlutRBJALLKfxBdJ9qg6WJB/+T1CTi3/7w0jY9AJA5zbC/esFSzZ/G3XPaqwKh9L5/6zOZdt1FytPuCZKWB7tfLT1+bQ/FoJTwvoSx3sUJcN+j+NxqMB+jZ4TjPCltpJE72knpQgPvu1SFkhHp+C2X/iQD5oD6+S0PJq9kLkozNWzU1zjIacYWrPX5h7RIRexLWGYMbXnAH41V5RnewXOOkOvDJ/lNdWZfflFRAohKZeIdxBPESzdVXFvPD8CFlErzyg3ZVPLOUvvgJw8ppGO/8uK04hGqiG9LNUzmpzY3jvBxGjc2YdAg9swIEdJndZXBnKg1kAuT9cQyXkyb8sgC+gSvdLEc8PoPSqg1Zznhll48JE4scL87hl1envy1pLJxiMxBKe/k/i1ETgt7wAusCIoccAC1025EGvKZPig7lNAsP6IXgbViC8p29YfAal1u7c3y+Wf4sHUJ1GJ0hZg/WYdZjFn2VHvOElrTdwMnCTRnlqZoECEKX0vhqrUYG89pVVQ8oWwuaTzIA/Er/+itqdGuToDtR4pPK+GOYJO0eCh0dus3ZkMss7FtLpsvd78bkcS/l1iqbzwjc1YCC/eQDZkA49WTEfrXy0ezmU/rGy+vNRUsWnKGdzB5i2Ubnz5aq5Z+HHPG+h6d6mNAyqcW6eIqt/HkqXYwCqnFh378QZYZi29ekXJ195sGN6JfSMiP/s1sPJ127m5JpszdxRoFzk5++a4aabsMH/595sMpW6rJT/7/dtKhLUD0xE/ujxDVzyoSiGqNTDIYJCjYms7Lo1/IdAZ; bm_so=D3A5711B79EF5D09700EB131122AE5B24C52651F2D87336E572216F0A73D41DF~YAAQd3kyFy23SOScAQAA25uuBQcaOOoC+5Mb//aEaAwyhc3F+RZdlGLtssvd0OSnlODf6cdDMxmgS1hyP9ieOW5dJh5sdDb9q7/ZP+QrHCOYTGa/d5gcckP+pWLmMPBySSBdOrcDT6/n5/gvRXH6+4xUeyf/Vkm90Hc7KUY/VVKb9IIon1DODywm03+vY5mkZJoat3To303Faf4h0rNotQ3GRlvwPOu9D7fcD4JD/F6CrwHe9AU3ku4kTPZfjbLuyUOkx4LGEPIiN31LVT7+aG3cOyIVOVt95mMmgv0/RovtiWgDmnvUivfKgWDinCxIdZaMdFXtnZLdzk++gkeaYg5ksrbeZQ99/r9Iu3j301tbO9Si65Dpsd4OMjvUK8hOE+lr3THcm5t9acYCr1Eeq9k+iDkG+Lh717dZMvaB618Zf1zIQHcegiWLrkLAEvMfvezcm+g8tkdqshv0KuRfNac=; bm_sv=4A0AB5D15ADFFC6B06B6CC3BAAFA34CC~YAAQd3kyF5+3SOScAQAAqpyuBR9W3Ca7kKbxHAdiSg6+329UxlB6ZHesYniblVQOUyg/nhXPFFImEVwvBy51u4DjlBwIORbn2So9PD3C4N1x71lFMZcYkWNP9KIhfL0YdP6lelxoG9NaPc/oJtwUm3WBY3pjLoHEYIxrtQWMk1aEguM42wmubWJW5euZOA4uvnSarZDWqN3FIAY+mMDddnt4/ygtm7JCRmKqYKNroEF5WdEmdgQlTxI9f6h9Y4j66eA=~1; bm_lso=D3A5711B79EF5D09700EB131122AE5B24C52651F2D87336E572216F0A73D41DF~YAAQd3kyFy23SOScAQAA25uuBQcaOOoC+5Mb//aEaAwyhc3F+RZdlGLtssvd0OSnlODf6cdDMxmgS1hyP9ieOW5dJh5sdDb9q7/ZP+QrHCOYTGa/d5gcckP+pWLmMPBySSBdOrcDT6/n5/gvRXH6+4xUeyf/Vkm90Hc7KUY/VVKb9IIon1DODywm03+vY5mkZJoat3To303Faf4h0rNotQ3GRlvwPOu9D7fcD4JD/F6CrwHe9AU3ku4kTPZfjbLuyUOkx4LGEPIiN31LVT7+aG3cOyIVOVt95mMmgv0/RovtiWgDmnvUivfKgWDinCxIdZaMdFXtnZLdzk++gkeaYg5ksrbeZQ99/r9Iu3j301tbO9Si65Dpsd4OMjvUK8hOE+lr3THcm5t9acYCr1Eeq9k+iDkG+Lh717dZMvaB618Zf1zIQHcegiWLrkLAEvMfvezcm+g8tkdqshv0KuRfNac=~1773916823017',
}

params = {
    'requestType': 'VENDOR_INVENTORY_ITEM',
    'sellerRequestDownloadExcelId': '4659256',
}
response = requests.get(
    url,
    params=params,
    cookies=cookies,
    headers=headers,
    timeout=60,
)

print(response.status_code)
print(response.url)
print(response.headers.get('Content-Disposition'))
print(len(response.content))

if response.status_code == 200 and response.content:
    filename = 'download.xlsx'

    content_disposition = response.headers.get('Content-Disposition', '')
    if 'filename=' in content_disposition:
        filename = content_disposition.split('filename=', 1)[1].strip().strip('"')

    with open(filename, 'wb') as f:
        f.write(response.content)

    print('저장 완료:', filename)
else:
    print('다운로드 실패')
    print(response.text[:500])