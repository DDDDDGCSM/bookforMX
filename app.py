#!/usr/bin/env python3
"""
BookForMX - 墨西哥图书交换平台
Flask 后端应用
"""

from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from collections import defaultdict
from threading import Lock

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# 模拟数据（实际应用中应该从数据库获取）
SAMPLE_BOOKS = [
    {
        'id': 1,
        'title': 'Cien años de soledad',
        'author': 'Gabriel García Márquez',
        'cover': 'https://images-na.ssl-images-amazon.com/images/I/81dQwQlmAXL.jpg',
        'condition': 'Como nuevo',
        'isbn': '978-0307474728',
        'publisher': 'Editorial Sudamericana',
        'why_release': 'Este libro me acompañó en un momento difícil. Ahora quiero que encuentre a alguien que también lo necesite.',
        'user': {
            'name': 'María González',
            'avatar': 'https://i.pravatar.cc/150?img=1',
            'trust_level': 'confiable',
            'trust_badge': '🦉 Compañero Confiable'
        },
        'has_story': True,
        'verified': True
    },
    {
        'id': 2,
        'title': 'El laberinto de la soledad',
        'author': 'Octavio Paz',
        'cover': 'https://images-na.ssl-images-amazon.com/images/I/71QKQ9KJZJL.jpg',
        'condition': 'Buen estado',
        'isbn': '978-9681600128',
        'publisher': 'Fondo de Cultura Económica',
        'why_release': 'Lo leí en la universidad y marcó mi forma de pensar sobre México. Espero que inspire a otros.',
        'user': {
            'name': 'Carlos Ramírez',
            'avatar': 'https://i.pravatar.cc/150?img=12',
            'trust_level': 'bibliofilo',
            'trust_badge': '📖 Bibliófilo Experto'
        },
        'has_story': True,
        'verified': True
    },
    {
        'id': 3,
        'title': 'Pedro Páramo',
        'author': 'Juan Rulfo',
        'cover': 'https://images-na.ssl-images-amazon.com/images/I/81Y5Z8KJZJL.jpg',
        'condition': 'Excelente',
        'isbn': '978-9684110128',
        'publisher': 'Fondo de Cultura Económica',
        'why_release': 'Un clásico que todos deberían leer. Mi copia tiene algunas anotaciones que espero sean útiles.',
        'user': {
            'name': 'Ana Martínez',
            'avatar': 'https://i.pravatar.cc/150?img=5',
            'trust_level': 'novato',
            'trust_badge': '🌵 Lector Novato'
        },
        'has_story': False,
        'verified': False
    }
]

SAMPLE_EXCHANGES = [
    {
        'id': 1,
        'date': '2024-01-15',
        'book1': {
            'title': 'Cien años de soledad',
            'cover': 'https://images-na.ssl-images-amazon.com/images/I/81dQwQlmAXL.jpg',
            'user': 'María González'
        },
        'book2': {
            'title': 'La casa de los espíritus',
            'cover': 'https://images-na.ssl-images-amazon.com/images/I/71QKQ9KJZJL.jpg',
            'user': 'Luis Fernández'
        },
        'message1': 'Gracias por compartir esta historia. Espero que disfrutes tanto como yo.',
        'message2': 'Un intercambio perfecto. ¡Gracias!'
    },
    {
        'id': 2,
        'date': '2024-01-20',
        'book1': {
            'title': 'El laberinto de la soledad',
            'cover': 'https://images-na.ssl-images-amazon.com/images/I/71QKQ9KJZJL.jpg',
            'user': 'Carlos Ramírez'
        },
        'book2': {
            'title': 'Rayuela',
            'cover': 'https://images-na.ssl-images-amazon.com/images/I/81Y5Z8KJZJL.jpg',
            'user': 'Sofía Herrera'
        },
        'message1': 'Un diálogo literario increíble. ¡Gracias!',
        'message2': 'Me encantó tu historia. ¡Que disfrutes el libro!'
    }
]

# =========================
# 简单埋点 & 统计存储（支持数据库持久化 + 内存回退）
# =========================

import json
from collections import defaultdict
from threading import Lock

# 检测是否配置了数据库
_use_database = False
_db_conn = None

