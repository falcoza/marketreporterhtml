from datetime import datetime

def generate_rss_feed(data: dict, output_path: str = "feed.xml"):
    timestamp = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    pub_date = datetime.now().strftime("%Y-%m-%d")

    html_summary = f"""<ul>
        <li>JSE All Share: {data["JSEALSHARE"]["Today"]}</li>
        <li>USD/ZAR: {data["USDZAR"]["Today"]}</li>
        <li>EUR/ZAR: {data["EURZAR"]["Today"]}</li>
        <li>GBP/ZAR: {data["GBPZAR"]["Today"]}</li>
        <li>Brent: {data["BRENT"]["Today"]}</li>
        <li>Gold: {data["GOLD"]["Today"]}</li>
        <li>S&P 500: {data["SP500"]["Today"]}</li>
        <li>Bitcoin ZAR: {data["BITCOINZAR"]["Today"]}</li>
    </ul>"""

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Daily Market Report (BM Feed)</title>
    <link>https://github.com/falcoza/marketreporterhtml/blob/main/Market_Report.html</link>
    <description>Automated market data summary for Business Maverick</description>
    <language>en-us</language>
    <lastBuildDate>{timestamp}</lastBuildDate>
    <item>
        <title>Market Report – {pub_date}</title>
        <link>https://github.com/falcoza/marketreporterhtml/blob/main/Market_Report.html</link>
        <pubDate>{timestamp}</pubDate>
        <guid>market-report-{pub_date}</guid>
        <description><![CDATA[
            {html_summary}
            <br><br>
            <a href="https://github.com/falcoza/marketreporterhtml/blob/main/Market_Report.html">View full report</a>
        ]]></description>
    </item>
</channel>
</rss>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rss)
