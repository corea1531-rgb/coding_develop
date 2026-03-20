import requests
import time
import csv
from collections import deque

URL = "https://datalab.naver.com/shoppingInsight/getCategory.naver"

# 쿠키는 외부 공유 금지
COOKIE = '''NAC=8gkXB8Q9El5V; NNB=5NU446E72STWS; ASID=afcc7c730000019cd15ade5600000027; _fbp=fb.1.1773108452631.288499144967574389; nstore_session=QgicHyjCt4O5MIjZLuWeEbeN; CBI_SES=3cqZbFb1aJy+TJEcsivoADSvdGzb+CmqHlW3MVp/FXEqIrO2umjr2dV2BEfRmkHrgrTH9z6quRES7ieIsNwqi2ohlhDBWJp0rAHuNqAL7oGs0S8bjUGNxVcszE6KCeAKUjiLqQVDNYLLkn8D5YaHqm6Pmig2B/V2tgacktRcwhv3E3wFbLhjon+HFlxSle4ot6jU3VcguFRN8x2tZKUIUcd7FVoj7+LpM/1uuNh61b9KEApWNPgSvmDSxnTU7sWdJ0D+QW3SnOZK8ZqeQbqepcsS56ZHik6CTWqV9V3DbBjMqPgWypIouifA/eiogWizOMpP/Cib1DzkmiGAmZz1wS6vjRQ5YBDKx+KIPEicH6Q4qeD/xq0SYpnLMIsvVduoN/MAxLc0qziAnY0rt9AXq8UqBqk5rNIK2p7A5DEpnGOUWJNrXCZF2wiPLegHLxQTlYB8BaXjSpknPbZd6kzX4Q==; cto_bundle=-QPZuF9tcmp3WnNCVzFaT056YXE0NnNBYTNoT21WUm8lMkYxVFpxdVhmVTNGZ3oySGw5dFZsNSUyRlpOcFpnRHVuYzBUZVYlMkJtZFRoZU9YSDdwbThpRDQ3eVdFdVBKRjJGT0FabXZQdk5JdVVRc1dGUDJUYnBpTm9RWXgwa3U4aUJPUmNHOXZiTG9maXFsRkJ5VWolMkZuR1BaaUZoWnNyUSUzRCUzRA; nid_inf=1119575111; NID_AUT=TqPR4+k5iiVuuPEkVdjctbZSjhaoQrWC1df94j8r9BsaKMSa6gveunRhsZ8L6uFE; NAVER_ADS_AVAILABLE_USER=true; nstore_pagesession=jkWjYwqQ6LISBdsM+QG-199681; 066c80626d06ffa5b32035f35cabe88d=^%^D9^%^F8d^%^B6^%^2A^%^B4^%^5C^%^B1^%^8B^%^A7^%^FD^%^13GV^%^0F^%^B6T^%^A5^%^F3^%^D7^%^D3^%^9B^%^15^%^05^%^CB^%^83^%^B4^%^22^%^8F^%^B8^%^9B^%^BC^%^A2^%^C4^%^A2^%^8CI^%^40rvE^%^D0^%^D5d^%^83^%^EC^%^9B^%^CDp^%^ABU^%^9E^%^25g^%^9AQ^%^16^%^FC^%^16D2E^%^BC^%^C7v^%^9C^%^8Ev^%^60^%^AD^%^01^%^CD^%^91^%^92^%^AC^%^14^%^F0^%^A7M^%^0C^%^A6^%^82^%^1B^%^ED^%^9D^%^5B6^%^FF^%^DC^%^D5OJt^%^07^%^E9^%^07^%^11TJ^%^0Dk^%^DA^%^27^%^CFz^%^22^%^C1-^%^AB0^%^5C^%^92^%^15^%^9B^%^CC^%^12^%^01^%^84P^%^28^%^03^%^F4^%^05^%^17i^%^A2^%^88LX^%^C6^%^2C^%^00J^%^24^%^FA^%^B8P^%^FC^%^03^%^88^%^FD^%^EB^%^CFj^%^BCI^%^8A^%^9C^%^DE^%^0B2^%^C2; 1a5b69166387515780349607c54875af=q^%^F6UA^%^F0^%^EAXJ; NACT=1; SRT30=1773892203; page_uid=jkWyksqX5mk2SiEAaHV-338440; CBI_CHK=^\^"r5V0mf9uRUZHZ/vmLGy3ez7f4/k4aqWXL5o03eN68fo+VSYh3iSGCDqsVmm+f2X6Rr0x7hb2HTTPr4C7jvXL1YX6mZpn1K1NuXCZWMESDsIjR/Lua3mh1WHawVl0RDHb+6dE0zKXgis3ZXufWctGNwP8KK1WoKeHFZUuAHfYSV8=^\^"; NID_SES=AAABxNYBvsPIg5FSE7Ai/F0PcyzVOfOHqpRwRD28CH7ogyKx7yTwb0qgPvx/9xbl1YHnKILPY0gQiXl84XeVbX9Quxh6J05I77w77BEe9Kx3/0+xTz8Sf3NyE0DlH4PcjTIqs5zZbnlbdyXWHehVimOpC08lOkiymtGGQIf1ZgQJxWNKOPLx7A3zTSxPjlwvxBSxrx+z+0a+6jG9bjlgcLU55WGi7BsyN/cbANVAIRI0Kxi4j4DI5d6OqPQfEjNAfNMZYUGj7YVIblVamZExHF20yDw1HMv4uSZ02m8nmW0/cuHAHkvTXMcK4St7eUdEIUU8YyfNv3tUWzrVvMr3cSR9BACoe7m2hBkzrjs3cwDzZEC+z9O1uPx5ugG7E6wLMxYfxzSKm2CkfoqwJ0DlY4gJ+QloYdDuYcrWSLDg5rqIQ6RexOp5bw6/IlSW5lFX/4DbOGQf7cY4Nv6qfud+OicEHI8hv66SxisR2T5ElnGlIm80b7IHwY0G2xF8JSewm3H/C8M5CSUt7/8fC5rpaixR4curNLlm0C7yshMyFsx0CM3mcUl5skBgkKyeLxQhsH3xNsbGZ9fNWNXP63Avw5mOZodzI2/dyhWKeyhHbmm0S3XO; _datalab_cid=50000008; BUC=evzPCei82G4UHikNfpf4SaqKcL8QutzCoQeg7fovvCQ=^'''

