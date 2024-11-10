from data import rest

from httpx import AsyncClient
from pydantic import Field, BaseModel, PlainSerializer

from typing import Literal, Annotated, List
from datetime import datetime, timedelta


AssetClass = Literal["STK", "OPT", "FUT", "CFD", "WAR", "SWP", "FUND", "BOND"]
BarType = Literal["Last", "Bid", "Ask", "Midpoint", "FeeRate", "Inventory"]
OrderStatusFilter = Literal["Inactive", "PendingSubmit", "PreSubmitted", "Submitted", "Filled", "PendingCancel", "Cancelled", "WarnState", "SortByTime"]
CommaSeparatedString = Annotated[List[str], PlainSerializer(lambda x: ",".join(x), when_used="unless-none")]
Period = Annotated[timedelta, PlainSerializer(lambda x: f"{x.days}D", when_used="unless-none")]
Bar = Annotated[timedelta, PlainSerializer(lambda x: f"{x.seconds}S", when_used="unless-none")]
DateTime = Annotated[datetime, PlainSerializer(lambda x: x.strftime("%Y%m%d-%H:%M:%S"), when_used="unless-none")]


class Order(BaseModel):
    account_id: str = Field(..., serialization_alias="acctId")
    conid: str = Field(...)
    order_type: str = Field(..., serialization_alias="orderType")
    side: Literal["BUY", "SELL"] = Field(...)
    tif: Literal["DAY", "IOC", "GTC", "OPG", "PAX"] = Field(...)
    quantity: float = Field(...)
    conidex: str | None = Field(default=None, serialization_alias="conidex")
    sec_type: str | None = Field(default=None, serialization_alias="secType")
    c_oid: str | None = Field(default=None, serialization_alias="cOID")
    parent_id: str | None = Field(default=None, serialization_alias="parentId")
    is_single_group: bool | None = Field(default=None, serialization_alias="isSingleGroup")
    outside_rth: bool | None = Field(default=None, serialization_alias="outsideRTH")
    aux_price: float | None = Field(default=None, serialization_alias="auxPrice")
    ticker: str | None = Field(default=None, serialization_alias="ticker")
    trailing_amt: float | None = Field(default=None, serialization_alias="trailingAmt")
    trailing_type: str | None = Field(default=None, serialization_alias="trailingType")
    referrer: str | None = Field(default=None, serialization_alias="referrer")
    cash_qty: float | None = Field(default=None, serialization_alias="cashQty")
    use_adaptive: bool | None = Field(default=None, serialization_alias="useAdaptive")
    is_ccy_conv: bool | None = Field(default=None, serialization_alias="isCcyConv")
    price: float | None = Field(default=None, serialization_alias="price")
    strategy: str | None = Field(default=None)
    strategy_parameters: dict | None = Field(default=None, serialization_alias="strategyParameters")


@rest.endpoint.register(resource="accounts", schema={"account_id": (str, Field(...))})
async def account_summary(client: AsyncClient, request: BaseModel):
    return await client.get(f"/iserver/account/{request.account_id}/summary")


@rest.endpoint.register(resource="contracts", schema={"conid": (str, Field(...))})
async def contract_details(client: AsyncClient, request: BaseModel):
    return await client.get(f"/iserver/contract/{request.conid}/info")


@rest.endpoint.register(resource="currencies", schema={"currency": (str, Field(...))})
async def currency_exchange_rates(client: AsyncClient, request: BaseModel):
    return await client.get(
        "/iserver/currency/exchange_rates", 
        params={
            "source": "USD",
            "target": request.currency,
        }
    )


@rest.endpoint.register(resource="securities", schema={
    "conid": (str, Field(default=None)),
    "sectype": (str, Field(default=None)),
    "month": (str, Field(default=None)),
    "exchange": (str, Field(default=None)),
    "strike": (float, Field(default=None)),
    "right": (str, Field(default=None)),
})
async def security_info(client: AsyncClient, request: BaseModel):
    return await client.get(
        "/iserver/secdef/info",
        params=request.model_dump(),
    )


