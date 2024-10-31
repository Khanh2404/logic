from pyswip import Prolog
import tkinter as tk
from tkinter import messagebox

# Cơ sở tri thức về triệu chứng và bệnh với lời khuyên
prolog = Prolog()
prolog.consult("kham.pl")
benh = {
    'Viêm kết mạc': ['mắt đỏ', 'mắt ngứa', 'mắt cay', 'mắt nhử', 'mắt lác', 'ngứa mắt','mọng mắt', "Có thể là viêm kết mạc. Nên đến bác sĩ để kiểm tra."],
    'Cườm nước': ['mắt nhỏ nước', 'mắt mờ', 'mắt đau', "Có thể là cườm nước. Cần kiểm tra mắt ngay."],
    'Loét giác mạc': ['mắt đau', 'mắt cay', 'mắt mờ', "Có thể là loét giác mạc. Nên đến bác sĩ chuyên khoa."],
    'Viêm tai giữa': ['tai đau', 'tai nghe kém', 'sốt', "Có thể là viêm tai giữa. Cần điều trị sớm."],
    'Rối loạn thính lực': ['tai nghe kém', 'mất cân bằng', 'ù tai', "Có thể là rối loạn thính lực. Tham khảo ý kiến bác sĩ."],
    'Viêm tai ngoài': ['tai sưng', 'tai đau', 'ù tai','ngứa tai', "Có thể là viêm tai ngoài. Cần theo dõi tình trạng tai."],
    'Viêm xoang': ['mũi tắc', 'mũi nhọt', 'đau đầu', "Có thể là viêm xoang. Cần sử dụng thuốc giảm đau."],
    'Viêm mũi dị ứng': ['mũi ngứa', 'mũi tắc', 'hắt xì', "Có thể là viêm mũi dị ứng. Tránh tiếp xúc với dị nguyên."],
    'Polyp mũi': ['mũi tắc', 'mất khứu giác', 'đau đầu', "Có thể là polyp mũi. Nên kiểm tra định kỳ."],
    'Viêm họng cấp': ['họng đau', 'sốt', 'nuốt khó', "Có thể là viêm họng cấp. Uống nhiều nước và nghỉ ngơi."],
    'Ung thư vòm họng': ['họng đau', 'sốt', 'nuốt đau', "Có thể là ung thư vòm họng. Cần tham khảo ý kiến bác sĩ ngay."],
    'Viêm amidan': ['họng đau', 'ho', 'khàn tiếng', "Có thể là viêm amidan. Nên đến bác sĩ nếu triệu chứng nặng."],
}

trieu_chung = set()

def chuan_doan():
    if not trieu_chung:
        messagebox.showinfo("Kết quả", "Vui lòng chọn triệu chứng trước!")
        return

    phan_tram = {}
    for benh_name, tri_list in benh.items():
        matched_symptoms = trieu_chung.intersection(set(tri_list[:-1]))  # Chỉ xét triệu chứng
        phan_tram[benh_name] = len(matched_symptoms) / len(tri_list[:-1]) * 100 if tri_list[:-1] else 0

    filtered_list = [(b, p) for b, p in phan_tram.items() if p > 0]
    if not filtered_list:
        messagebox.showinfo("Kết quả", "Không tìm thấy bệnh phù hợp với triệu chứng!")
    else:
        filtered_list.sort(key=lambda x: x[1], reverse=True)
        benh_max, max_phan_tram = filtered_list[0]
        loi_khuyen = benh[benh_max][-1]  # Lời khuyên
        messagebox.showinfo("Kết quả", f"Kết luận: Bệnh: {benh_max} ({max_phan_tram:.2f}%)\n\n{loi_khuyen}")

    trieu_chung.clear()

def chon_trieu_chung(trieu_chung_input):
    if trieu_chung_input in trieu_chung:
        messagebox.showwarning("Cảnh báo", f"Triệu chứng '{trieu_chung_input}' đã được chọn trước đó.")
    else:
        trieu_chung.add(trieu_chung_input)
        messagebox.showinfo("Thông báo", f"Đã chọn triệu chứng: {trieu_chung_input}")

