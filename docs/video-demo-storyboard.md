# Kịch Bản Video Demo Ngắn

Đây là bản lời thoại ngắn 60-90 giây để đọc trực tiếp khi quay video demo.

## Lời thoại

"Đây là đồ án nghiên cứu và triển khai mô hình bảo mật đa tầng theo hướng defense-in-depth. Hệ thống gồm pfSense, OpenVPN, Snort IDS/IPS, máy chủ Ubuntu được hardening, cùng lớp giám sát và phản ứng sự cố.

Kiến trúc mạng được chia thành ba vùng chính là WAN, LAN và OpenVPN. pfSense đóng vai trò firewall, gateway và điểm kết nối VPN. Trong lab, Ubuntu là máy chủ nội bộ cần bảo vệ, còn Kali được dùng để mô phỏng tấn công và kiểm thử.

Lớp firewall chặn các dịch vụ nguy hiểm như Telnet, SMB, RDP và FTP, đồng thời chỉ cho phép các dịch vụ cần thiết. Ở lớp OpenVPN, người dùng hợp lệ phải xác thực trước khi truy cập vào mạng nội bộ.

Snort IDS/IPS được dùng để phát hiện các hành vi quét dò, truy cập bất thường và lưu lượng tấn công. Khi gặp rule phù hợp, hệ thống có thể ghi nhận cảnh báo hoặc chặn traffic theo cấu hình.

Máy chủ Ubuntu được tăng cường bảo mật bằng UFW, fail2ban, auditd và giới hạn đăng nhập SSH. Toàn bộ log được gom về hệ thống giám sát để theo dõi và hỗ trợ phản ứng sự cố.

Phần kiểm thử gồm quét mạng, brute force SSH và mô phỏng flood nhẹ. Kết quả cho thấy mô hình bảo mật đa tầng giúp tăng khả năng phát hiện, ngăn chặn và phản ứng trong môi trường lab."

## Gợi Ý Hình Minh Họa

1. Tiêu đề đề tài
2. Sơ đồ mạng tổng thể
3. pfSense và các rule firewall
4. OpenVPN log và user list
5. Snort alert
6. Ubuntu hardening
7. Grafana / Loki / syslog-ng
8. Màn hình attack simulation
9. Kết luận

