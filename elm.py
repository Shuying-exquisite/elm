import streamlit as st
import subprocess

# 定义执行Shell脚本的函数
def run_shell_script(elmck):
    # 执行Shell脚本
    result = subprocess.run(["./elm.sh", elmck], capture_output=True, text=True)
    return result.stdout, result.stderr

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
