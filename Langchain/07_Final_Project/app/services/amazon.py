import re

import httpx
from bs4 import BeautifulSoup

from app.schemas import PriceFetchResult


ASIN_PATTERN = re.compile(r"/(?:dp|gp/product)/([A-Z0-9]{10})")


def extract_asin(url: str) -> str:
    match = ASIN_PATTERN.search(url)
    if not match:
        raise ValueError("Could not extract ASIN from Amazon URL.")
    return match.group(1)


def _parse_price(raw_text: str) -> float:
    cleaned = re.sub(r"[^0-9.]", "", raw_text.replace(",", ""))
    if not cleaned:
        raise ValueError("Price text not found.")
    return float(cleaned)


async def fetch_price_from_amazon(product_url: str) -> PriceFetchResult:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
        ),
        "Accept-Language": "en-IN,en;q=0.9",
    }
    async with httpx.AsyncClient(timeout=25, follow_redirects=True) as client:
        response = await client.get(product_url, headers=headers)
    response.raise_for_status()
    final_url = str(response.url)

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.select_one("#productTitle")
    price_tag = (
        soup.select_one("span.a-price span.a-offscreen")
        or soup.select_one("#priceblock_dealprice")
        or soup.select_one("#priceblock_ourprice")
    )
    if not title_tag or not price_tag:
        raise ValueError("Could not parse product title or price from Amazon page.")

    title = title_tag.get_text(strip=True)
    price = _parse_price(price_tag.get_text(strip=True))

    return PriceFetchResult(
        # Support short links (e.g., amzn.in) by extracting ASIN from final redirected URL.
        source_product_id=extract_asin(final_url),
        title=title,
        product_url=final_url,
        price=price,
        in_stock=True,
        currency="INR",
        confidence="high",
    )