@rest.endpoint.register(resource="securities", schema={
    "symbol": (str, Field(...)),
    "sectype": (str, Field(default=None)),
    "name": (bool, Field(default=None)),
    "more": (bool, Field(default=None)),
    "fund": (bool, Field(default=None)),
    "fund_family_con_id_ex": (str, Field(default=None)),
    "pattern": (bool, Field(default=None)),
    "referrer": (str, Field(default=None)),
})
async def security_search(client: AsyncClient, request: BaseModel):
    return await client.get("/iserver/secdef/search", params=request.model_dump())


@rest.endpoint.register(resource="securities", schema={
    "conid": (str, Field(...)),
    "sectype": (str, Field(...)),
    "month": (str, Field(...)),
    "exchange": (str, Field(default="SMART")),
})
async def security_strikes(client: AsyncClient, request: BaseModel):
    return await client.get("/iserver/secdef/strikes", params=request.model_dump())


@rest.endpoint.register(resource="securities", schema={
    "asset_class": (AssetClass, Field(default="STK", serialization_alias="assetClass")),
    "exchange": (str, Field(default="SMART")),
})
async def all_contracts(client: AsyncClient, request: BaseModel):
    return await client.get("/trsrv/all-conids", params=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="securities", schema={
    "symbols": (CommaSeparatedString, Field(...)),
    "exchange": (str, Field(default="SMART")),
})
async def all_futures(client: AsyncClient, request: BaseModel):
    return await client.get("/trsrv/futures", params=request.model_dump())


@rest.endpoint.register(resource="securities", schema={
    "asset_class": (AssetClass, Field(default="STK", serialization_alias="assetClass")),
    "symbol": (str, Field(...)),
    "exchange_filter": (CommaSeparatedString, Field(default=None, serialization_alias="exchangeFilter")),
    "exchange": (str, Field(default="SMART")),
})
async def security_schedule(client: AsyncClient, request: BaseModel):
    return await client.get("/trsrv/secdef/schedule", params=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="securities", schema={
    "conids": (CommaSeparatedString, Field(...)),
    "criteria": (str, Field(default=None)),
    "bondp": (str, Field(default=None)),
})
async def security_definition(client: AsyncClient, request: BaseModel):
    return await client.get("/trsrv/secdef", params=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="securities", schema={
    "symbols": (CommaSeparatedString, Field(...)),
    "exchange": (str, Field(default="SMART")),
})
async def security_stocks(client: AsyncClient, request: BaseModel):
    return await client.get("/trsrv/stocks", params=request.model_dump())


@rest.endpoint.register(resource="securities", schema={
    "conid": (int, Field(...)),
    "bar_type": (BarType, Field(..., serialization_alias="barType")),
    "anchor_date": (DateTime, Field(..., serialization_alias="startTime")),
    "period": (Period, Field(...)),
    "bar": (Bar, Field(...)),
    "anchor_date_is_start": (
        Annotated[bool, PlainSerializer(lambda x: 1 if x else -1)], 
        Field(default=True, serialization_alias="direction")
    ),
    "outside_rth": (bool, Field(default=False, serialization_alias="outsideRTH")),
})
async def data_ohlc_hmds(client: AsyncClient, request: BaseModel):
    return await client.get("/hmds/history", params=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="securities", schema={
    "conid": (int, Field(...)),
    "period": (Period, Field(...)),
    "bar": (Bar, Field(...)),
    "start_time": (DateTime, Field(..., serialization_alias="startTime")),
    "exchange": (str, Field(default="SMART")),
    "outside_rth": (bool, Field(default=False, serialization_alias="outsideRTH")),
})
async def data_ohlc_iserver(client: AsyncClient, request: BaseModel):
    return await client.get("/iserver/marketdata/history", params=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="securities", schema={
    "conids": (CommaSeparatedString, Field(...)),
    "fields": (CommaSeparatedString, Field(...)),
})
async def data_snapshots(client: AsyncClient, request: BaseModel):
    return await client.get("/iserver/marketdata/snapshot", params=request.model_dump())


