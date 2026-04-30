# 🛡️ BFStock Tracker - AI Instructions & Guidelines

Tài liệu này chứa các quy tắc bắt buộc mà AI phải tuân thủ khi làm việc trên dự án BFStock. Tuyệt đối không được tự ý thay đổi dữ liệu cốt lõi nếu không có yêu cầu cụ thể.

## 🍎 1. Danh sách Trái Ác Quỷ Chuẩn (Whitelist)
Chỉ được phép hiển thị và sử dụng dữ liệu từ danh sách 41 trái dưới đây. Mọi trái khác ngoài danh sách này đều được coi là dữ liệu rác của API và phải bị loại bỏ.

| Tên Trái | Rarity | Beli | Robux | Type | Tên cũ / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rocket** | Common | 5,000 | 50 | Natural | Thay thế Kilo |
| **Spin** | Common | 7,500 | 75 | Natural | |
| **Blade** | Common | 30,000 | 100 | Natural | Thay thế Chop |
| **Spring** | Common | 60,000 | 180 | Natural | |
| **Bomb** | Common | 80,000 | 220 | Natural | |
| **Smoke** | Common | 100,000 | 250 | Elemental | |
| **Spike** | Common | 180,000 | 380 | Natural | |
| **Flame** | Uncommon | 250,000 | 550 | Elemental | |
| **Ice** | Uncommon | 350,000 | 750 | Elemental | |
| **Sand** | Uncommon | 420,000 | 850 | Elemental | |
| **Dark** | Uncommon | 500,000 | 950 | Elemental | |
| **Eagle** | Uncommon | 550,000 | 975 | Beast | Thay thế Falcon |
| **Diamond** | Uncommon | 600,000 | 1,000 | Natural | |
| **Light** | Rare | 650,000 | 1,100 | Elemental | |
| **Rubber** | Rare | 750,000 | 1,200 | Natural | |
| **Ghost** | Rare | 940,000 | 1,275 | Natural | Thay thế Revive |
| **Magma** | Rare | 960,000 | 1,300 | Elemental | |
| **Quake** | Legendary | 1,000,000 | 1,500 | Natural | |
| **Buddha** | Legendary | 1,200,000 | 1,650 | Beast | |
| **Love** | Legendary | 1,300,000 | 1,700 | Natural | |
| **Creation** | Legendary | 1,400,000 | 1,750 | Natural | Thay thế Barrier |
| **Spider** | Legendary | 1,500,000 | 1,800 | Natural | Tên cũ String |
| **Sound** | Legendary | 1,700,000 | 1,900 | Natural | |
| **Phoenix** | Legendary | 1,800,000 | 2,000 | Beast | |
| **Portal** | Legendary | 1,900,000 | 2,000 | Natural | |
| **Lightning** | Legendary | 2,100,000 | 2,100 | Elemental | Tên cũ Rumble |
| **Pain** | Legendary | 2,300,000 | 2,200 | Natural | Tên cũ Paw |
| **Blizzard** | Legendary | 2,400,000 | 2,250 | Elemental | |
| **Gravity** | Mythical | 2,500,000 | 2,300 | Natural | |
| **Mammoth** | Mythical | 2,700,000 | 2,350 | Beast | |
| **T-Rex** | Mythical | 2,700,000 | 2,350 | Beast | |
| **Dough** | Mythical | 2,800,000 | 2,400 | Elemental | |
| **Shadow** | Mythical | 2,900,000 | 2,425 | Natural | |
| **Venom** | Mythical | 3,000,000 | 2,450 | Natural | |
| **Gas** | Mythical | 3,200,000 | 2,500 | Elemental | |
| **Spirit** | Mythical | 3,400,000 | 2,550 | Natural | Thay thế Soul |
| **Tiger** | Mythical | 5,000,000 | 3,000 | Beast | Thay thế Leopard |
| **Yeti** | Mythical | 5,000,000 | 3,000 | Beast | |
| **Kitsune** | Mythical | 8,000,000 | 4,000 | Beast | |
| **Control** | Mythical | 9,000,000 | 4,000 | Natural | |
| **Dragon** | Mythical | 15,000,000 | 5,000 | Beast | |

## ⚙️ 2. Quy tắc Backend (Worker)
- **Mapping**: Luôn chuyển đổi tên cũ sang tên mới (ví dụ `Falcon` -> `Eagle`) trước khi gửi dữ liệu về Frontend.
- **Dữ liệu**: Nếu API thiếu giá hoặc rarity, phải lấy từ bảng trên để bổ sung.
- **History**: Lưu tối đa 50 bản ghi lịch sử vào Cloudflare KV.

## 🎨 3. Quy tắc Frontend & UI
- **Hình ảnh**: File ảnh đặt tại `assets/fruits/[Tên_Mới].webp`.
- **Đường dẫn**: Sử dụng đường dẫn tương đối (không có dấu `/` ở đầu) để hỗ trợ xem file offline (`file://`).
- **Thanh điều hướng**: Đã bị xóa theo yêu cầu của User. Các liên kết pháp lý nằm ở Footer.
- **Aesthetics**: Giữ phong cách Dark Mode Premium, Glassmorphism, hiệu ứng Mythical Glow.

## 🚀 4. Deployment
- **Clean URL**: Cloudflare Pages sử dụng file `_redirects` để loại bỏ đuôi `.html`.
- **Git**: Người dùng (Minh Edward) sẽ tự thực hiện lệnh `push`. AI chỉ sửa code.

---
*Tài liệu này được tạo vào ngày 30/04/2026 bởi Antigravity dưới sự hướng dẫn của Minh Edward.*
