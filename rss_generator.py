from datetime import datetime

def generate_rss_feed(data: dict, output_path: str = "feed.xml"):
    now = datetime.utcnow()
    pub_date = now.strftime("%Y-%m-%d")
    last_build = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Daily Market Report</title>
    <link>https://falcoza.github.io/marketreporterhtml/Market_Report.html</link>
    <description>Automatically generated market reports and infographics, updated twice daily.</description>
    <language>en-za</language>
    <lastBuildDate>{last_build}</lastBuildDate>

    <item>
        <title>Market Report for {pub_date}</title>
        <link>https://falcoza.github.io/marketreporterhtml/Market_Report.html</link>
        <guid isPermaLink="true">https://falcoza.github.io/marketreporterhtml/Market_Report.html</guid>
        <pubDate>{last_build}</pubDate>
        <description><![CDATA[Click to view the full market infographic report.]]></description>
    </item>
</channel>
</rss>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rss)
