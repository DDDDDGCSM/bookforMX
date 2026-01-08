# BookForMX - 墨西哥图书交换平台

一个以故事为核心的图书交换社区平台，专为墨西哥市场设计。

## 🌐 在线访问

部署到 Vercel 后，访问链接将自动生成：
- **主站点**: `https://your-project.vercel.app`

## 📊 功能特性

- ✅ **单页面设计** - 所有功能在一个页面完成
- ✅ **图书浏览** - 左右箭头切换，查看20本精选图书
- ✅ **快速换书** - 上传图片+填写故事，一键申请交换
- ✅ **WhatsApp 联系** - 提交后直接联系交换人
- ✅ **历史记录** - 左右滑动查看成功交换记录
- ✅ **分享功能** - 一键分享到社交平台
- ✅ **移动适配** - 完美支持手机端

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

访问：http://localhost:5000

### 部署到 Vercel

详细步骤请查看：`DEPLOY_VERCEL.md`

**快速部署**：
1. 推送代码到 GitHub
2. 在 Vercel 导入项目
3. 自动部署完成

## 📱 功能说明

### 主要功能

1. **浏览图书**
   - 使用 ◀ ▶ 箭头切换20本图书
   - 每本书都有真实的"放手理由"故事
   - 显示用户信息和信任徽章

2. **申请交换**
   - 点击底部"Solicitar Intercambio"按钮
   - 上传你的图书照片
   - 填写为什么想要这本书（至少20字）
   - 提交后显示 WhatsApp 联系方式

3. **WhatsApp 联系**
   - 提交交换申请后，显示交换人 WhatsApp
   - 点击图标直接跳转到 WhatsApp
   - 号码：+971 50 921 6685

4. **历史记录**
   - 页面底部展示成功交换记录
   - 左右滑动查看
   - 日期显示为最近一个月

5. **分享功能**
   - 右上角分享按钮
   - 分享内容包含书名、作者、故事、链接
   - 支持原生分享（移动端）

## 🎨 设计特色

- 温暖的牛皮纸色背景（#F5E6D3）
- 墨西哥文化元素（仙人掌、猫头鹰等）
- 响应式设计，完美适配手机
- 流畅的交互动画

## 📁 项目结构

```
bookforMX/
├── app.py                 # Flask 后端应用
├── requirements.txt       # Python 依赖
├── vercel.json           # Vercel 部署配置
├── templates/
│   └── index.html        # 主页面（单页面应用）
├── static/               # 静态资源（可选）
└── README.md            # 项目说明
```

## 🔧 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5, CSS3, JavaScript (Vanilla)
- **部署**: Vercel
- **数据库**: 模拟数据（可扩展）

## 📝 待扩展功能

- [ ] 数据库集成（PostgreSQL/MySQL）
- [ ] 用户认证系统
- [ ] 图片上传到云存储
- [ ] 消息通知系统
- [ ] 搜索功能

## 🌍 本地化

- **语言**: 西班牙语（墨西哥）
- **文化元素**: 仙人掌🌵、猫头鹰🦉、阿兹特克纹样📖
- **信任徽章**: Lector Novato、Compañero Confiable、Bibliófilo Truequero

## 📞 支持

如有问题，请查看：
- `DEPLOY_VERCEL.md` - 部署指南
- `测试指南.md` - 功能测试说明
- `功能完成清单.md` - 功能列表

---

**BookForMX - Intercambia libros, comparte historias** 📚
