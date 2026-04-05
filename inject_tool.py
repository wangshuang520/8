def inject_update_url_to_png(png_path, url, output_path):
    # PNG 文件的结束标记是 IEND (4字节) + CRC校验 (4字节)
    # 我们在这之后追加我们的隐藏数据
    with open(png_path, 'rb') as f:
        png_data = f.read()
    
    # 定义我们的隐藏数据标记 (随便写一个独特的标记，避免和正常PNG冲突)
    marker = b'__SMART_CHAT_UPDATE__'
    url_bytes = url.encode('utf-8')
    
    # 组合：原PNG数据 + 标记 + URL长度(4字节) + URL数据
    import struct
    url_len = struct.pack('>I', len(url_bytes)) # 大端序存长度
    
    new_data = png_data + marker + url_len + url_bytes
    
    with open(output_path, 'wb') as f:
        f.write(new_data)
    
    print(f"✅ 成功！生成的智能图片已保存为: {output_path}")

# --- 配置区域 ---
# 这里填你后面要用来放更新图片的 GitHub Pages 地址
# 注意：图片名统一叫 update_chat.png，这样你后面覆盖上传就行
YOUR_UPDATE_URL = "https://你的用户名.github.io/你的仓库名/update_chat.png"

# 执行注入
if __name__ == "__main__":
    # 把你最开始的原图放进来，命名为 original_chat.png
    inject_update_url_to_png("original_chat.png", YOUR_UPDATE_URL, "smart_chat.png")
