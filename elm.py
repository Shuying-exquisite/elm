import streamlit as st
import subprocess
import os

# 添加执行权限
def add_execute_permission(script_path):
    try:
        os.chmod(script_path, 0o755)  # 添加执行权限
        st.write("已成功添加执行权限")
    except Exception as e:
        st.write(f"添加执行权限时出现错误：{e}")

# 定义执行Shell脚本的函数
def run_shell_script(elmck):
    try:
        script_path = os.path.join(os.path.dirname(__file__), "elm.sh")
        add_execute_permission(script_path)  # 添加执行权限
        
        # 调试信息
        st.write(f"当前工作目录: {os.getcwd()}")
        st.write(f"__file__: {__file__}")
        st.write(f"脚本路径: {script_path}")
        st.write(f"文件存在: {os.path.isfile(script_path)}")
        st.write(f"文件可执行: {os.access(script_path, os.X_OK)}")

        # 执行Shell脚本
        result = subprocess.run([script_path, elmck], capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return str(e), ""

# Streamlit界面
st.title("饿了么自动化脚本")

# 用户输入elmck
elmck = st.text_input("请输入elmck值:")

if st.button("执行脚本"):
    if elmck:
        st.write("脚本正在执行，请稍候...")
        stdout, stderr = run_shell_script(elmck)
        st.write("脚本输出:")
        st.text(stdout)
        if stderr:
            st.write("脚本错误:")
            st.text(stderr)
    else:
        st.write("请输入elmck值")

