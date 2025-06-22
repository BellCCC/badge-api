from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import requests

app = FastAPI()

class BadgeRequest(BaseModel):
    name: str
    employee_id: str
    photo_url: str

@app.post("/generate_badge")
async def generate_badge(data: BadgeRequest):
    # 创建空白工牌背景
    width, height = 400, 200
    badge = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(badge)

    # 加载字体（如果部署到云端无法用本地字体，可略过字体）
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except:
        font = ImageFont.load_default()

    # 写入姓名和工号
    draw.text((150, 30), f"Name: {data.name}", fill=(0, 0, 0), font=font)
    draw.text((150, 70), f"ID: {data.employee_id}", fill=(0, 0, 0), font=font)

    # 下载头像
    try:
        response = requests.get(data.photo_url)
        photo = Image.open(io.BytesIO(response.content)).resize((100, 100))
        badge.paste(photo, (30, 50))
    except Exception as e:
        print("Error downloading or pasting photo:", e)

    # 转为 base64
    buffered = io.BytesIO()
    badge.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {
        "status": "success",
        "image_base64": img_str
    }
