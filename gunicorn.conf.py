# gunicorn.conf.py

bind = "0.0.0.0:8000"  # Địa chỉ và cổng mà ứng dụng sẽ chạy trên đó
workers = 4  # Số lượng worker (nên chọn dựa trên số lượng CPU của máy chủ)
worker_class = "uvicorn.workers.UvicornWorker"  # Worker class cho FastAPI với Uvicorn
loglevel = "info"  # Mức độ ghi log
accesslog = "-"  # Ghi log truy cập vào stdout
errorlog = "-"  # Ghi log lỗi vào stdout