def them_trieu_chung_tu_nhap():
    # Lấy triệu chứng từ ô nhập liệu
    symptom = symptom_entry.get().strip()
    if symptom:
        chon_trieu_chung(symptom)  # Thêm triệu chứng vào danh sách triệu chứng
        symptom_entry.delete(0, tk.END)  # Xóa nội dung sau khi nhập
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập triệu chứng.")

def hien_thi_trieu_chung(bo_phan):
    for widget in root.winfo_children():
        widget.destroy()
        
    label = tk.Label(root, text=f"Chọn triệu chứng cho bộ phận: {bo_phan}", font=("Helvetica", 14))
    label.pack(pady=10)

    if bo_phan == 'Mắt':
        trieu_chung_list = ['mắt đỏ', 'mắt ngứa', 'mắt cay', 'mắt nhỏ nước', 'mắt mờ', 'mắt đau']
    elif bo_phan == 'Tai':
        trieu_chung_list = ['tai đau', 'tai nghe kém', 'sốt', 'mất cân bằng', 'ù tai', 'tai sưng']
    elif bo_phan == 'Mũi':
        trieu_chung_list = ['mũi tắc', 'mũi nhọt', 'đau đầu', 'mũi ngứa', 'hắt xì', 'mất khứu giác']
    elif bo_phan == 'Họng':
        trieu_chung_list = ['họng đau', 'sốt', 'nuốt khó', 'nuốt đau', 'ho', 'khàn tiếng']
        
    for i in range(0, len(trieu_chung_list), 3):
        row_frame = tk.Frame(root)
        row_frame.pack(pady=5)
        for tri in trieu_chung_list[i:i+3]:
            button = tk.Button(row_frame, text=tri, command=lambda tc=tri: chon_trieu_chung(tc), width=10, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 12))
            button.pack(side=tk.LEFT, padx=5)

    # Thêm ô nhập liệu và nút để thêm triệu chứng
    # entry_label = tk.Label(root, text="Hoặc tự nhập triệu chứng:", font=("Helvetica", 12))
    # entry_label.pack(pady=5)

    # global symptom_entry
    # symptom_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
    # symptom_entry.pack(pady=5)

    # add_symptom_button = tk.Button(root, text="Thêm triệu chứng", command=them_trieu_chung_tu_nhap, bg="#009688", fg="white", font=("Helvetica", 12), width=15, height=1)
    # add_symptom_button.pack(pady=10)

    #Nút "Kiểm tra bệnh" và "Trở lại" ở góc dưới cùng
    kiem_tra_button = tk.Button(root, text="Kiểm tra bệnh", command=chuan_doan, bg="#2196F3", fg="white", font=("Helvetica", 13), width=13, height=1)
    kiem_tra_button.place(relx=0.55, rely=0.75)

    tro_lai_button = tk.Button(root, text="Trở lại", command=hien_thi_lua_chon_bo_phan, bg="#FF5722", fg="white", font=("Helvetica", 10), width=10, height=1)
    tro_lai_button.place(relx=0.55, rely=0.85)

def hien_thi_lua_chon_bo_phan():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Bạn hãy chọn bộ phận cần khám", font=("Helvetica", 14))
    label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    bo_phan_buttons = {
        'Mắt': lambda: hien_thi_trieu_chung('Mắt'),
        'Tai': lambda: hien_thi_trieu_chung('Tai'),
        'Mũi': lambda: hien_thi_trieu_chung('Mũi'),
        'Họng': lambda: hien_thi_trieu_chung('Họng'),
    }

    for i, (bo_phan, command) in enumerate(bo_phan_buttons.items()):
        button = tk.Button(button_frame, text=bo_phan, command=command, width=10, height=2, bg="#3F51B5", fg="white", font=("Helvetica", 12))
        button.grid(row=i//2, column=i%2, padx=10, pady=5)

# Tạo giao diện Tkinter
root = tk.Tk()
root.geometry("500x500")
root.title("Chẩn đoán bệnh qua triệu chứng")

hien_thi_lua_chon_bo_phan()

root.mainloop()
