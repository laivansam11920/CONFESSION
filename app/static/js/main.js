document.getElementById('confessionForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const status = document.getElementById('statusMsg');
    status.textContent = "ĐÃ GỬI CONFESSION THÀNH CÔNG! :)";
    status.style.display = "block";
    this.reset();
    setTimeout(() => {status.style.display = "none";}, 3500);
});