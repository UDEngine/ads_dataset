import streamlit as st
from components import logout

def show_sidebar():
    """显示侧边栏导航"""
    with st.sidebar:
        st.title("导航菜单")

        # 显示用户信息
        if st.session_state.user_info:
            st.write(f"欢迎, **{st.session_state.user_info['username']}**")

        # 导航选项
        page_options = {
            "dashboard": "🏠仪表板",
            "user_manage": "👤用户管理",
            "task_data": "📊任务管理",
            "settings": "⚙️系统设置",
            "logout": "🚪退出登录"
        }

        # 创建导航按钮
        for page_id, page_info in page_options.items():
            if st.sidebar.button(
                    page_info,
                    key=f"nav_{page_id}",
                    disabled=st.session_state.current_page == page_id,
                    use_container_width=True
            ):
                st.session_state.current_page = page_id
                st.query_params.page = page_id
                st.rerun()

        # selected_page = st.radio(
        #     "选择页面",
        #     list(page_options.keys()),
        #     format_func=lambda x: page_options[x]
        # )
        # st.session_state.current_page = selected_page

        # 添加一些样式
        st.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-color: #f0f2f6;
            }
        </style>
        """, unsafe_allow_html=True)