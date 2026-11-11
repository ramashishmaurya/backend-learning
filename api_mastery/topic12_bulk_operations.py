"""
================================================================================
TOPIC 12: BULK OPERATIONS (BATCH PROCESSING)
================================================================================
Run command:
    uvicorn api_mastery.topic12_bulk_operations:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
TWO WAYS TO DESIGN BULK APIS:
1. ATOMIC (All-or-Nothing):
   - Wrap all inserts in a single database transaction.
   - If row 99 fails, ROLLBACK the whole transaction and return 400 Bad Request.
   - Used in financial operations (e.g. batch payroll transfers).
2. BEST-EFFORT (Partial Success):
   - Insert all valid rows, collect errors for invalid rows.
   - Return HTTP 207 Multi-Status with a detailed summary.
   - Used in data imports (e.g. CSV contact import, product catalog sync).
================================================================================
"""

from typing import List, Dict
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Topic 12: Bulk Operations & Partial Success")

INVENTORY_DB: Dict[str, dict] = {
    "SKU-101": {"sku": "SKU-101", "name": "Standard USB Cable", "qty": 100}
}

class ProductBatchItem(BaseModel):
    sku: str = Field(..., min_length=3, description="Unique product SKU")
    name: str = Field(..., min_length=2)
    qty: int = Field(..., ge=1)

class BulkImportRequest(BaseModel):
    items: List[ProductBatchItem] = Field(..., min_length=1, max_length=100)

class BulkImportResponse(BaseModel):
    total_requested: int
    succeeded_count: int
    failed_count: int
    created: List[dict]
    errors: List[dict]

@app.post(
    "/inventory/bulk-import",
    response_model=BulkImportResponse,
    status_code=status.HTTP_207_MULTI_STATUS,  # 207 Multi-Status indicates mixed results!
    tags=["Bulk Operations"]
)
def bulk_import_inventory(payload: BulkImportRequest):
    """
    Best-Effort Partial Success:
    Valid SKUs are stored. Duplicate SKUs are flagged without failing the entire batch!
    """
    created_list = []
    error_list = []

    for idx, item in enumerate(payload.items):
        if item.sku in INVENTORY_DB:
            error_list.append({
                "row_index": idx,
                "sku": item.sku,
                "reason": f"SKU '{item.sku}' already exists in database"
            })
            continue

        # Save to DB
        new_record = {"sku": item.sku, "name": item.name, "qty": item.qty}
        INVENTORY_DB[item.sku] = new_record
        created_list.append(new_record)

    return BulkImportResponse(
        total_requested=len(payload.items),
        succeeded_count=len(created_list),
        failed_count=len(error_list),
        created=created_list,
        errors=error_list
    )
