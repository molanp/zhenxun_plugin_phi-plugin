from typing import Dict, Any, List, Optional

from .embedlink import EmbedLinkThemeEnum, EmbedLinkPayload
from .node import NodeListItem, NodeDetail, NodeSearchInfo
from .space import SpaceListItem
from .record import RawRecord
from .view import MetaView
from .field import MetaField
from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    """
    Unified response body format returned by REST API
    """
    code: int
    success: bool
    message: str
    data: Optional[Any] = None


Records = List[RawRecord]


class RecordsData(BaseModel):
    records: Records


class GETResponseBase(BaseModel):
    total: int
    pageNum: int
    pageSize: int


class GETRecordResponseData(GETResponseBase, RecordsData):
    pass


class GETRecordResponse(ResponseBase):
    data: GETRecordResponseData


class PatchRecordResponse(ResponseBase):
    data: RecordsData


class PostRecordResponse(ResponseBase):
    data: RecordsData


class DeleteRecordResponse(ResponseBase):
    pass


class UploadFileResponse(ResponseBase):
    data: Dict[str, Any]


# meta field
class GETMetaFieldResponseData(BaseModel):
    items: List[MetaField] = Field(alias="fields")


class GETMetaFieldResponse(ResponseBase):
    data: GETMetaFieldResponseData


class PostMetaFieldResponseData(BaseModel):
    id: str
    name: str


class PostMetaFieldResponse(ResponseBase):
    data: PostMetaFieldResponseData


class DeleteFieldResponse(ResponseBase):
    pass


# meta view
class GETMetaViewResponseData(BaseModel):
    views: List[MetaView]


class GETMetaViewResponse(ResponseBase):
    data: GETMetaViewResponseData


# space
class GETSpaceListResponseData(BaseModel):
    spaces: List[SpaceListItem]


class GETSpaceListResponse(ResponseBase):
    data: GETSpaceListResponseData


# node
class GETNodeListResponseData(BaseModel):
    nodes: List[NodeListItem]


class GETNodeListResponse(ResponseBase):
    data: GETNodeListResponseData

class GETSearchNodeListResponseData(BaseModel):
    nodes: List[NodeSearchInfo]

class GETSearchNodeListResponse(ResponseBase):
    data: GETSearchNodeListResponseData


class GETNodeDetailResponse(ResponseBase):
    data: NodeDetail


class PostDatasheetMetaResponseData(BaseModel):
    id: str
    createdAt: int
    items: List[PostMetaFieldResponseData] = Field(alias="fields")


class PostDatasheetMetaResponse(ResponseBase):
    data: PostDatasheetMetaResponseData


class PostEmbedLinkResponseData(BaseModel):
    payload: Optional[EmbedLinkPayload] = None
    theme: Optional[EmbedLinkThemeEnum] = None
    linkId: str
    url: str


class PostEmbedLinkResponse(ResponseBase):
    data: PostEmbedLinkResponseData


GetEmbedLinkResponseData = PostEmbedLinkResponseData


class GetEmbedLinkResponse(ResponseBase):
    data: List[GetEmbedLinkResponseData]


class DeleteEmbedLinkResponse(ResponseBase):
    pass
