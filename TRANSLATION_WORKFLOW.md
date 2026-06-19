# Europe-Train 多语言页面发布流程

## 目的
防止多语言页面发布时出现翻译缺失、链接错误、语言标识错误等问题。

## 发布前检查清单

### 1. 内容翻译检查
- [ ] 所有 UI 元素已翻译（导航、按钮、标题）
- [ ] 所有正文内容已翻译
- [ ] 所有 alt 文本已翻译
- [ ] 所有 meta 信息已翻译（title, description, og:title, og:description）

### 2. 技术检查
- [ ] HTML lang 属性正确（en, de, fr, es, ja, ko, pt, zh）
- [ ] hreflang 链接完整（所有语言版本互相关联）
- [ ] 导航链接指向正确语言路径（/fr/, /de/ 等）
- [ ] 语言切换器 active 状态正确
- [ ] 图片路径正确（相对路径或绝对路径）
- [ ] CSS/JS 路径正确

### 3. 本地化信息
- [ ] 货币信息本地化
- [ ] 价格示例本地化
- [ ] 官方预订链接本地化
- [ ] 支付方式本地化
- [ ] 客服信息本地化

### 4. 翻译脚本使用

#### 方式一：使用现有翻译脚本
```bash
# 翻译文章
python3 translate_articles.py

# 翻译 tickets 页面
python3 translate_tickets.py

# 翻译首页
python3 translate_homepage.py
```

#### 方式二：手动翻译流程
1. 复制英文版本作为模板
2. 替换所有文本内容
3. 更新 lang 属性
4. 更新 hreflang 链接
5. 更新导航链接
6. 更新本地化信息
7. 验证所有链接可用

### 5. 发布流程

```bash
# 1. 本地验证
python3 validate_translations.py  # 检查翻译完整性

# 2. 提交代码
git add -A
git commit -m "feat: 添加 XXX 页面多语言版本"

# 3. 推送（如有权限）
git push origin main

# 4. 验证线上
# 访问各语言版本确认正常
```

## 常见问题

### Q: 翻译脚本没有覆盖新页面？
A: 需要更新翻译字典，添加新页面的翻译键值对。

### Q: 某些语言显示乱码？
A: 检查 HTML 文件是否保存为 UTF-8 编码，检查是否有 BOM 头。

### Q: 链接跳转错误？
A: 检查相对路径是否正确，多语言页面需要使用 `/{lang}/` 前缀。

## 责任
- 发布者负责验证所有语言版本
- 翻译问题由发布者修复
- 技术问题由开发团队支持
