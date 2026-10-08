# report/generate_report.py
import pandas as pd, pathlib, datetime

def make_html(csv_path):
    df = pd.read_csv(csv_path)

    # 오류가 있는 행을 빨간 배경으로 표시
    def style(row):
        return ['background:#ffdddd' if not row.ok else '' for _ in row]

    html_table = df.style.apply(style, axis=1).set_table_attributes('border="1"').render()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>외부링크 점검 보고서</title></head>
<body>
<h2>📊 외부링크 자동 점검 보고서 ({ts})</h2>
{html_table}
</body></html>"""

    out_path = pathlib.Path(csv_path).with_suffix(".html")
    out_path.write_text(html, encoding="utf-8")
    return out_path

if __name__ == "__main__":
    import sys
    make_html(sys.argv[1])
