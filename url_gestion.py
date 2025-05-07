from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class BestBuyPaginationURLGenerator:
    def __init__(self, base_url):
        self.base_url = base_url
        self.query_params = self._extract_query_params()

    def _extract_query_params(self):
        parsed = urlparse(self.base_url)
        query = parse_qs(parsed.query)

        # Flatten the query parameters
        flat_query = {key: val[0] for key, val in query.items()}

        # Attempt to extract category ID from path if missing
        if "id" not in flat_query:
            path_parts = parsed.path.strip("/").split("/")
            for part in path_parts:
                if part.startswith("pcmcat") and part.endswith(".c"):
                    flat_query["id"] = part.split(".")[0]

        return flat_query

    def generate_paginated_urls(self, start=1, end=10):
        paginated_urls = []

        for page in range(start, end + 1):
            params = self.query_params.copy()
            params.update({
                "_dyncharset": "UTF-8",
                "browsedCategory": self.query_params["id"],
                "cp": str(page),
                "iht": "n",
                "ks": "960",
                "list": "y",
                "sc": "Global",
                "st": f"{self.query_params['id']}_categoryid$cat00000",
                "type": "page",
                "usc": "All Categories"
            })

            url = urlunparse((
                "https",
                "www.bestbuy.com",
                "/site/searchpage.jsp",
                "",
                urlencode(params),
                ""
            ))

            paginated_urls.append(url)

        return paginated_urls


