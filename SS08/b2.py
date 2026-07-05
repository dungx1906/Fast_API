from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date
import re

app = FastAPI(title="IT Asset Management API")

assets = [
    {
        "id": 1,
        "serial_number": "SN-MAC-01",
        "model": "MacBook Pro M3",
        "stock_available": 5,
        "status": "READY"
    },
    {
        "id": 2,
        "serial_number": "SN-DELL-02",
        "model": "Dell UltraSharp 27",
        "stock_available": 10,
        "status": "READY"
    },
    {
        "id": 3,
        "serial_number": "SN-THINK-03",
        "model": "ThinkPad X1 Carbon",
        "stock_available": 0,
        "status": "REPAIRING"
    }
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'


class AssetCreate(BaseModel):
    serial_number: str
    model: str = Field(min_length=2, max_length=255)
    stock_available: int = Field(ge=0)
    status: Literal["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]


class AllocationCreate(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(gt=0)
    start_date: date
    duration_months: int = Field(ge=1, le=12)


def find_asset(asset_id: int):
    for asset in assets:
        if asset["id"] == asset_id:
            return asset
    return None


@app.post("/assets", status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetCreate):

    for item in assets:
        if item["serial_number"].lower() == asset.serial_number.lower():
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    new_asset = asset.model_dump()
    new_asset["id"] = max([a["id"] for a in assets], default=0) + 1

    assets.append(new_asset)

    return {
        "message": "Asset created successfully",
        "data": new_asset
    }


@app.get("/assets")
def get_assets(
        keyword: Optional[str] = Query(None),
        status: Optional[str] = Query(None),
        min_stock: Optional[int] = Query(None)
):

    results = assets

    if keyword:
        keyword = keyword.lower()
        results = [
            asset for asset in results
            if keyword in asset["serial_number"].lower()
            or keyword in asset["model"].lower()
        ]

    if status:
        results = [
            asset for asset in results
            if asset["status"] == status
        ]

    if min_stock is not None:
        results = [
            asset for asset in results
            if asset["stock_available"] >= min_stock
        ]

    return results


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):

    asset = find_asset(asset_id)

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset: AssetCreate):

    old_asset = find_asset(asset_id)

    if old_asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    for item in assets:
        if (
            item["id"] != asset_id
            and item["serial_number"].lower() == asset.serial_number.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    old_asset.update(asset.model_dump())

    return {
        "message": "Asset updated successfully",
        "data": old_asset
    }


@app.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id: int):

    asset = find_asset(asset_id)

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    assets.remove(asset)


@app.post("/allocations", status_code=status.HTTP_201_CREATED)
def create_allocation(allocation: AllocationCreate):

    asset = find_asset(allocation.asset_id)

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if asset["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail="Asset is not ready"
        )

    if allocation.allocated_quantity > asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    if not re.fullmatch(EMAIL_REGEX, allocation.employee_email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    new_allocation = allocation.model_dump()
    new_allocation["id"] = max([a["id"] for a in allocations], default=0) + 1
    new_allocation["start_date"] = str(new_allocation["start_date"])

    allocations.append(new_allocation)

    asset["stock_available"] -= allocation.allocated_quantity

    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    return {
        "message": "Allocation created successfully",
        "data": new_allocation
    }


@app.get("/allocations")
def get_allocations():
    return allocations