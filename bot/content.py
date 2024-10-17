import re
from pathlib import Path
from typing import List, Tuple

import aiofiles


class ContentManager:
    BASE_DIR = Path(__file__).resolve().parent.parent / "tonutils"

    @classmethod
    async def read_file(cls, relative_path: str) -> str:
        """Asynchronously read the content of a file."""
        async with aiofiles.open(cls.BASE_DIR / relative_path, "r") as file:
            return await file.read()

    @classmethod
    async def _extract_section(cls, start_pattern: str, end_pattern: str) -> str:
        """Extract a section of content between start and end patterns."""
        content = await cls.read_file("README.md")
        section_match = re.search(fr'{start_pattern}\s*(.*?)\s*{end_pattern}', content, re.DOTALL)

        if section_match:
            return section_match.group(1).strip()

        raise RuntimeError("Section not found")

    @classmethod
    async def _extract_guide_section(cls) -> str:
        """Extract the Guide section from the README file."""
        return await cls._extract_section('### Guide', '## Contribution')

    @classmethod
    async def _parse_categories(cls, data: str) -> List[Tuple[str, str, str]]:
        """Parse categories and their items from the guide content."""
        category_pattern = re.compile(r"#### (.+)")
        subcategory_pattern = re.compile(r"- ##### (.+)")

        item_pattern = re.compile(r"- \[([^]]+)]\(([^)]+)\)")
        subcategory_item_pattern = re.compile(r" {2}- \[([^]]+)]\(([^)]+)\)")

        items = []
        current_category = ""
        current_subcategory = ""

        for line in data.split('\n'):
            if category_match := category_pattern.match(line):
                current_category = category_match.group(1).strip()
                current_subcategory = None

            elif subcategory_match := subcategory_pattern.match(line):
                current_subcategory = subcategory_match.group(1).strip()

            elif subcategory_item_match := subcategory_item_pattern.match(line):
                item_name, item_link = subcategory_item_match.groups()
                category_or_subcategory = f"{current_category} • {current_subcategory}" if current_subcategory else current_category
                items.append((category_or_subcategory, item_name, item_link))

            elif item_match := item_pattern.match(line):
                item_name, item_link = item_match.groups()
                category_or_subcategory = f"{current_category} • {current_subcategory}" if current_subcategory else current_category
                items.append((category_or_subcategory, item_name, item_link))

        return items

    @classmethod
    async def get_categories(cls) -> List[Tuple[str, str, str]]:
        """Extract and parse categories from the Guide section."""
        data = await cls._extract_guide_section()
        return await cls._parse_categories(data)

    @classmethod
    async def search_items(cls, query: str) -> List[Tuple[str, str, str]]:
        """Search for items in categories matching the query."""
        items = await cls.get_categories()

        return [
            (section, operation, link)
            for section, operation, link in items
            if query.lower() in operation.lower() or query.lower() in section.lower()
        ]
