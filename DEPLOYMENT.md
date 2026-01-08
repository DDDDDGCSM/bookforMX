# BookForMX 部署指南

## 🚀 快速开始

### 本地开发

1. **安装依赖**
```bash
cd bookforMX
pip install -r requirements.txt
```

2. **启动服务**
```bash
python app.py
```

3. **访问应用**
- 主页（图书广场）: http://localhost:5000
- 交换墙: http://localhost:5000/exchange-wall
- 书籍详情: http://localhost:5000/book/1

## 📦 部署到 Vercel

### 方法一：通过 GitHub

1. **创建 GitHub 仓库**
```bash
git init
git add .
git commit -m "Initial commit: BookForMX"
git remote add origin https://github.com/YOUR_USERNAME/bookforMX.git
git push -u origin main
```

2. **在 Vercel 部署**
   - 访问 https://vercel.com
   - 使用 GitHub 登录
   - 点击 "New Project"
   - 导入 `bookforMX` 仓库
   - 保持默认设置，点击 "Deploy"

3. **完成！**
   - Vercel 会自动部署
   - 获得访问链接：`https://bookformx.vercel.app`

### 方法二：使用 Vercel CLI

```bash
npm i -g vercel
vercel login
cd bookforMX
vercel --prod
```

## 🎨 功能特性

### 已实现功能

✅ **图书广场（Plaza de Libros）**
- 杂志式布局，温暖的牛皮纸色背景
- 今日故事轮播
- 动态过滤器（带故事、认证用户等）
- 图书卡片展示（封面、放手理由、用户信息）

✅ **书籍详情页**
- 三个标签页：
  - El Libro（书籍信息、相册、旅程时间轴）
  - Su Historia（发起人故事）
  - Intercambios Pasados（往期交换记录）
- 侧边栏行动区（申请交换按钮）

✅ **申请交换流程**
- 多步骤模态框
- Paso 1: 讲述你的故事
- Paso 2: 选择你的书
- 表单验证

✅ **交换墙（El Mural del Trueque）**
- 瀑布流展示成功交换记录
- 双方书籍封面并排展示
- 交换感言和日期

✅ **墨西哥文化元素**
- 信任徽章本地化（🌵 仙人掌、🦉 猫头鹰、📖 阿兹特克纹样）
- 装饰性图标（仙人掌、咖啡杯、太阳）
- 西班牙语（墨西哥）文案

## 🔧 配置说明

### 环境变量（可选）

目前应用使用模拟数据，无需配置环境变量。

如需连接数据库，可添加：
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

### 自定义配置

在 `app.py` 中可以修改：
- 端口号（默认 5000）
- 模拟数据
- API 端点

## 📝 下一步开发

### 待实现功能

- [ ] 用户认证系统
- [ ] 数据库集成（PostgreSQL/MySQL）
- [ ] 用户个人资料页
- [ ] 我的书架功能
- [ ] 消息通知系统
- [ ] 搜索功能
- [ ] 图片上传功能
- [ ] 邮件通知

### 数据库模型建议

```python
# 用户表
users (id, name, email, avatar, trust_level, created_at)

# 图书表
books (id, title, author, isbn, publisher, condition, cover_image, user_id, created_at)

# 故事表
stories (id, book_id, user_id, content, created_at)

# 交换表
exchanges (id, book1_id, book2_id, user1_id, user2_id, status, created_at, completed_at)

# 交换历史表
exchange_history (id, book_id, from_user_id, to_user_id, date, city)
```

## 🐛 故障排查

### 问题：页面无法加载

**解决方案**：
1. 检查 Flask 服务是否运行
2. 查看终端错误信息
3. 确认端口 5000 未被占用

### 问题：样式未加载

**解决方案**：
1. 检查 `static/css/style.css` 文件是否存在
2. 清除浏览器缓存
3. 检查 Flask 静态文件路径配置

### 问题：模态框无法打开

**解决方案**：
1. 检查浏览器控制台是否有 JavaScript 错误
2. 确认 `static/js/book_detail.js` 已加载
3. 检查按钮的 `onclick` 事件

## 📚 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5, CSS3, JavaScript (Vanilla)
- **部署**: Vercel / Railway / Render
- **数据库**: PostgreSQL / MySQL (待集成)

## 🌟 特色设计

- **颜色系统**: 温暖的牛皮纸色调（#F5E6D3）
- **字体**: Segoe UI（系统字体，兼容性好）
- **响应式**: 支持移动端和桌面端
- **动画**: 平滑过渡和悬停效果
- **本地化**: 墨西哥文化元素和西班牙语文案

## 📞 支持

如有问题，请查看：
- README.md
- 代码注释
- Flask 官方文档：https://flask.palletsprojects.com/

---

**祝部署顺利！** 🎉

