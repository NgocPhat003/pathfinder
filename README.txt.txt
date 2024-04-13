Robot tìm đường
-----------------------------------------------------
1. Cho một bản đồ phẳng xOy (góc phần tư I), trên đó người ta đặt một điểm bắt đầu
S(xs, ys) và một điểm đích đến G(xG,yG). Đồng thời đặt các chướng ngại vật là các hình
đa giác lồi sao cho các đa giác không được đặt chồng lên nhau hay có điểm chung.
Không gian bản đồ được giới hạn trong một khung hình chữ nhật có góc trái dưới trùng
với gốc tọa độ, độ dày của khung là 1 đơn vị. Không có điểm nào trong bản đồ được vượt
hay đè lên khung này.
Chọn và cài đặt các thuật toán để tìm kiếm đường đi ngắn nhất từ S đến G sao cho
đường đi không được cắt xuyên qua các đa giác. Đường đi có thể men theo cạnh của đa
giác nhưng không được đè lên cạnh của nó. Biểu diễn đồ họa có thể ở mức đơn giản nhất
để người sử dụng thấy được các đa giác và đường đi.
Mức độ thực hiện được chia theo các mức như sau:
- Mức 1 (40%): cài đặt thành công 1 thuật toán để tìm đường đi từ S tới G. Báo
cáo lại thuật toán và quá trình chạy thử. Lưu ý, chạy thử trường hợp không có
đường đi.
- Mức 2 (30%): cài đặt ít nhất 3 thuật toán khác nhau (ví dụ tìm kiếm mù, tham
lam, heuristic, …). Báo cáo nhận xét sự khác nhau khi chạy thử 3 thuật toán.
- Mức 3 (20%): trên bản đồ sẽ xuất hiện thêm một số điểm khác được gọi là
điểm đón. Xuất phát từ S, sau đó đi đón tất cả các điểm này rồi đến trạng thái
G. Thứ tự các điểm đón không quan trọng. Mục tiêu là tìm ra cách để tổng
đường đi là nhỏ nhất. Báo cáo thuật toán đã áp dụng và quá trình chạy thử.
- Mức 4 (10%)(chưa làm được): các hình đa giác có thể di động được với tốc độ h tọa độ/s.
Cách thức di động có thể ở mức đơn giản nhất là tới lui một khoảng nhỏ để
đảm bảo không đè lên đa giác khác. Chạy ít nhất 1 thuật toán trên đó. Quay
video và đính kèm trực tiếp/link vào báo cáo.
- Mức 5 (điểm cộng 10%)(chưa làm được): thể hiện mô hình trên không gian 3 chiều (3D).\
-------------------------------------------------------------------------------
HƯỚNG DẪN SỬ DỤNG
Bước 1: Nếu chưa cài pygame thì phải cài, cách cài:
	Mở terminal, nhập:
	pip install pygame
	python -m pip install pygame
(Nếu đã cài rồi, bỏ qua bước 1)
Bước 2: Tại terminal, cd đến thư mục chứa source code rồi nhập:
	python main.py --file [inputFile] --option [optionName]
	(Trong đó: inputFile là tên file truyền vào, optionName là tên các cách tìm đường tương ứng:
	- A* search: "astar"
	- Tìm kiếm mù: "blind"
	- BFS: "BFS"
	- DFS: "DFS"
	- Tìm kiếm có điểm đón: "waypoints"
	Ex: python main.py --file input.txt --option astar
(Các file input có sẵn để test:
	input_1.txt, input_2.txt: 2 file này dùng để test tìm đường đi ngắn nhất nhưng không có điểm đón (checkpoint)
	input_3.txt, input_4.txt, input_5.txt: 3 file input này dùng để test các thuật toán tìm đường ngắn nhất, có các điểm đón (checkpoint) dọc đường
	input_6.txt, input_7.txt: 2 file này dùng để test tìm đường đi ngắn nhất trong trường hợp không tồn tại đường đi
	