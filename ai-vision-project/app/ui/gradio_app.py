import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/api/v1/recognize/image"

def predict(image):
    try:
        files = {"image": open(image, "rb")}
        response = requests.post(API_URL, files=files)

        data = response.json()

        # ===============================
        # ✅ SUCCESS CASE
        # ===============================
        if data.get("status") == "success":
            return f"""
✅ Item Detected Successfully!

 Product: {data['display_name']}
 Category: {data['category']}
 Price: {data['price']} {data['currency']}
 Confidence: {round(data['confidence'] * 100, 2)}%

"""

        # ===============================
        # ⚠️ NOT FOUND IN DB
        # ===============================
        elif data.get("status") == "not_found":
            return f"""
⚠️ Item recognized but not in catalog

 Detected: {data['display_name']}
 Category: {data['category']}
Confidence: {round(data['confidence'] * 100, 2)}%

❗ Price not available
"""

        # ===============================
        # ❌ ERROR CASE
        # ===============================
        else:
            return f"""
❌ Error: {data.get('error_code')}

📝 Message: {data.get('message')}
"""

    except Exception as e:
        return f"❌ UI Error: {str(e)}"


demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="AI Image Recognition"
)

demo.launch()