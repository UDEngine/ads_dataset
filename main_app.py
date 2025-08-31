
import streamlit as st

from components import init_session_state
from components.login_form import login_form, is_logged_in, logout
from lib import get_db

# 这必须是第一个 Streamlit 命令
st.set_page_config(layout="wide")

# 获取数据库管理器
db = get_db()

# 初始化 session state
init_session_state()

# 根据登录状态显示不同内容
if is_logged_in():

    # 显示主应用界面
    from components.sidebar import show_sidebar
    show_sidebar()

    # 显示当前页面内容
    page = st.session_state.get('current_page', 'dashboard')
    if page == 'dashboard':
        from pages.dashboard import show_dashboard
        show_dashboard()
    elif page == 'user_manage':
        from pages.user_manage import show_user_management
        show_user_management()
    elif page == 'task_data':
        from pages.task_data import show_task_data
        show_task_data()
    elif page == 'settings':
        from pages.settings import show_settings
        show_settings()
    elif page == 'logout':
        logout()
else:
    # 显示登录界面
    login_form()
