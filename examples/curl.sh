  #!/bin/bash

curl -s https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer e9acaba8-a79a-4504-9344-69c013d1bed3" \
  -d '{
    "model": "ep-20260104165752-j9wxl",
    "messages": [
      {
        "role": "system",
        "content": "你是一个桌面 GUI 自动化助手。你可以通过以下工具控制用户的电脑:\n\n1. screenshot(): 截取当前屏幕，返回截图图片\n\n2. click(x, y, click_type): 点击指定坐标\n   - x, y: 归一化坐标 (0-1000)，(0,0) 左上角，(1000,1000) 右下角，(500,500) 屏幕中心\n   - click_type: \"left\"(左键单击), \"right\"(右键单击), \"double\"(左键双击)\n\n3. type_text(text, x, y, press_enter): 输入文本（支持中文）\n   - text: 要输入的文本\n   - x, y: 可选，输入前先点击的坐标获取焦点\n   - press_enter: 可选，输入后是否按回车\n\n4. scroll(x, y, direction, amount): 滚动屏幕\n   - x, y: 滚动位置的归一化坐标\n   - direction: \"up\" 或 \"down\"\n   - amount: 滚动量，建议 3=小幅，5=中等，10=大幅\n\n工作流程:\n1. 先使用 screenshot 查看当前屏幕\n2. 分析截图，确定要操作的位置（转换为 0-1000 坐标）\n3. 使用 click/type_text/scroll 执行操作\n4. 每次操作后会自动返回新截图，确认结果\n5. 重复直到任务完成\n\n注意:\n- 坐标是归一化的 0-1000，不是像素值\n- 仔细观察截图中的元素位置再操作"
      },
      {
        "role": "user",
        "content": "请打开 chrome 浏览器，并通过 google 搜索一下今天的新闻"
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "screenshot",
          "description": "截取当前屏幕截图\n\nReturns:\n    ToolResponse: 包含截图的响应\n\nExample:\n    >>> result = screenshot()",
          "parameters": {
            "type": "object",
            "properties": {},
            "required": []
          }
        }
      },
      {
        "type": "function",
        "function": {
          "name": "click",
          "description": "在指定坐标执行鼠标点击操作\n\n坐标系统说明：\n- 使用 0-1000 归一化坐标，与实际屏幕分辨率无关\n- 原点 (0, 0) 在屏幕左上角\n- 右下角是 (1000, 1000)\n- 例如：屏幕中心坐标为 (500, 500)\n\nArgs:\n    x: X 坐标 (0-1000)，0 是最左边，1000 是最右边\n    y: Y 坐标 (0-1000)，0 是最上边，1000 是最下边\n    click_type: 点击类型 - left(左键单击), right(右键单击), double(左键双击)\n\nReturns:\n    ToolResponse: 包含操作结果和截图的响应\n\nExample:\n    >>> result = click(x=500, y=500)  # 点击屏幕中心\n    >>> result = click(x=100, y=200, click_type=\"double\")  # 双击",
          "parameters": {
            "type": "object",
            "properties": {
              "x": {
                "type": "integer",
                "description": "X 坐标 (0-1000)，0 是最左边，1000 是最右边"
              },
              "y": {
                "type": "integer",
                "description": "Y 坐标 (0-1000)，0 是最上边，1000 是最下边"
              },
              "click_type": {
                "type": "string",
                "description": "点击类型 - left(左键单击), right(右键单击), double(左键双击)",
                "enum": ["left", "right", "double"],
                "default": "left"
              }
            },
            "required": ["x", "y"]
          }
        }
      },
      {
        "type": "function",
        "function": {
          "name": "type_text",
          "description": "输入文本（支持中文）\n\n使用方式：\n1. 仅输入文本：type_text(text=\"hello\") - 在当前焦点位置输入\n2. 点击后输入：type_text(text=\"hello\", x=?, y=?) - 先点击坐标获取焦点，再输入\n3. 输入后回车：type_text(text=\"hello\", press_enter=True) - 输入后按回车键提交\n4. 完整流程：type_text(text=\"hello\", x=?, y=?, press_enter=True)\n\nArgs:\n    text: 要输入的文本\n    x: 可选，输入前先点击的 X 坐标 (0-1000)\n    y: 可选，输入前先点击的 Y 坐标 (0-1000)\n    press_enter: 可选，输入完成后是否按回车键\n\nReturns:\n    ToolResponse: 包含操作结果和截图的响应\n\nExample:\n    >>> result = type_text(text=\"Hello World\")\n    >>> result = type_text(text=\"搜索内容\", x=500, y=100, press_enter=True)",
          "parameters": {
            "type": "object",
            "properties": {
              "text": {
                "type": "string",
                "description": "要输入的文本"
              },
              "x": {
                "type": "integer",
                "description": "可选，输入前先点击的 X 坐标 (0-1000)"
              },
              "y": {
                "type": "integer",
                "description": "可选，输入前先点击的 Y 坐标 (0-1000)"
              },
              "press_enter": {
                "type": "boolean",
                "description": "可选，输入完成后是否按回车键",
                "default": false
              }
            },
            "required": ["text"]
          }
        }
      },
      {
        "type": "function",
        "function": {
          "name": "scroll",
          "description": "在指定位置滚动屏幕\n\n坐标系统：使用 0-1000 归一化坐标，(0,0) 为左上角，(1000,1000) 为右下角\n\n重要说明：\n- amount 是滚轮单位（wheel units），不是像素或屏幕百分比\n- 建议值：amount=3 小幅滚动，amount=5 中等滚动，amount=10 大幅滚动\n- 如果滚动不够或过多，请查看截图后再次调用调整\n\nArgs:\n    x: 归一化 X 坐标 (0-1000)，指定滚动时鼠标所在位置\n    y: 归一化 Y 坐标 (0-1000)，指定滚动时鼠标所在位置\n    direction: 滚动方向 \"up\" 或 \"down\"\n    amount: 滚轮单位数量，默认为 3\n\nReturns:\n    ToolResponse: 包含操作结果和截图的响应\n\nExample:\n    >>> result = scroll(x=500, y=500, direction=\"down\", amount=5)",
          "parameters": {
            "type": "object",
            "properties": {
              "x": {
                "type": "integer",
                "description": "归一化 X 坐标 (0-1000)，指定滚动时鼠标所在位置"
              },
              "y": {
                "type": "integer",
                "description": "归一化 Y 坐标 (0-1000)，指定滚动时鼠标所在位置"
              },
              "direction": {
                "type": "string",
                "description": "滚动方向 \"up\" 或 \"down\"",
                "enum": ["up", "down"]
              },
              "amount": {
                "type": "integer",
                "description": "滚轮单位数量，默认为 3",
                "default": 3
              }
            },
            "required": ["x", "y", "direction"]
          }
        }
      }
    ],
    "tool_choice": "auto"
  }' | python -m json.tool
