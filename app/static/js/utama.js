// Logika untuk mengecilkan header
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.hero');
    const currentPath = window.location.pathname;

    if (currentPath !== '/' && header) {
        header.classList.add('small'); // Tambahkan kelas 'small' jika bukan halaman utama
    }
});