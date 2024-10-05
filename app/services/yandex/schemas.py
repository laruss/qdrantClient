from typing import Literal

from pydantic import BaseModel


class BlockName(BaseModel):
    block: str
    mods: dict


class BlockParams(BaseModel):
    url: str
    originalImageUrl: str
    cbirId: str
    bundles: list


class Block(BaseModel):
    name: BlockName
    params: BlockParams
    html: str


class MetaBundles(BaseModel):
    lb: str


class MetaAssets(BaseModel):
    las: str


class MetaExtraContent(BaseModel):
    names: list


class MetaBundlesMetadata(BaseModel):
    lb: str


class MetaAssetsMetadata(BaseModel):
    las: str


class Metadata(BaseModel):
    bundles: MetaBundles
    assets: MetaAssets
    extraContent: MetaExtraContent
    bundlesMetadata: MetaBundlesMetadata
    assetsMetadata: MetaAssetsMetadata


class UploadContent(BaseModel):
    cnt: Literal["pageview_candidate"]
    blocks: list[Block]
    metadata: Metadata
    assets: dict


class SerpItemResize(BaseModel):
    w: int
    h: int


class SerpItemOrigin(SerpItemResize):
    url: str | None = None


class SerpItemImage(SerpItemResize):
    url: str
    fileSizeInBytes: int | None = None
    ext: str | None = None
    origin: SerpItemOrigin | None = None
    resize: SerpItemResize | None = None
    title: str | None = None
    domain: str | None = None
    siteHref: str | None = None


class Size(BaseModel):
    width: int
    height: int


class SerpItemThumb(BaseModel):
    url: str
    size: Size | None = None
    w: int | None = None
    h: int | None = None


class SerpItemSnippet(BaseModel):
    title: str
    hasTitle: bool | None = None
    text: str | None = None
    url: str | None = None
    domain: str | None = None
    shopScore: int | None = None


class SerpItem(BaseModel):
    reqid: str
    freshness: str
    preview: list[SerpItemImage]
    dups: list[SerpItemImage] | None = None
    thumb: SerpItemThumb
    snippet: SerpItemSnippet
    detail_url: str | None = None
    img_href: str | None = None
    useProxy: bool | None = None
    pos: int | None = None
    id: str | None = None
    documentid: str | None = None
    rimId: str | None = None
    img_url: str | None = None
    counterPath: str | None = None
    counterPostfix: str | None = None
    sizes: dict | None = None
