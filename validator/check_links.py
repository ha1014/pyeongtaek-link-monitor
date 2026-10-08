# validator/check_links.py
import asyncio, httpx, yaml, pathlib, csv, datetime, json

async def check_one(client, url):
    try:
        resp = await client.head(url, follow_redirects=True, timeout=10)
        return {"url": url, "status": resp.status_code, "ok": resp.is_success}
    except Exception as e:
        return {"url": url, "status": "ERR", "ok": False, "msg": str(e)}

async def main():
    cfg = yaml.safe_load(open("config.yaml"))
    data_path = pathlib.Path("data/links.json")
    # jsonlines 파일을 읽고 중복 URL을 세트로 만든다
    urls = set()
    for line in data_path.read_text().splitlines():
        obj = json.loads(line)
        urls.add(obj["url"])

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[check_one(client, u) for u in urls])

    out_dir = pathlib.Path("reports")
    out_dir.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d")
    csv_path = out_dir / f"link_check_{ts}.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["url", "status", "ok", "msg"])
        w.writeheader()
        for r in results:
            w.writerow(r)

    return csv_path

if __name__ == "__main__":
    asyncio.run(main())
