
from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import base64

app = FastAPI()

class BadgeRequest(BaseModel):
    name: str
    employee_id: str
    photo_url: str

@app.post("/generate_badge")
def generate_badge(data: BadgeRequest):
    # 1. 加载背景图（请替换为你自己的背景图路径）
    bg = Image.open("badge_template.jpg").convert("RGBA")

    # 2. 下载头像
    response = requests.get(data.photo_url)
    avatar = Image.open(io.BytesIO(response.content)).resize((160, 200))

    # 3. 合成图像
    bg.paste(avatar, (100, 100))  # 根据你的模板调整位置
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("arial.ttf", 30)
    draw.text((100, 320), f"姓名：{data.name}", font=font, fill="black")
    draw.text((100, 360), f"工号：{data.employee_id}", font=font, fill="black")

    # 4. 转为 base64 图像
    buffer = io.BytesIO()
    bg.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "status": "ok",
        "image_base64": f"data:image/png;base64,{base64_img}"
    }