@rest.endpoint.register(resource="securities", schema={
    "conid": (int, Field(...)),
})
async def data_snapshots_unsubscribe(client: AsyncClient, request: BaseModel):
    return await client.post("/iserver/marketdata/unsubscribe", json=request.model_dump())


@rest.endpoint.register(resource="securities")
async def data_snapshots_unsubscribe_all(client: AsyncClient):
    return await client.get("/iserver/marketdata/unsubscribe/all")


@rest.endpoint.register(resource="orders", schema={
    "order_id": (int, Field(..., serialization_alias="orderId")),
})
async def order_status(client: AsyncClient, request: BaseModel):
    return await client.get(f"/iserver/account/order/status/{request.order_id}", params=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="orders")
async def all_orders(client: AsyncClient):
    return await client.get("/iserver/account/orders")


@rest.endpoint.register(resource="orders", schema={
    "order_id": (int, Field(..., serialization_alias="orderId")),
    "account_id": (str, Field(..., serialization_alias="acctId")),
    "order": (Order, Field(...)),
})
async def modify_order(client: AsyncClient, request: BaseModel):
    if request.order.account_id != request.account_id or request.order.order_id != request.order_id:
        raise ValueError("account_id and order_id must match")
    return await client.post(
        f"/iserver/account/{request.account_id}/order/{request.order_id}", 
        json=request.order.model_dump(by_alias=True)
    )


@rest.endpoint.register(resource="orders", schema={
    "order_id": (int, Field(..., serialization_alias="orderId")),
    "account_id": (str, Field(..., serialization_alias="acctId")),
})
async def cancel_order(client: AsyncClient, request: BaseModel):
    return await client.delete(f"/iserver/account/order/{request.order_id}")


@rest.endpoint.register(resource="orders", schema={
    "account_id": (str, Field(..., serialization_alias="acctId")),
    "order": (Order, Field(...))
})
async def place_order(client: AsyncClient, request: BaseModel):
    if request.order.account_id != request.account_id:
        raise ValueError("account_id and order_id must match")
    return await client.post(
        f"/iserver/account/{request.account_id}/orders", 
        json=request.order.model_dump(by_alias=True)
    )


@rest.endpoint.register(resource="orders", schema={
    "account_id": (str, Field(..., serialization_alias="acctId")),
    "order": (Order, Field(...))
})
async def simulate_order(client: AsyncClient, request: BaseModel):
    if request.order.account_id != request.account_id:
        raise ValueError("account_id and order_id must match")
    return await client.post(
        f"/iserver/account/{request.account_id}/orders/whatif", 
        json=request.order.model_dump(by_alias=True)
    )


@rest.endpoint.register(resource="orders", schema={
    "order_id": (int, Field(..., serialization_alias="orderId")),
    "req_id": (str, Field(..., serialization_alias="reqId")),
    "text": (str, Field(...)),
})
async def respond_to_order_prompt(client: AsyncClient, request: BaseModel):
    return await client.post("/iserver/notification", json=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="orders", schema={
    "message_ids": (CommaSeparatedString, Field(..., serialization_alias="messageIds")),
})
async def suppress_order_prompt(client: AsyncClient, request: BaseModel):
    return await client.post("/iserver/questions/suppress", json=request.model_dump(by_alias=True))


@rest.endpoint.register(resource="orders")
async def reset_suppressed_order_prompts(client: AsyncClient):
    return await client.post("/iserver/questions/suppress/reset")


@rest.endpoint.register(resource="orders", schema={
    "reply_id": (str, Field(..., serialization_alias="replyId")),
    "confirmed": (bool, Field(default=True)),
})
async def confirm_order_prompt(client: AsyncClient, request: BaseModel):
    return await client.post(f"/iserver/reply/{request.reply_id}", json=request.model_dump(by_alias=True))
