import re

html_regex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

async def sanitize_html(raw_html: str) -> str:
  return re.sub(html_regex, '', raw_html)
  