from flask import Flask, render_template, request
from lunarcalendar import Converter, Solar

app = Flask(__name__)

def sum_digits(s):
    return sum(int(c) for c in str(s) if c.isdigit())

def get_quai_menh(gender, lunar_year):
    total = sum_digits(lunar_year)
    r = total % 9
    if gender.lower() == "nam":
        m = {1: "KHẢM", 2: "LY", 3: "CẤN", 4: "ĐOÀI", 5: "CÀN", 6: "KHÔN", 7: "TỐN", 8: "CHẤN", 9: "KHÔN", 0: "KHÔN"}
    else:
        m = {1: "CẤN", 2: "CÀN", 3: "ĐOÀI", 4: "CẤN", 5: "LY", 6: "KHẢM", 7: "KHÔN", 8: "CHẤN", 9: "TỐN", 0: "TỐN"}
    return m[r]

def get_quai_so(phone_number):
    r = sum_digits(phone_number) % 9
    m = {1: "KHẢM", 2: "KHÔN", 3: "CHẤN", 4: "TỐN", 5: "KHÔN", 6: "CÀN", 7: "ĐOÀI", 8: "CẤN", 9: "LY", 0: "LY"}
    return m[r]

def get_ket_qua_ket_hop(q1, q2):
    mapping = {
        "CÀNCÀN": "Phục Vị", "CÀNKHẢM": "Lục Sát", "CÀNCẤN": "Thiên y", "CÀNCHẤN": "Ngũ Quỷ",
        "CÀNTỐN": "Họa Hại", "CÀNLY": "Tuyệt Mệnh", "CÀNKHÔN": "Diên Niên", "CÀNĐOÀI": "Sinh Khí",
        # (Thêm đầy đủ như bạn đã gửi ở trên)
    }
    return mapping.get(q1 + q2, "Không xác định")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone = request.form["phone"]
        day = int(request.form["day"])
        month = int(request.form["month"])
        year = int(request.form["year"])
        gender = request.form["gender"]

        try:
            solar = Solar(year, month, day)
            lunar = Converter.Solar2Lunar(solar)
            lunar_date = f"{lunar.day}/{lunar.month}/{lunar.year}"
            quai1 = get_quai_menh(gender, lunar.year)
            quai2 = get_quai_so(phone)
            ketqua = get_ket_qua_ket_hop(quai1, quai2)

            return render_template("index.html",
                                   phone=phone,
                                   solar_date=f"{day}/{month}/{year}",
                                   lunar_date=lunar_date,
                                   quai1=quai1,
                                   quai2=quai2,
                                   ketqua=ketqua)
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
