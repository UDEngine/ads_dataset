from typing import Optional, Dict
import streamlit as st
from lib import get_db

def login_form():
    """登录表单组件"""
    st.title("管理员系统登录")
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("👑用户名", key="login_username")
        password = st.text_input("🔑密码", type="password", key="login_password")
        submitted = st.form_submit_button("🚪 登录")

        if submitted:
            if not username or not password:
                st.error("⚠️请输入用户名和密码")
            elif verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_info = get_user_info(username=username)
                st.success("✅登录成功!")

                # 设置查询参数以保持登录状态
                st.query_params.token=username
                st.rerun()
            else:
                st.error("⚠️用户名或密码错误")

    # 添加一些样式
    st.markdown("""
    <style>
        #the-title {
            text-align: center
        }
        .stForm {
            max-width: 400px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """初始化 session state"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'

    # 检查当前页面状态
    if st.query_params.get('page') and not st.session_state.logged_in:
        st.session_state.current_page = st.query_params.page

    # 检查 URL 查询参数中的登录状态
    if st.query_params.get('token') and not st.session_state.logged_in:
        token = st.query_params.token
        # 这里应该验证 token 的有效性
        st.session_state.logged_in = True
        st.session_state.username = token  # 或者从 token 中解码出用户名
        st.session_state.user_info = get_user_info(username=token)


def is_logged_in() -> bool:
    """检查用户是否已登录"""
    return st.session_state.get('logged_in', False)

def verify_user(username: str, password: str) -> bool:
    """验证用户凭据"""
    try:
        db = get_db()
        user = db.get_one("admins", "username = %s", (username,))
        if user:
            # 在实际应用中，这里应该使用密码哈希验证
            stored_password = user['password']
            return password == stored_password
        return False
    except Exception as e:
        print(e)
        return False

def get_user_info(username: str) -> Optional[Dict]:
    """获取用户信息"""
    try:
        db = get_db()
        return db.get_one(
            "admins",
            "username = %s",
            username
        )
    except Exception as e:
        print(e)
        return None

def logout():
    """退出登录"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_info = None
    st.session_state.current_page = 'dashboard'
    st.query_params.clear()
    st.rerun()