# 🔹 Import required FastAPI components
from fastapi import APIRouter, UploadFile, File, HTTPException

# 🔹 Import AI model factory (can switch to Gemini later)
from app.services.genai_recognition_service import get_model

# 🔹 Import DB lookup service (UPDATED to support brand)
from app.services.product_lookup_service import find_product

# 🔹 Import Pydantic schemas for validation
from app.schemas.ai_response import AIDetectionResponse, RecognitionAPIResponse

# 🔹 Create router
router = APIRouter()


# 🔹 Main API endpoint for image recognition
@router.post("/recognize/image", response_model=RecognitionAPIResponse)
async def recognize_image(image: UploadFile = File(...)):

    try:
        # ==============================
        # ✅ 1. Validate file type
        # ==============================
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

        if image.content_type not in allowed_types:
            filename = (image.filename or "").lower()

            if not filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
                raise HTTPException(
                    status_code=400,
                    detail="INVALID_IMAGE_FORMAT"
                )

        # ==============================
        # ✅ 2. Read image bytes
        # ==============================
        image_bytes = await image.read()

        # ==============================
        # ✅ 3. Validate file size
        # ==============================
        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="FILE_TOO_LARGE")

        # ==============================
        # ✅ 4. Call AI model
        # ==============================
        model = get_model()
        raw_result = model.recognize(image_bytes)

        # ==============================
        # ✅ 5. Validate AI JSON
        # ==============================
        try:
            ai_result = AIDetectionResponse(**raw_result)
        except:
            raise HTTPException(status_code=502, detail="INVALID_MODEL_RESPONSE")

        # ==============================
        # ❌ 6. Not recognized
        # ==============================
        if not ai_result.recognized:
            return RecognitionAPIResponse(
                      status="error",
                      recognized=False,
                      item_name=None,
                      display_name=None,
                      category=None,
                      price=None,
                      currency=None,
                      confidence=ai_result.confidence,
                      source="image_upload",
                     error_code="ITEM_NOT_RECOGNIZED",
                     message=ai_result.message
                 )

        # ==============================
        # ✅ 7. Normalize AI output
        # ==============================
        raw_name = (ai_result.item_name or "").lower().strip()

        if not raw_name:
            raise HTTPException(status_code=422, detail="INVALID_ITEM_NAME")

        # ==============================
        # ✅ 8. Brand Detection
        # ==============================
        words = raw_name.split()

        brand = None
        for word in words:
            if word in ["acer", "dell", "hp", "logitech", "samsung", "sony", "boat"]:
                brand = word
                break

        # ==============================
        # ✅ 9. Smart Search Logic
        # ==============================
        search_candidates = []

        # Full name
        search_candidates.append(raw_name)

        # Split words
        search_candidates.extend(words)

        # Aliases from AI
        search_candidates.extend(ai_result.aliases)

        product = None

        for name in search_candidates:
            name = name.lower().strip()

            if not name:
                continue

            product = find_product(name, brand)

            if product:
                break

        # ==============================
        # ✅ 10. Found in DB
        # ==============================
        if product:
            return RecognitionAPIResponse(
                status="success",
                recognized=True,
                item_name=product.item_name,
                display_name=product.display_name,
                category=product.category,
                price=product.price,
                currency=product.currency,
                confidence=ai_result.confidence,
                source="image_upload",
                error_code=None,
                message="Item identified and price retrieved successfully"
            )

        # ==============================
        # ⚠️ 11. Not found in DB
        # ==============================
        return RecognitionAPIResponse(
            status="not_found",
            recognized=True,
            item_name=raw_name,
            display_name=ai_result.display_name,
            category=ai_result.category,
            price=None,
            currency=None,
            confidence=ai_result.confidence,
            source="image_upload",
            error_code=None,
            message="Item identified, but pricing is not available in the catalog"
        )

    # ==============================
    # 🔹 Handle known errors
    # ==============================
    except HTTPException as e:
        raise e

    # ==============================
    # 🔴 Catch unexpected errors
    # ==============================
    except Exception:
        raise HTTPException(status_code=500, detail="INTERNAL_SERVER_ERROR")