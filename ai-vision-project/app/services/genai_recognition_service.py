# 🔹 Used to convert image bytes → base64 string (required for LLaVA input)
import base64

# 🔹 Used to extract JSON from LLM output (in case extra text is present)
import re
import json

# 🔹 LangChain wrapper for Ollama models (LLaVA in your case)
from langchain_ollama import ChatOllama

# 🔹 Prompt template system (to dynamically inject instructions)
from langchain_core.prompts import PromptTemplate

# 🔹 Forces LLM output to match a strict Pydantic schema
from langchain_core.output_parsers import PydanticOutputParser

# 🔹 Your AI response schema (defines expected JSON structure)
from app.schemas.ai_response import AIDetectionResponse

# 🔹 App configuration (model name, base URL, etc.)
from app.core.config import settings


# 🔹 Abstract base class (for future model switching)
class VisionModel:
    def recognize(self, image_bytes):
        raise NotImplementedError()


# 🔹 Ollama Vision Model implementation
class OllamaVisionModel(VisionModel):

    def __init__(self):
        # 🔹 Initialize LLM
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            temperature=0,
            timeout=30
        )

        # 🔹 Strict JSON parser using Pydantic
        self.parser = PydanticOutputParser(
            pydantic_object=AIDetectionResponse
        )

        # 🔹 Prompt with dynamic format instructions
        self.prompt = PromptTemplate.from_template("""
You are an AI vision model.

Analyze the image and return STRICT JSON only.
 DO NOT wrap it inside "properties".
 DO NOT wrap inside: "properties"
- "data"
- "result"

Return EXACTLY this structure:


{format_instructions}
""")

    # 🔹 Extract JSON from messy LLM output
    def clean_output(self, text):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return match.group() if match else text

    # 🔹 Main recognition function
    def recognize(self, image_bytes):

        # 🔹 Convert image → base64
        image_b64 = base64.b64encode(image_bytes).decode()

        # 🔹 Inject format instructions into prompt
        formatted_prompt = self.prompt.format(
            format_instructions=self.parser.get_format_instructions()
        )

        # 🔹 Call LLM with image + prompt
        response = self.llm.invoke([
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": formatted_prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{image_b64}"
                    }
                ]
            }
        ])

        # 🔹 Raw model output
        raw_output = response.content
        print("\n🔍 RAW OUTPUT:\n", raw_output)

        try:
            # 🔹 Clean JSON string
            cleaned = self.clean_output(raw_output)

            # 🔹 Convert to dict
            data = json.loads(cleaned)

            # 🔥 Handle "properties" wrapper (LLM mistake)
            if "properties" in data:
                data = data["properties"]

            # 🔹 Validate using Pydantic parser
            parsed = self.parser.parse(json.dumps(data))

            # 🔹 Return as Python dict (Pydantic v2)
            return parsed.model_dump()

        except Exception as e:
            print("❌ PARSE ERROR:", str(e))

            # 🔴 Safe fallback response
            return {
                "recognized": False,
                "item_name": None,
                "display_name": None,
                "category": None,
                "aliases": [],
                "confidence": 0.1,
                "needs_human_review": True,
                "message": "Invalid model output"
            }


# 🔹 Factory function (for future model switching)
def get_model():
    return OllamaVisionModel()