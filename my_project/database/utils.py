from typing import Optional

from pydantic import AnyUrl
from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


class utcnow(expression.FunctionElement):
    type = TIMESTAMP()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class PostgresDsnAsyncPg(AnyUrl):
    allowed_schemes = {
        "postgresql",
        "postgresql+asyncpg",
    }

    @classmethod
    def validate_parts(cls, parts: dict[str, str]) -> dict[str, str]:
        parts = super().validate_parts(parts)
        if "+" not in parts["scheme"]:
            parts["scheme"] += "+asyncpg"
        return parts

    @classmethod
    def validate_host(
        cls, parts: dict[str, str]
    ) -> tuple[str, Optional[str], str, bool]:
        host, tld, host_type, rebuild = super().validate_host(parts)
        return host, tld, host_type, True