HEADERS = {
    "accept": "*/*",
    "referer": "https://datalab.naver.com/shoppingInsight/sCategory.naver",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "cookie": COOKIE,
}


def get_children(cid: str, session: requests.Session) -> list:
    params = {"cid": cid}
    res = session.get(URL, headers=HEADERS, params=params, timeout=20)
    res.raise_for_status()
    data = res.json()

    # 핵심: childList를 반환
    if isinstance(data, dict) and "childList" in data:
        return data["childList"]

    print(f"[경고] 예상과 다른 응답 구조 (cid={cid})")
    print(str(data)[:1000])
    return []


def split_path(parent_path: str, name: str):
    """
    parentPath + 현재 name 으로 전체 경로 생성
    """
    if parent_path and parent_path != "전체":
        full_path = f"{parent_path} > {name}"
    else:
        full_path = name

    parts = full_path.split(" > ")
    while len(parts) < 4:
        parts.append("")

    return full_path, parts[:4]


def main():
    session = requests.Session()

    rows = []
    visited = set()

    # 시작점: cid=0
    queue = deque(["0"])

    while queue:
        cid = queue.popleft()

        if cid in visited:
            continue
        visited.add(cid)

        try:
            children = get_children(cid, session)
        except Exception as e:
            print(f"[에러] cid={cid} 조회 실패: {e}")
            time.sleep(1)
            continue

        print(f"cid={cid} -> 하위 {len(children)}개")

        for child in children:
            child_cid = str(child.get("cid", "")).strip()
            pid = str(child.get("pid", "")).strip()
            name = str(child.get("name", "")).strip()
            parent_path = str(child.get("parentPath", "")).strip()
            level = child.get("level", "")

            # childList의 각 항목에는 leaf가 안 보일 수 있으므로
            # level 4를 일단 말단으로 간주하고,
            # 더 안전하게는 나중에 실제 하위 조회 결과 0개인지로도 판별 가능
            full_path, parts = split_path(parent_path, name)

            row = {
                "cid": child_cid,
                "pid": pid,
                "name": name,
                "level": level,
                "category1": parts[0],
                "category2": parts[1],
                "category3": parts[2],
                "category4": parts[3],
                "full_path": full_path,
            }
            rows.append(row)

            # 계속 하위 탐색
            if child_cid:
                queue.append(child_cid)

        time.sleep(0.2)

    # 말단 판별: 내 cid를 pid로 갖는 자식이 없는 경우
    parent_ids = {row["pid"] for row in rows if row["pid"]}
    for row in rows:
        row["leaf"] = row["cid"] not in parent_ids

    total_count = len(rows)
    leaf_count = sum(1 for row in rows if row["leaf"])
    non_leaf_count = total_count - leaf_count

    print("\n===== 수집 완료 =====")
    print(f"전체 노드 수: {total_count}")
    print(f"말단(leaf) 수: {leaf_count}")
    print(f"중간 노드 수: {non_leaf_count}")

    output_file = "naver_shopping_categories.csv"
    fieldnames = [
        "cid", "pid", "name", "level",
        "category1", "category2", "category3", "category4",
        "full_path", "leaf"
    ]

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV 저장 완료: {output_file}")


if __name__ == "__main__":
    main()