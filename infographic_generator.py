from config import THEME, REPORT_COLUMNS

def generate_html_infographic(data: dict) -> str:
    """Generate an HTML infographic instead of a PNG image"""
    
    css = f"""
    <style>
        body {{
            font-family: Georgia, serif;
            background-color: {THEME['background']};
            color: {THEME['text']};
            margin: 0;
            padding: 20px;
            width: 520px;
        }}
        .report-header {{
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 16px;
        }}
        th {{
            background-color: {THEME['header']};
            color: white;
            padding: 8px;
            text-align: center;
        }}
        td {{
            padding: 8px;
            text-align: center;
        }}
        .label-cell {{
            text-align: left;
        }}
        .row-even {{
            background-color: #F5F5F5;
        }}
        .positive {{
            color: {THEME['positive']};
        }}
        .negative {{
            color: {THEME['negative']};
        }}
        .footer {{
            font-size: 14px;
            color: #666666;
            text-align: right;
            margin-top: 20px;
        }}
    </style>
    """

    html = css + f"""
    <div class="report-header">Market Report {data['timestamp']}</div>
    <table>
        <thead>
            <tr>
    """

    # Add table headers
    for col_name, _ in REPORT_COLUMNS:
        html += f"<th>{col_name}</th>"
    html += "</tr></thead><tbody>"

    # Define the rows for each metric
    metrics = [
        ("JSE All Share", data["JSEALSHARE"]),
        ("USD/ZAR", data["USDZAR"]),
        ("EUR/ZAR", data["EURZAR"]),
        ("GBP/ZAR", data["GBPZAR"]),
        ("Brent Crude", data["BRENT"]),
        ("Gold", data["GOLD"]),
        ("S&P 500", data["SP500"]),
        ("Bitcoin ZAR", data["BITCOINZAR"])
    ]

    for idx, (label, values) in enumerate(metrics):
        row_class = "row-even" if idx % 2 == 0 else ""
        html += f'<tr class="{row_class}">'

        # First column: metric name
        html += f'<td class="label-cell">{label}</td>'

        # Second column: today's value
        today_val = values["Today"]
        today_text = f"{today_val:,.0f}" if today_val > 1000 else f"{today_val:,.2f}"
        html += f"<td>{today_text}</td>"

        # Other columns: Change, Monthly, YTD
        for period in ["Change", "Monthly", "YTD"]:
            val = values[period]
            style = "positive" if val >= 0 else "negative"
            html += f'<td class="{style}">{val:+.1f}%</td>'

        html += "</tr>"

    html += "</tbody></table>"
    html += '<div class="footer">Data: Yahoo Finance, CoinGecko</div>'

    return html
