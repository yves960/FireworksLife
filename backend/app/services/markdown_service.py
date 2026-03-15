"""
Markdown 渲染服务
"""
import markdown
import bleach
from typing import Optional

# 允许的 HTML 标签
ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code',
    'div', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'hr', 'i', 'img', 'li', 'ol', 'p', 'pre', 'span',
    'strong', 'table', 'tbody', 'td', 'th', 'thead', 'tr', 'ul'
]

# 允许的 HTML 属性
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'div': ['class'],
    'span': ['class'],
    'code': ['class'],
    'pre': ['class'],
    'td': ['align'],
    'th': ['align'],
}

# 允许的协议
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def render_markdown(text: str) -> str:
    """
    将 Markdown 文本渲染为安全的 HTML
    
    Args:
        text: Markdown 文本
        
    Returns:
        渲染后的安全 HTML
    """
    if not text:
        return ""
    
    # 配置 Markdown 扩展
    extensions = [
        'fenced_code',      # 代码块
        'codehilite',       # 代码高亮
        'tables',           # 表格
        'toc',              # 目录
        'nl2br',            # 换行转 <br>
        'sane_lists',       # 更好的列表处理
    ]
    
    extension_configs = {
        'codehilite': {
            'css_class': 'highlight',
            'linenums': False,
        }
    }
    
    # 渲染 Markdown
    html = markdown.markdown(
        text,
        extensions=extensions,
        extension_configs=extension_configs
    )
    
    # 清理 XSS 攻击向量
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    
    # 为外部链接添加 rel="noopener noreferrer"
    clean_html = bleach.linkify(
        clean_html,
        callbacks=[_add_link_rel],
        skip_tags=['pre', 'code']
    )
    
    return clean_html


def _add_link_rel(attrs, new=False):
    """
    为链接添加安全属性
    """
    if 'href' in attrs:
        href = attrs['href']
        if isinstance(href, str) and href.startswith(('http://', 'https://')):
            attrs['rel'] = 'noopener noreferrer'
            attrs['target'] = '_blank'
    return attrs


def get_plain_text_summary(text: str, max_length: int = 200) -> str:
    """
    获取纯文本摘要
    
    Args:
        text: Markdown 文本
        max_length: 最大长度
        
    Returns:
        纯文本摘要
    """
    if not text:
        return ""
    
    # 移除 Markdown 语法
    import re
    plain = re.sub(r'[#*_`~\[\]()>-]', '', text)
    plain = re.sub(r'\n+', ' ', plain)
    plain = plain.strip()
    
    if len(plain) > max_length:
        return plain[:max_length] + '...'
    
    return plain