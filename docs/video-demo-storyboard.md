# Kịch Bản Lời Thuyết Minh Video Demo

Tài liệu này dùng để đọc lời thuyết minh cho video demo HD của đồ án tốt nghiệp.

## Mục Tiêu

Giới thiệu mô hình bảo mật đa tầng theo hướng `defense-in-depth` với các lớp:

- firewall và phân đoạn mạng
- truy cập từ xa qua VPN
- phát hiện tấn công bằng Snort IDS/IPS
- tăng cường bảo mật máy chủ Ubuntu
- giám sát và phản ứng sự cố

## Cảnh 1: Mở Đầu

Hình:

- tiêu đề đề tài
- toàn bộ sơ đồ mạng

Lời thuyết minh:

- "Đây là đồ án nghiên cứu và triển khai mô hình bảo mật đa tầng theo hướng defense-in-depth."
- "Hệ thống được xây dựng trên pfSense, OpenVPN, Snort IDS/IPS, Ubuntu hardening và lớp giám sát sự cố."

## Cảnh 2: Kiến Trúc Tổng Quan

Hình:

- ảnh `network-topology.png`
- làm nổi bật pfSense ở trung tâm
- làm nổi bật các vùng LAN, WAN và OpenVPN

Lời thuyết minh:

- "Mạng được chia thành ba vùng chính là WAN, LAN và OpenVPN."
- "pfSense đóng vai trò firewall, gateway và điểm kết nối VPN."

## Cảnh 3: Các Máy Trong Lab

Hình:

- các máy ảo trong mô hình
- pfSense
- Ubuntu Server
- VPN client
- Kali attacker

Lời thuyết minh:

- "Lab này được triển khai trên bốn máy ảo."
- "Ubuntu là máy chủ nội bộ được bảo vệ, còn Kali được dùng để mô phỏng tấn công và kiểm thử."

## Cảnh 4: Lớp Firewall

Hình:

- rule WAN của pfSense
- các cổng bị chặn như Telnet, SMB, RDP và FTP

Lời thuyết minh:

- "Lớp firewall chặn các dịch vụ nguy hiểm và giữ nguyên nguyên tắc default deny."
- "Chỉ các dịch vụ cần thiết mới được phép đi qua."

## Cảnh 5: Lớp OpenVPN

Hình:

- log kết nối OpenVPN
- danh sách user VPN
- máy khách truy cập vào mạng nội bộ

Lời thuyết minh:

- "Người dùng hợp lệ kết nối qua OpenVPN để truy cập an toàn vào mạng LAN."
- "Lớp VPN đảm bảo xác thực trước khi cho phép vào hệ thống nội bộ."

## Cảnh 6: Lớp Snort IDS/IPS

Hình:

- cảnh báo Snort
- cảnh báo scan bằng Nmap
- cảnh báo ICMP bị chặn

Lời thuyết minh:

- "Snort được dùng để phát hiện các hành vi quét dò, truy cập bất thường và lưu lượng tấn công."
- "Ở chế độ IPS, một số traffic phù hợp với rule sẽ bị chặn tự động."

## Cảnh 7: Tăng Cường Bảo Mật Máy Chủ

Hình:

- checklist hardening Ubuntu
- fail2ban
- UFW
- auditd

Lời thuyết minh:

- "Máy chủ Ubuntu được tăng cường bảo mật bằng fail2ban, UFW, auditd và giới hạn đăng nhập SSH."
- "Đây là lớp phòng thủ ở mức host để bổ sung cho firewall và IDS."

## Cảnh 8: Giám Sát Và Phản Ứng

Hình:

- Grafana dashboard
- Loki logs
- syslog-ng
- màn hình auto-response

Lời thuyết minh:

- "Các log được gom tập trung để phục vụ giám sát và phân tích sự cố."
- "Module Python có thể đọc log, phát hiện sự kiện nghi ngờ và hỗ trợ chặn IP tấn công."

## Cảnh 9: Mô Phỏng Tấn Công

Hình:

- quét Nmap
- brute force SSH
- mô phỏng flood nhẹ

Lời thuyết minh:

- "Phần kiểm thử bao gồm quét mạng, brute force và mô phỏng flood nhẹ."
- "Mỗi tình huống đều được kiểm tra trên firewall, Snort và lớp bảo vệ host."

## Cảnh 10: Kết Luận

Hình:

- sơ đồ mạng cuối cùng
- ảnh kết quả tổng kết

Lời thuyết minh:

- "Kết quả cho thấy mô hình bảo mật đa tầng giúp tăng khả năng phát hiện, ngăn chặn và phản ứng sự cố trong môi trường lab."

## Gợi Ý Thời Lượng

- 90 đến 150 giây cho bản ngắn phục vụ CV
- 3 đến 5 phút cho bản thuyết trình đồ án

## Gợi Ý Chữ Hiển Thị Trên Video

- "Bảo mật đa tầng"
- "Firewall"
- "OpenVPN"
- "Snort IDS/IPS"
- "Host Hardening"
- "Monitoring and Incident Response"
- "Attack Validation"

