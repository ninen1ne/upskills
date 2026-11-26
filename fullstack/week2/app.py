from flask import Flask, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret"  # ใช้เซ็น session (ตะกร้า) เปลี่ยนเป็นค่าสุ่มของคุณเอง

# ---------- ข้อมูลสินค้า (แก้ชื่อ ราคา รูปได้ที่นี่) ----------
DRINKS = [
    {"id": 1, "name": "Iced Americano", "price": 55, "desc": "กาแฟดำเข้มหอม ดื่มเย็นสดชื่น",
     "img": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80"},
    {"id": 2, "name": "Iced Latte", "price": 65, "desc": "เอสเปรสโซนุ่มๆ ผสมนมสด",
     "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&q=80"},
    {"id": 3, "name": "Fresh Orange Juice", "price": 60, "desc": "น้ำส้มคั้นสด ไม่ใส่น้ำตาลเพิ่ม",
     "img": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=600&q=80"},
    {"id": 4, "name": "Bubble Milk Tea", "price": 59, "desc": "ชานมไข่มุก หวานมัน เคี้ยวหนึบ",
     "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?w=600&q=80"},
    {"id": 5, "name": "Lemon Iced Tea", "price": 45, "desc": "ชามะนาวเย็น เปรี้ยวหวานกำลังดี",
     "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&q=80"},
    {"id": 6, "name": "Berry Smoothie", "price": 70, "desc": "สมูทตี้เบอร์รี่รวม ปั่นเนียน",
     "img": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80"},
]
BY_ID = {d["id"]: d for d in DRINKS}

# รูปสำรองสีเทา ใช้ตอนลิงก์รูปโหลดไม่ได้
FALLBACK = ("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27600%27 height=%27400%27%3E"
            "%3Crect width=%27100%25%27 height=%27100%25%27 fill=%27%23dee2e6%27/%3E%3C/svg%3E")

# ---------- HTML (อยู่ในไฟล์นี้ทั้งหมด) ----------
PAGE = """<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>.card-img-top{height:200px;object-fit:cover}</style>
</head>
<body class="bg-light">
<nav class="navbar navbar-dark bg-dark mb-4">
  <div class="container">
    <a class="navbar-brand" href="{{ url_for('shop') }}">Cool Sip</a>
    <a class="btn btn-outline-light btn-sm" href="{{ url_for('cart') }}">
      ตะกร้า <span class="badge text-bg-warning">{{ cart_count }}</span>
    </a>
  </div>
</nav>

<main class="container pb-5">
{% if view == 'shop' %}
  <h1 class="h3 mb-4">เมนูเครื่องดื่ม</h1>
  <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">
    {% for d in drinks %}
    <div class="col">
      <div class="card h-100 shadow-sm">
        <img src="{{ d.img }}" class="card-img-top" alt="{{ d.name }}"
             onerror="this.onerror=null;this.src='{{ fallback }}'">
        <div class="card-body">
          <h2 class="h5 card-title">{{ d.name }}</h2>
          <p class="card-text text-muted">{{ d.desc }}</p>
        </div>
        <div class="card-footer bg-white d-flex justify-content-between align-items-center">
          <span class="fw-bold">฿{{ "{:,}".format(d.price) }}</span>
          <form method="post" action="{{ url_for('add', did=d.id) }}">
            <button class="btn btn-primary btn-sm">ใส่ตะกร้า</button>
          </form>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>

{% else %}
  <h1 class="h3 mb-4">ตะกร้าสินค้า</h1>
  {% if items %}
  <div class="table-responsive bg-white shadow-sm rounded">
    <table class="table align-middle mb-0">
      <thead><tr><th>สินค้า</th><th class="text-end">ราคา</th><th class="text-end">จำนวน</th><th class="text-end">รวม</th><th></th></tr></thead>
      <tbody>
      {% for i in items %}
        <tr>
          <td>{{ i.name }}</td>
          <td class="text-end">฿{{ "{:,}".format(i.price) }}</td>
          <td class="text-end">{{ i.qty }}</td>
          <td class="text-end">฿{{ "{:,}".format(i.sub) }}</td>
          <td class="text-end">
            <form method="post" action="{{ url_for('remove', did=i.id) }}">
              <button class="btn btn-outline-danger btn-sm">ลบ</button>
            </form>
          </td>
        </tr>
      {% endfor %}
      </tbody>
      <tfoot><tr><th colspan="3" class="text-end">ยอดรวม</th><th class="text-end">฿{{ "{:,}".format(total) }}</th><th></th></tr></tfoot>
    </table>
  </div>
  {% else %}
  <div class="alert alert-secondary">ตะกร้ายังว่าง เลือกเครื่องดื่มที่ชอบได้เลย</div>
  {% endif %}
  <a class="btn btn-link mt-3 ps-0" href="{{ url_for('shop') }}">&larr; กลับไปเลือกเมนู</a>
{% endif %}
</main>
</body>
</html>"""


# ---------- ตะกร้า (เก็บใน session) ----------
def get_cart():
    items, total, count = [], 0, 0
    for did, qty in session.get("cart", {}).items():
        d = BY_ID.get(int(did))
        if d:
            sub = d["price"] * qty
            items.append({**d, "qty": qty, "sub": sub})
            total += sub
            count += qty
    return items, total, count


@app.context_processor
def inject_globals():
    return {"cart_count": get_cart()[2], "fallback": FALLBACK}


# ---------- Routes ----------
@app.route("/")
def shop():
    return render_template_string(PAGE, view="shop", drinks=DRINKS)


@app.route("/cart")
def cart():
    items, total, _ = get_cart()
    return render_template_string(PAGE, view="cart", items=items, total=total)


@app.post("/add/<int:did>")
def add(did):
    if did in BY_ID:
        c = session.get("cart", {})
        c[str(did)] = c.get(str(did), 0) + 1
        session["cart"] = c
    return redirect(url_for("shop"))


@app.post("/remove/<int:did>")
def remove(did):
    c = session.get("cart", {})
    c.pop(str(did), None)
    session["cart"] = c
    return redirect(url_for("cart"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # ใช้ 5001 เลี่ยงพอร์ต 5000 ที่ Mac มักถูกจอง
    # app.run(host="0.0.0.0", debug=False, port=5001)  # allow same network to join