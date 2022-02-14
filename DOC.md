
molecular/ 
    _init_.py
    descriptions.py            CONSTANT VARIABLE เกี่ยวกับคำอธิบาย
    names.py                   CONSTANT VARIABLE เกี่ยวกับชื่อ
    operators.py               ไฟล์ที่ทำการรัน simulate จำลองการทำ mocular โดยมีเรียกใช้ไฟล์ core.pyx แล้วนำค่าที่ได้กลับมาใส่ใน       blender particle system
    simulate.py                ใส่ค่าเริ่มต้นให้กับระบบ simulate
    ui.py                      หน้าต่าง UI ใน blender
    utils.py                   ฟังก์ชันช่วยเพิ่มเติม
source/
    core.pyx                  ไฟล์หลักในการคำนวณค่าต่างๆ ก่อนจะ return importdata ที่คำนวณแล้วกลับไป
    setup.bat                 compiling core.pyx, ย้ายไฟล์และลบไฟล์ที่ไม่จำเป็น
    setup.py                  ตั้งค่า complie สำหรับ cython
make_release.py               ใช้รันสำหรับสร้าง file zip addon และพร้อใสำหรับใช้ใน blender - คำสั่ง 'python make_release.py' 

---

core.pyx function สำคัญ
- init(importdata) ตั้งค่าเริ่มต้นการคำนวณ, ถูกเรียกใข้งานเพียงครั้งเดียวเมื่อ addon เริ่มทำงาน (ถูกเรียกใช้จาก operators.py)
- simulate(importdata) ฟังก์ชันหลักจำลองการทำงานของ molecular, ถูกเรียกใช้งาน 1ครั้ง/framesubstep  (ฟังก์ชันชันที่ 2 ที่ถูกเรียกใช้โดย operators.py)
- update(data) นำค่าที่นำเข้ามาจาก importdata ของฟังก์ชัน simulate เข้าไปอัพเดรตข้อมูลปัจจุบันก่อนเริ่มการคำนวณ
- create_link(int par_id, int max_link, int parothers_id=-1) สร้าง link ระหว่าง particle
- solve_link(Particle *par) - คำนวณค่า particle ใน link
- collide(Particle *par) - คำนวณค่า self-collision ระหว่าง particle

---------
ฟังก์ชันที่ถูกสร้างเพิ่มเติมขึ้นมา
- remove_link(Particle *par) ลบ link ระหว่าง particle (ถูกเรียกใช้โดย create_link)
