import os
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="บทเรียน 515113", page_icon="📚", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LESSON_DIR = os.path.join(BASE_DIR, "lessons")

# ชื่อไฟล์ต้องตรงกับไฟล์ในโฟลเดอร์ lessons/ ทุกตัวอักษร (รวมช่องว่างและตัวพิมพ์เล็ก-ใหญ่)
LESSONS = [
    {
        "key": "cloud",
        "icon": "☁️",
        "title": "Cloud Chamber จำลอง",
        "file": "Cloud Chamber.html",
        "desc": "ปรับอุณหภูมิ ใส่สนามแม่เหล็ก เปลี่ยนแหล่งกำเนิดรังสี แล้วเก็บข้อมูลการนับ",
    },
    {
        "key": "nuclear",
        "icon": "🧲",
        "title": "ห้องทดลองสร้างนิวเคลียส",
        "file": "nuclear_lab.html",
        "desc": "ประกอบนิวเคลียส ดูสปินและความถี่ Larmor ส่งคลื่น RF ให้สั่นพ้อง ศึกษา T1 และ T2 ไปจนถึงภาพ MRI",
    },
]

def go(page, lesson=None):
    st.session_state.page = page
    st.session_state.lesson = lesson


if "page" not in st.session_state:
    st.session_state.page = "home"
    st.session_state.lesson = None

st.title("📚 บทเรียน 515113")

# หน้าแรก: ปุ่มบทเรียน
if st.session_state.page == "home":
    st.button("📚  บทเรียน 515113", type="primary", on_click=go, args=("lessons",))

# หน้าเลือกบทเรียน: ปุ่มแยกสองหัวข้อ
elif st.session_state.page == "lessons":
    st.button("◀ กลับหน้าแรก", on_click=go, args=("home",))
    st.subheader("เลือกบทเรียน")
    cols = st.columns(len(LESSONS))
    for col, L in zip(cols, LESSONS):
        with col:
            st.caption(L["desc"])
            st.button(
                f"{L['icon']}  {L['title']}",
                key=f"pick_{L['key']}",
                type="primary",
                on_click=go,
                args=("lesson", L["key"]),
            )

# หน้าบทเรียน: แสดงไฟล์ HTML
elif st.session_state.page == "lesson":
    L = next((x for x in LESSONS if x["key"] == st.session_state.lesson), None)
    st.button("◀ กลับไปเลือกบทเรียน", on_click=go, args=("lessons",))
    if L is None:
        st.error("ไม่พบบทเรียนที่เลือก")
    else:
        st.subheader(f"{L['icon']} {L['title']}")
        path = Path(LESSON_DIR) / L["file"]
        if path.exists():
            # height="content" ทำให้กรอบสูงเท่าเนื้อหา จึงไม่มีแถบเลื่อนซ้อน
            st.iframe(path, width="stretch", height="content")
        else:
            st.error(f"ไม่พบไฟล์บทเรียน: {path}")