def _init_database_if_available():
    """尝试初始化数据库连接（如果配置了环境变量）"""
    global _use_database, _db_conn
    try:
        database_url = (os.environ.get('DATABASE_URL') or 
                       os.environ.get('POSTGRES_URL') or 
                       os.environ.get('NEON_DATABASE_URL') or
                       os.environ.get('SUPABASE_DATABASE_URL'))
        
        if database_url:
            import psycopg2
            # Vercel/Neon 提供的 URL 格式转换
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor()
            
            # 创建表（如果不存在）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS book_exchange_events (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(50) NOT NULL,
                    book_id INTEGER,
                    anon_id TEXT,
                    extra JSONB,
                    ip VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_event_type ON book_exchange_events(event_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON book_exchange_events(created_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_id ON book_exchange_events(book_id)')
            
            conn.commit()
            cursor.close()
            _db_conn = conn
            _use_database = True
            print('✅ 数据库连接成功，使用持久化存储')
            return True
    except ImportError:
        print('⚠️ psycopg2 未安装，使用内存存储')
    except Exception as e:
        print(f'⚠️ 数据库连接失败，使用内存存储: {e}')
    
    _use_database = False
    return False

# 尝试初始化数据库
_init_database_if_available()

# 内存存储（作为回退方案）
_analytics_storage = {
    'events': [],  # 存储所有事件
    'lock': Lock()  # 线程锁
}

def get_analytics_storage():
    """获取分析存储（内存）"""
    return _analytics_storage

def _get_db_connection():
    """获取数据库连接（处理 Neon 自动休眠）"""
    global _db_conn
    if _use_database:
        if _db_conn:
            try:
                # 检查连接是否有效
                _db_conn.cursor().execute('SELECT 1')
                return _db_conn
            except Exception as e:
                # 连接失效（可能是 Neon 休眠），关闭旧连接
                try:
                    _db_conn.close()
                except:
                    pass
                _db_conn = None
        
        # 重新连接（Neon 会自动唤醒）
        if not _db_conn:
            try:
                database_url = (os.environ.get('DATABASE_URL') or 
                               os.environ.get('POSTGRES_URL') or 
                               os.environ.get('NEON_DATABASE_URL') or
                               os.environ.get('SUPABASE_DATABASE_URL'))
                if database_url:
                    import psycopg2
                    if database_url.startswith('postgres://'):
                        database_url = database_url.replace('postgres://', 'postgresql://', 1)
                    _db_conn = psycopg2.connect(database_url)
                    return _db_conn
            except Exception as e:
                print(f'⚠️ 数据库重连失败: {e}')
                return None
    
    return None

def add_event(event_type: str, book_id: Optional[int] = None, 
              anon_id: Optional[str] = None, extra: Dict = None,
              ip: str = '', user_agent: str = ''):
    """添加事件（优先使用数据库，否则使用内存存储）"""
    # 优先使用数据库
    db_conn = _get_db_connection()
    if db_conn:
        try:
            cursor = db_conn.cursor()
            extra_json = json.dumps(extra or {}, ensure_ascii=False)
            cursor.execute('''
                INSERT INTO book_exchange_events 
                (event_type, book_id, anon_id, extra, ip, user_agent)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (event_type, book_id, anon_id, extra_json, ip, user_agent))
            db_conn.commit()
            cursor.close()
            return
        except Exception as e:
            print(f'⚠️ 数据库写入失败，回退到内存存储: {e}')
    
    # 回退到内存存储
    storage = get_analytics_storage()
    with storage['lock']:
        event = {
            'id': len(storage['events']) + 1,
            'event_type': event_type,
            'book_id': book_id,
            'anon_id': anon_id,
            'extra': extra or {},
            'ip': ip,
            'user_agent': user_agent,
            'created_at': datetime.utcnow().isoformat()
        }
        storage['events'].append(event)
        # 限制内存使用：只保留最近 10000 条记录
        if len(storage['events']) > 10000:
            storage['events'] = storage['events'][-10000:]

def get_events(event_type: Optional[str] = None, limit: int = None):
    """获取事件列表（优先从数据库，否则从内存）"""
    # 优先使用数据库
    db_conn = _get_db_connection()
    if db_conn:
        try:
            cursor = db_conn.cursor()
            query = 'SELECT id, event_type, book_id, anon_id, extra, ip, user_agent, created_at FROM book_exchange_events'
            params = []
            if event_type:
                query += ' WHERE event_type = %s'
                params.append(event_type)
            query += ' ORDER BY created_at DESC'
            if limit:
                query += ' LIMIT %s'
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            events = []
            for row in rows:
                try:
                    extra = json.loads(row[4]) if row[4] else {}
                except:
                    extra = {}
                events.append({
                    'id': row[0],
                    'event_type': row[1],
                    'book_id': row[2],
                    'anon_id': row[3],
                    'extra': extra,
                    'ip': row[5] or '',
                    'user_agent': row[6] or '',
                    'created_at': row[7].isoformat() if hasattr(row[7], 'isoformat') else str(row[7])
                })
            cursor.close()
            return events
        except Exception as e:
            print(f'⚠️ 数据库读取失败，回退到内存存储: {e}')
    
    # 回退到内存存储
    storage = get_analytics_storage()
    with storage['lock']:
        events = storage['events']
        if event_type:
            events = [e for e in events if e['event_type'] == event_type]
        if limit:
            events = events[-limit:]
        return events

def count_events(event_type: str) -> int:
    """统计特定类型事件的数量（优先从数据库，否则从内存）"""
    # 优先使用数据库
    db_conn = _get_db_connection()
    if db_conn:
        try:
            cursor = db_conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM book_exchange_events WHERE event_type = %s', (event_type,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            print(f'⚠️ 数据库统计失败，回退到内存存储: {e}')
    
    # 回退到内存存储
    storage = get_analytics_storage()
    with storage['lock']:
        return sum(1 for e in storage['events'] if e['event_type'] == event_type)

def get_distinct_anon_ids(event_type: str) -> set:
    """（旧）获取独立访客 ID 集合，暂保留以兼容后续升级"""
    storage = get_analytics_storage()
    with storage['lock']:
        anon_ids = set()
        for e in storage['events']:
            if e['event_type'] == event_type and e.get('anon_id'):
                anon_ids.add(e['anon_id'])
        return anon_ids


def get_distinct_ips(event_type: str) -> set:
    """获取独立访客 IP 集合（用于 UV 统计，优先从数据库，否则从内存）"""
    # 优先使用数据库
    db_conn = _get_db_connection()
    if db_conn:
        try:
            cursor = db_conn.cursor()
            cursor.execute('SELECT DISTINCT ip FROM book_exchange_events WHERE event_type = %s AND ip IS NOT NULL AND ip != %s', (event_type, ''))
            ips = {row[0] for row in cursor.fetchall()}
            cursor.close()
            return ips
        except Exception as e:
            print(f'⚠️ 数据库查询失败，回退到内存存储: {e}')
    
    # 回退到内存存储
    storage = get_analytics_storage()
    with storage['lock']:
        ips = set()
        for e in storage['events']:
            if e['event_type'] == event_type and e.get('ip'):
                ips.add(e['ip'])
        return ips

def get_daily_stats(days: int = 30):
    """获取按天统计的 PV/UV（优先从数据库，否则从内存）"""
    # 优先使用数据库
    db_conn = _get_db_connection()
    if db_conn:
        try:
            cursor = db_conn.cursor()
            cursor.execute('''
                SELECT DATE(created_at) as day,
                       COUNT(*) as pv,
                       COUNT(DISTINCT ip) as uv
                FROM book_exchange_events
                WHERE event_type = 'page_view'
                  AND created_at >= CURRENT_DATE - INTERVAL '%s days'
                GROUP BY day
                ORDER BY day DESC
                LIMIT %s
            ''', (days, days))
            rows = cursor.fetchall()
            result = [{'day': str(row[0]), 'pv': row[1], 'uv': row[2]} for row in rows]
            cursor.close()
            return result
        except Exception as e:
            print(f'⚠️ 数据库查询失败，回退到内存存储: {e}')
    
    # 回退到内存存储
    storage = get_analytics_storage()
    with storage['lock']:
        daily = defaultdict(lambda: {'pv': 0, 'uv': set()})
        for e in storage['events']:
            if e['event_type'] == 'page_view':
                day = e['created_at'][:10]  # YYYY-MM-DD
                daily[day]['pv'] += 1
                if e.get('ip'):
                    daily[day]['uv'].add(e['ip'])
        
        # 转换为列表格式
        result = []
        for day in sorted(daily.keys(), reverse=True)[:days]:
            result.append({
                'day': day,
                'pv': daily[day]['pv'],
                'uv': len(daily[day]['uv'])
            })
        return result

def init_analytics_db() -> None:
    """初始化分析存储（内存版本，无需初始化）"""
    pass


# 内存存储无需初始化，直接使用即可

@app.route('/')
def index():
    """主页 - 单页面应用"""
    return render_template('index.html')

@app.route('/plaza')
def plaza():
    """图书广场 - 发现页（保留兼容性）"""
    return render_template('plaza.html', books=SAMPLE_BOOKS)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """书籍详情页"""
    book = next((b for b in SAMPLE_BOOKS if b['id'] == book_id), None)
    if not book:
        return "Libro no encontrado", 404
    
    # 模拟交换历史
    exchange_history = [
        {
            'date': '2024-01-10',
            'from_user': 'Juan Pérez',
            'to_user': 'María González',
            'city': 'Ciudad de México'
        },
        {
            'date': '2023-12-05',
            'from_user': 'Ana López',
            'to_user': 'Juan Pérez',
            'city': 'Guadalajara'
        }
    ]
    
    return render_template('book_detail.html', book=book, exchange_history=exchange_history)

@app.route('/exchange-wall')
def exchange_wall():
    """交换墙"""
    return render_template('exchange_wall.html', exchanges=SAMPLE_EXCHANGES)

@app.route('/api/books')
def api_books():
    """获取图书列表API"""
    category = request.args.get('category', '')
    has_story = request.args.get('has_story', '').lower() == 'true'
    verified = request.args.get('verified', '').lower() == 'true'
    
    books = SAMPLE_BOOKS.copy()
    
    if has_story:
        books = [b for b in books if b.get('has_story', False)]
    
    if verified:
        books = [b for b in books if b.get('verified', False)]
    
    return jsonify({'books': books})

@app.route('/api/book/<int:book_id>')
def api_book_detail(book_id):
    """获取图书详情API"""
    book = next((b for b in SAMPLE_BOOKS if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Libro no encontrado'}), 404
    return jsonify(book)

@app.route('/api/exchange/request', methods=['POST'])
def api_exchange_request():
    """提交交换申请API"""
    data = request.get_json()
    
    # 这里应该保存到数据库
    # 现在只是返回成功响应
    
    return jsonify({
        'success': True,
        'message': 'Solicitud de intercambio enviada exitosamente'
    })


@app.route('/api/track', methods=['POST'])
def api_track_event():
    """前端埋点上报接口

    记录：
    - event_type: page_view / share / exchange_request / whatsapp_click 等
    - book_id: 相关图书（可选）
    - anon_id: 前端生成的匿名用户ID，用于 UV 统计
    - extra: 其他JSON数据
    """
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    event_type = (data.get('event_type') or '').strip()

    if not event_type:
        return jsonify({'success': False, 'error': 'event_type is required'}), 400

    book_id = data.get('book_id')
    anon_id = (data.get('anon_id') or '').strip() or None
    extra = data.get('extra') or {}

    # 获取真实 IP（处理代理情况）
    ip = request.headers.get('X-Forwarded-For', '')
    if ip:
        # X-Forwarded-For 可能包含多个 IP，取第一个
        ip = ip.split(',')[0].strip()
    if not ip:
        ip = request.remote_addr or ''
    user_agent = request.headers.get('User-Agent', '')

    # 使用内存存储替代 SQLite
    add_event(
        event_type=event_type,
        book_id=book_id,
        anon_id=anon_id,
        extra=extra,
        ip=ip,
        user_agent=user_agent
    )

    return jsonify({'success': True})


@app.route('/admin/stats')
def admin_stats():
    """简单后台：PV/UV 与关键行为统计 + 最近提交明细 + 书籍浏览数据"""
    # Token 验证：优先使用环境变量，否则使用硬编码的默认 token
    admin_token = os.environ.get('ADMIN_TOKEN', '20260109ForMXG')
    req_token = request.args.get('token')
    
    if not req_token or req_token != admin_token:
        return """
        <!DOCTYPE html>
        <html lang="es-MX">
        <head>
            <meta charset="UTF-8">
            <title>Acceso Restringido - Trueque Digital</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: #F5E6D3;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                }
                .login-box {
                    background: white;
                    border-radius: 15px;
                    padding: 40px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    max-width: 400px;
                    width: 90%;
                }
                h1 {
                    color: #2C5F2D;
                    margin-bottom: 20px;
                    text-align: center;
                }
                .error {
                    color: #d32f2f;
                    background: #ffebee;
                    padding: 12px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    font-size: 14px;
                    text-align: center;
                }
                input {
                    width: 100%;
                    padding: 12px;
                    border: 2px solid #E8D5B7;
                    border-radius: 8px;
                    font-size: 16px;
                    margin-bottom: 20px;
                    box-sizing: border-box;
                }
                input:focus {
                    outline: none;
                    border-color: #2C5F2D;
                }
                button {
                    width: 100%;
                    padding: 12px;
                    background: #2C5F2D;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                button:hover {
                    background: #4A7C59;
                }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h1>🔒 Acceso Restringido</h1>
                <form method="GET" action="/admin/stats">
                    <input type="password" name="token" placeholder="Ingresa el token de acceso" required autofocus>
                    <button type="submit">Acceder</button>
                </form>
            </div>
        </body>
        </html>
        """, 403

    # 使用内存存储获取统计数据
    total_pv = count_events('page_view')
    # UV 使用 IP 维度，便于内部核对
    total_uv = len(get_distinct_ips('page_view'))
    
    # 书籍浏览统计
    total_book_views = count_events('book_view')
    # 被浏览过的不同书本数
    book_view_events = get_events('book_view')
    viewed_book_ids = {e.get('book_id') for e in book_view_events if e.get('book_id') is not None}
    
    stats = {
        'total_pv': total_pv,
        'total_uv': total_uv,
        'share_count': count_events('share'),
        'exchange_request_count': count_events('exchange_request'),
        'whatsapp_click_count': count_events('whatsapp_click'),
        'book_view_count': total_book_views,
        'book_view_unique_books': len(viewed_book_ids),
    }
    
    # 按天聚合 PV/UV（最近30天）
    daily = get_daily_stats(30)

    # 最近提交明细（最多 50 条，按时间倒序）
    recent_submits = []
    events = get_events('exchange_request', limit=50)
    for e in reversed(events):  # 最新的在前
        extra = e.get('extra') or {}
        book_title = None
        try:
            book_id = e.get('book_id')
            if isinstance(book_id, int):
                for b in SAMPLE_BOOKS:
                    if b.get('id') == book_id:
                        book_title = b.get('title')
                        break
        except Exception:
            book_title = None
        
        recent_submits.append({
            'created_at': e.get('created_at'),
            'book_id': e.get('book_id'),
            'book_title': book_title,
            'story_snippet': extra.get('story_snippet') or '',
            'story_length': extra.get('story_length') or 0,
            'has_image': bool(extra.get('has_image')),
            # 内部使用完整 IP，便于校验
            'ip': e.get('ip') or ''
        })

    # 传递 token 到模板，用于生成带 token 的链接
    return render_template('admin_stats.html', stats=stats, daily=daily, recent_submits=recent_submits, token=req_token)

@app.route('/static/<path:path>')
def send_static(path):
    """提供静态文件"""
    import urllib.parse
    from flask import abort, Response
    import os
    
    # 处理URL编码的路径
    decoded_path = urllib.parse.unquote(path)
    
    # 在Vercel环境下，静态文件可能在多个位置
    # 尝试多个可能的路径
    possible_dirs = [
        Path(app.static_folder or 'static'),
        Path('static'),
        Path(os.getcwd()) / 'static',
        Path('/var/task/static'),
        Path('/vercel/path0/static'),
    ]
    
    file_path = None
    for static_dir in possible_dirs:
        if not static_dir.exists():
            continue
            
        try:
            # 尝试解码后的路径
            file_path = static_dir / decoded_path
            if file_path.exists() and file_path.is_file():
                file_path = file_path.resolve()
                static_dir_resolved = static_dir.resolve()
                # 安全检查
                if str(file_path).startswith(str(static_dir_resolved)):
                    break
            
            # 尝试原始路径（未解码）
            file_path = static_dir / path
            if file_path.exists() and file_path.is_file():
                file_path = file_path.resolve()
                static_dir_resolved = static_dir.resolve()
                # 安全检查
                if str(file_path).startswith(str(static_dir_resolved)):
                    break
            
            file_path = None
        except Exception as e:
            continue
    
    if file_path and file_path.exists() and file_path.is_file():
        # 设置正确的Content-Type
        mimetype = None
        if file_path.suffix.lower() in ['.jpg', '.jpeg']:
            mimetype = 'image/jpeg'
        elif file_path.suffix.lower() == '.png':
            mimetype = 'image/png'
        
        # 添加缓存头，优化加载速度
        response = send_file(file_path, mimetype=mimetype)
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response
    else:
        # 如果所有路径都失败，返回404
        abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('=' * 60)
    print('🚀 Trueque Digital - 墨西哥图书交换平台')
    print('=' * 60)
    print(f'✅ 服务启动成功')
    print(f'📱 访问地址: http://localhost:{port}')
    print(f'📚 图书广场: http://localhost:{port}/')
    print(f'🤝 交换墙: http://localhost:{port}/exchange-wall')
    print('=' * 60)
    print('🛑 按 Ctrl+C 停止服务')
    print('=' * 60)
    print('')
    app.run(host='0.0.0.0', port=port, debug=True)

